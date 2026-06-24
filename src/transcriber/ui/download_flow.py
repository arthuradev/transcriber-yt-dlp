"""Interactive download flow (source -> probe -> profile -> dry-run -> execute).

A UI controller that sequences application services (probe, batch, planner,
executor) and rendering. Supports a single URL or a ``.txt`` batch file, builds a
dry-run plan, confirms, then executes (for downloadable profiles) with progress.
Prompts are injected via a small protocol so the flow can be driven in tests
without a terminal.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol

import questionary
from rich.console import Console
from rich.markup import escape
from rich.panel import Panel

from transcriber.application.batch import BatchProbeService
from transcriber.application.executor import DownloadExecutor
from transcriber.application.planner import DownloadPlanner
from transcriber.application.probe import MediaProbeService
from transcriber.application.reporting import build_download_report
from transcriber.config.models import CookiesConfig, PathsConfig
from transcriber.core.media import MediaError, MediaFormat, MediaMetadata, ProbeResult
from transcriber.core.plan import DownloadPlan
from transcriber.core.profiles import (
    MANUAL_PROFILE_ID,
    DownloadProfile,
    manual_profile,
    profiles_for_category,
)
from transcriber.observability.recorder import OperationRecorder
from transcriber.safety.audit import AuditLog
from transcriber.safety.cookies import evaluate_cookies
from transcriber.ui.ascii_art import AsciiArt, fits, render_art
from transcriber.ui.download_result import render_download_summary
from transcriber.ui.i18n import Translator
from transcriber.ui.media import format_size, render_metadata
from transcriber.ui.plan import render_plan
from transcriber.ui.progress import ProgressPresenter

_SUCCESS_ART_MIN_WIDTH = 110

# Sentinel entry appended to the profile list to offer manual format selection.
MANUAL_PROFILE = DownloadProfile(
    profile_id=MANUAL_PROFILE_ID,
    kind="video",
    format_selector="",
    default_ext="",
    extract_audio=False,
    audio_format=None,
    requires_ffmpeg=False,
)


@dataclass(frozen=True)
class DownloadSource:
    """Where to download from: a single URL or a batch ``.txt`` file path."""

    is_batch: bool
    value: str


def _format_label(fmt: MediaFormat) -> str:
    resolution = f"{fmt.height}p" if fmt.height else (fmt.note or "")
    parts = [fmt.format_id, fmt.ext, resolution, format_size(fmt.filesize)]
    return " | ".join(part for part in parts if part)


class DownloadFlowPrompts(Protocol):
    """Prompts the download flow needs."""

    def ask_source(self) -> DownloadSource | None: ...
    def select_profile(self, profiles: Sequence[DownloadProfile]) -> DownloadProfile | None: ...
    def select_format(self, formats: Sequence[MediaFormat]) -> MediaFormat | None: ...
    def ask_output_dir(self, default: str) -> str: ...
    def confirm(self, *, strong: bool) -> bool: ...
    def confirm_cookies(self) -> bool: ...


class QuestionaryDownloadFlowPrompts:
    """Questionary-backed prompts for the download flow."""

    def __init__(self, translator: Translator) -> None:
        self._t = translator

    def ask_source(self) -> DownloadSource | None:
        choices = [
            questionary.Choice(title=self._t("source.single"), value="single"),
            questionary.Choice(title=self._t("source.batch"), value="batch"),
        ]
        kind: str | None = questionary.select(self._t("source.prompt"), choices=choices).ask()
        if kind is None:
            return None
        if kind == "batch":
            path: str | None = questionary.text(self._t("source.file")).ask()
            return DownloadSource(is_batch=True, value=path or "")
        url: str | None = questionary.text(self._t("plan.enter_url")).ask()
        return DownloadSource(is_batch=False, value=url or "")

    def select_profile(self, profiles: Sequence[DownloadProfile]) -> DownloadProfile | None:
        choices = [
            questionary.Choice(title=self._profile_title(p), value=p.profile_id) for p in profiles
        ]
        answer: str | None = questionary.select(
            self._t("plan.select_profile"), choices=choices
        ).ask()
        if answer is None:
            return None
        return next((p for p in profiles if p.profile_id == answer), None)

    def _profile_title(self, profile: DownloadProfile) -> str:
        if profile.profile_id == MANUAL_PROFILE_ID:
            return self._t("plan.manual_format")
        return profile.profile_id

    def select_format(self, formats: Sequence[MediaFormat]) -> MediaFormat | None:
        choices = [questionary.Choice(title=_format_label(f), value=f.format_id) for f in formats]
        answer: str | None = questionary.select(
            self._t("plan.select_format"), choices=choices
        ).ask()
        if answer is None:
            return None
        return next((f for f in formats if f.format_id == answer), None)

    def ask_output_dir(self, default: str) -> str:
        answer: str | None = questionary.text(self._t("plan.output"), default=default).ask()
        return answer or default

    def confirm(self, *, strong: bool) -> bool:
        message = self._t("plan.confirm_strong") if strong else self._t("plan.confirm")
        return bool(questionary.confirm(message, default=not strong).ask())

    def confirm_cookies(self) -> bool:
        return bool(questionary.confirm(self._t("cookies.confirm"), default=False).ask())


class DownloadFlow:
    """Drives the source -> probe -> profile -> dry-run -> execute sequence."""

    def __init__(
        self,
        *,
        probe_service: MediaProbeService,
        planner: DownloadPlanner,
        console: Console,
        translator: Translator,
        paths: PathsConfig,
        prompts: DownloadFlowPrompts,
        executor: DownloadExecutor | None = None,
        batch_service: BatchProbeService | None = None,
        success_art: AsciiArt | None = None,
        cookies: CookiesConfig | None = None,
        audit: AuditLog | None = None,
        recorder: OperationRecorder | None = None,
    ) -> None:
        self._probe_service = probe_service
        self._planner = planner
        self._console = console
        self._t = translator
        self._paths = paths
        self._prompts = prompts
        self._executor = executor
        self._batch_service = batch_service
        self._success_art = success_art
        self._cookies = cookies if cookies is not None else CookiesConfig()
        self._audit = audit
        self._recorder = recorder

    def run(self, category: str) -> None:
        self._run(category)
        self._pause()

    def _run(self, category: str) -> None:
        source = self._prompts.ask_source()
        if source is None or not source.value.strip():
            return

        if source.is_batch:
            plan = self._plan_from_batch(category, source.value.strip())
        else:
            plan = self._plan_from_url(category, source.value.strip())
        if plan is None:
            return

        self._execute_plan(plan)

    def _plan_from_url(self, category: str, url: str) -> DownloadPlan | None:
        try:
            result = self._probe_service.probe(url)
        except MediaError as exc:
            self._console.print(
                f"[error]{self._t('plan.probe_failed', error=escape(exc.message))}[/error]"
            )
            return None

        render_metadata(self._console, result, self._t)
        profile = self._choose_profile(category, result)
        if profile is None:
            return None
        return self._build_plan([result], profile)

    def _plan_from_batch(self, category: str, path: str) -> DownloadPlan | None:
        if self._batch_service is None:
            self._console.print(f"[error]{self._t('batch.unavailable')}[/error]")
            return None

        batch = self._batch_service.probe_file(path)
        for error in batch.errors:
            self._console.print(f"[warning]- {escape(error)}[/warning]")
        if not batch.results:
            self._console.print(f"[error]{self._t('batch.none')}[/error]")
            return None

        self._console.print(f"[info]{self._t('batch.found', count=len(batch.results))}[/info]")
        profile = self._choose_named_profile(category)
        if profile is None:
            return None
        return self._build_plan(batch.results, profile)

    def _build_plan(self, probes: Sequence[ProbeResult], profile: DownloadProfile) -> DownloadPlan:
        output_dir = self._prompts.ask_output_dir(self._paths.download_dir)
        paths = self._paths.model_copy(update={"download_dir": output_dir})
        cookies_browser = self._resolve_cookies()
        plan = self._planner.plan_batch(
            probes, profile, paths, cookies_from_browser=cookies_browser
        )
        render_plan(self._console, plan, self._t)
        return plan

    def _resolve_cookies(self) -> str | None:
        """Cookie guard: only return a browser when enabled, allowed, and confirmed."""
        if not self._cookies.enabled:
            return None
        decision = evaluate_cookies(self._cookies)
        if not decision.allowed:
            self._console.print(f"[warning]{escape(decision.reason)}[/warning]")
            return None
        self._console.print(
            Panel(self._t("cookies.warning"), title=self._t("cookies.title"), border_style="error")
        )
        if decision.requires_confirmation and not self._prompts.confirm_cookies():
            return None
        return decision.browser

    def _execute_plan(self, plan: DownloadPlan) -> None:
        if (
            plan.requires_confirmation
            and plan.has_items
            and not self._prompts.confirm(strong=plan.requires_strong_confirmation)
        ):
            self._console.print(f"[muted]{self._t('plan.cancelled')}[/muted]")
            return

        if not plan.is_downloadable or self._executor is None or not plan.has_items:
            self._console.print(f"[info]{self._t('plan.execution_later')}[/info]")
            return

        with ProgressPresenter(self._console, self._t) as presenter:
            outcome = self._executor.execute(plan, on_progress=presenter.update)

        render_download_summary(self._console, outcome, self._t)
        if self._audit is not None:
            self._audit.record(
                "download",
                plan.risk,
                f"items={plan.item_count} ok={outcome.succeeded} "
                f"skipped={outcome.skipped} failed={outcome.failed} "
                f"cookies={'yes' if plan.cookies_from_browser else 'no'}",
            )
        if self._recorder is not None:
            self._recorder.record(build_download_report(plan, outcome))
        if (
            outcome.ok
            and self._success_art is not None
            and self._console.is_terminal
            and fits(self._success_art, self._console.width, min_width=_SUCCESS_ART_MIN_WIDTH)
        ):
            render_art(self._console, self._success_art)

    def _choose_named_profile(self, category: str) -> DownloadProfile | None:
        profiles = profiles_for_category(category)
        if not profiles:
            return None
        return self._prompts.select_profile(profiles)

    def _choose_profile(self, category: str, result: ProbeResult) -> DownloadProfile | None:
        profiles = list(profiles_for_category(category))
        if not profiles:
            return None
        manual_possible = isinstance(result, MediaMetadata) and bool(result.formats)
        if manual_possible:
            profiles.append(MANUAL_PROFILE)

        chosen = self._prompts.select_profile(profiles)
        if chosen is None:
            return None
        if chosen.profile_id != MANUAL_PROFILE_ID:
            return chosen

        # Manual mode: result is a MediaMetadata with formats (guaranteed above).
        assert isinstance(result, MediaMetadata)
        fmt = self._prompts.select_format(result.formats)
        if fmt is None:
            return None
        return manual_profile(fmt)

    def _pause(self) -> None:
        if self._console.is_terminal:
            self._console.input(f"[muted]{self._t('shell.press_enter')}[/muted] ")
