"""Interactive subtitle/transcript flow (probe -> pick language -> download subs).

Prefers existing subtitles: probes a single video URL, lists available subtitle
and auto-caption languages, downloads the chosen track, and falls back to a hint
about local transcription when none exist. Prompts, paths, and the clock are
injectable so the flow is testable without a terminal or network.
"""

from __future__ import annotations

import os
from collections.abc import Callable, Sequence
from datetime import date
from typing import Protocol

import questionary
from rich.console import Console
from rich.markup import escape
from rich.panel import Panel

from transcriber.application.probe import MediaProbeService
from transcriber.application.subtitles import SubtitleService
from transcriber.config.models import PathsConfig
from transcriber.core.media import MediaError, MediaMetadata
from transcriber.core.paths import plan_output_path
from transcriber.core.subtitles import SubtitleRequest
from transcriber.ui.i18n import Translator
from transcriber.ui.media import render_metadata


class SubtitleFlowPrompts(Protocol):
    """Prompts the subtitle flow needs."""

    def ask_url(self) -> str: ...
    def select_language(self, languages: Sequence[str]) -> str | None: ...


class QuestionarySubtitleFlowPrompts:
    """Questionary-backed prompts for the subtitle flow."""

    def __init__(self, translator: Translator) -> None:
        self._t = translator

    def ask_url(self) -> str:
        answer: str | None = questionary.text(self._t("plan.enter_url")).ask()
        return answer or ""

    def select_language(self, languages: Sequence[str]) -> str | None:
        choices = [questionary.Choice(title=lang, value=lang) for lang in languages]
        answer: str | None = questionary.select(
            self._t("subtitle.select_language"), choices=choices
        ).ask()
        return answer


class SubtitleFlow:
    """Drives the probe -> language -> subtitle-download sequence."""

    def __init__(
        self,
        *,
        probe_service: MediaProbeService,
        subtitle_service: SubtitleService,
        console: Console,
        translator: Translator,
        paths: PathsConfig,
        subtitle_format: str,
        prompts: SubtitleFlowPrompts,
        today: Callable[[], date] = date.today,
    ) -> None:
        self._probe_service = probe_service
        self._subtitle_service = subtitle_service
        self._console = console
        self._t = translator
        self._paths = paths
        self._subtitle_format = subtitle_format
        self._prompts = prompts
        self._today = today

    def run(self) -> None:
        self._run()
        self._pause()

    def _run(self) -> None:
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
        if not isinstance(result, MediaMetadata):
            self._console.print(f"[warning]{self._t('subtitle.playlist_unsupported')}[/warning]")
            return

        languages = self._available_languages(result)
        if not languages:
            self._console.print(f"[warning]{self._t('subtitle.none')}[/warning]")
            return

        language = self._prompts.select_language(languages)
        if language is None:
            return

        request = SubtitleRequest(
            url=result.webpage_url or url,
            languages=(language,),
            fmt=self._subtitle_format,
            output_base=self._output_base(result),
        )
        outcome = self._subtitle_service.download(request)
        if outcome.ok:
            body = "\n".join(escape(path) for path in outcome.files)
            self._console.print(
                Panel(body, title=self._t("subtitle.saved"), border_style="success")
            )
        else:
            self._console.print(
                f"[error]{self._t('subtitle.failed', error=escape(outcome.error or '?'))}[/error]"
            )

    def _available_languages(self, media: MediaMetadata) -> list[str]:
        languages = list(media.subtitle_languages)
        for lang in media.auto_caption_languages:
            if lang not in languages:
                languages.append(lang)
        return languages

    def _output_base(self, media: MediaMetadata) -> str:
        path = plan_output_path(
            output_dir=self._paths.download_dir,
            extractor=media.extractor,
            media_id=media.media_id,
            title=media.title,
            ext=self._subtitle_format,
            organize_by_site=self._paths.organize_by_site,
            organize_by_date=self._paths.organize_by_date,
            include_media_id=self._paths.include_media_id_in_filename,
            today=self._today(),
            group="",
        )
        return os.path.splitext(path)[0]

    def _pause(self) -> None:
        if self._console.is_terminal:
            self._console.input(f"[muted]{self._t('shell.press_enter')}[/muted] ")
