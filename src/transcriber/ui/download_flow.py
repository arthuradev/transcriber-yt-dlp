"""Interactive download planning flow (URL -> probe -> profile -> dry-run).

A UI controller that sequences application services (probe, planner) and
rendering. It performs no download: it stops at the dry-run and confirmation.
Prompts are injected via a small protocol so the flow can be driven in tests
without a terminal.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

import questionary
from rich.console import Console
from rich.markup import escape

from transcriber.application.executor import DownloadExecutor
from transcriber.application.planner import DownloadPlanner
from transcriber.application.probe import MediaProbeService
from transcriber.config.models import PathsConfig
from transcriber.core.media import MediaError, MediaFormat, MediaMetadata, ProbeResult
from transcriber.core.profiles import (
    MANUAL_PROFILE_ID,
    DownloadProfile,
    manual_profile,
    profiles_for_category,
)
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


def _format_label(fmt: MediaFormat) -> str:
    resolution = f"{fmt.height}p" if fmt.height else (fmt.note or "")
    size = format_size(fmt.filesize)
    parts = [fmt.format_id, fmt.ext, resolution, size]
    return " | ".join(part for part in parts if part)


class DownloadFlowPrompts(Protocol):
    """Prompts the download flow needs."""

    def ask_url(self) -> str: ...
    def select_profile(self, profiles: Sequence[DownloadProfile]) -> DownloadProfile | None: ...
    def select_format(self, formats: Sequence[MediaFormat]) -> MediaFormat | None: ...
    def ask_output_dir(self, default: str) -> str: ...
    def confirm(self, *, strong: bool) -> bool: ...


class QuestionaryDownloadFlowPrompts:
    """Questionary-backed prompts for the download flow."""

    def __init__(self, translator: Translator) -> None:
        self._t = translator

    def ask_url(self) -> str:
        answer: str | None = questionary.text(self._t("plan.enter_url")).ask()
        return answer or ""

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


class DownloadFlow:
    """Drives the URL -> probe -> profile -> dry-run sequence."""

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
        success_art: AsciiArt | None = None,
    ) -> None:
        self._probe_service = probe_service
        self._planner = planner
        self._console = console
        self._t = translator
        self._paths = paths
        self._prompts = prompts
        self._executor = executor
        self._success_art = success_art

    def run(self, category: str) -> None:
        self._run(category)
        self._pause()

    def _run(self, category: str) -> None:
        url = self._prompts.ask_url().strip()
        if not url:
            return

        try:
            result = self._probe_service.probe(url)
        except MediaError as exc:
            self._console.print(
                f"[error]{self._t('plan.probe_failed', error=escape(exc.message))}[/error]"
            )
            return

        render_metadata(self._console, result, self._t)

        profile = self._choose_profile(category, result)
        if profile is None:
            return

        output_dir = self._prompts.ask_output_dir(self._paths.download_dir)
        effective_paths = self._paths.model_copy(update={"download_dir": output_dir})
        plan = self._planner.plan(result, profile, effective_paths)
        render_plan(self._console, plan, self._t)

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
        if (
            outcome.ok
            and self._success_art is not None
            and self._console.is_terminal
            and fits(self._success_art, self._console.width, min_width=_SUCCESS_ART_MIN_WIDTH)
        ):
            render_art(self._console, self._success_art)

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
