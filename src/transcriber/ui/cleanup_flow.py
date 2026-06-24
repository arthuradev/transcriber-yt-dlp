"""Interactive LLM transcript-cleanup flow.

Reads a transcript file, asks for explicit consent (only the transcript text is
sent to the provider — never audio/video), checks the API key, runs chunked
cleanup with the chosen style, and saves the cleaned transcript alongside the
raw one. Transcript content is never logged. Prompts, reader, key, and the
file-existence check are injectable for offline testing.
"""

from __future__ import annotations

import os
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Protocol

import questionary
from rich.console import Console
from rich.markup import escape
from rich.panel import Panel

from transcriber.application.cleanup import CleanupService
from transcriber.core.cleanup import CleanupProfile, LLMError, cleanup_profiles
from transcriber.ports.file_reader import TextFileReader
from transcriber.storage.text_store import save_text
from transcriber.ui.i18n import Translator


class CleanupFlowPrompts(Protocol):
    """Prompts the cleanup flow needs."""

    def ask_file(self) -> str: ...
    def confirm(self) -> bool: ...
    def select_profile(self, profiles: Sequence[CleanupProfile]) -> CleanupProfile | None: ...


class QuestionaryCleanupFlowPrompts:
    """Questionary-backed prompts for the cleanup flow."""

    def __init__(self, translator: Translator) -> None:
        self._t = translator

    def ask_file(self) -> str:
        answer: str | None = questionary.text(self._t("cleanup.enter_file")).ask()
        return answer or ""

    def confirm(self) -> bool:
        return bool(questionary.confirm(self._t("cleanup.confirm"), default=False).ask())

    def select_profile(self, profiles: Sequence[CleanupProfile]) -> CleanupProfile | None:
        choices = [questionary.Choice(title=p.profile_id, value=p.profile_id) for p in profiles]
        answer: str | None = questionary.select(
            self._t("cleanup.select_profile"), choices=choices
        ).ask()
        if answer is None:
            return None
        return next((p for p in profiles if p.profile_id == answer), None)


class CleanupFlow:
    """Drives the transcript-file -> consent -> clean -> save sequence."""

    def __init__(
        self,
        *,
        service: CleanupService,
        reader: TextFileReader,
        console: Console,
        translator: Translator,
        output_dir: str,
        model: str,
        api_key: str | None,
        prompts: CleanupFlowPrompts,
        path_exists: Callable[[str], bool] = os.path.isfile,
    ) -> None:
        self._service = service
        self._reader = reader
        self._console = console
        self._t = translator
        self._output_dir = output_dir
        self._model = model
        self._api_key = api_key
        self._prompts = prompts
        self._path_exists = path_exists

    def run(self) -> None:
        self._run()
        self._pause()

    def _run(self) -> None:
        path = self._prompts.ask_file().strip()
        if not path:
            return
        if not self._path_exists(path):
            self._console.print(
                f"[error]{self._t('cleanup.file_missing', path=escape(path))}[/error]"
            )
            return

        # Always ask before cleanup, after warning what is sent.
        self._console.print(Panel(self._t("cleanup.warning"), border_style="warning"))
        if not self._prompts.confirm():
            self._console.print(f"[muted]{self._t('cleanup.cancelled')}[/muted]")
            return
        if not self._api_key:
            self._console.print(f"[error]{self._t('cleanup.no_key')}[/error]")
            return

        profile = self._prompts.select_profile(cleanup_profiles())
        if profile is None:
            return

        try:
            text = self._reader.read_text(path)
        except OSError as exc:
            self._console.print(
                f"[error]{self._t('cleanup.failed', error=escape(str(exc)))}[/error]"
            )
            return

        try:
            cleaned = self._service.clean(text, profile, self._model)
        except LLMError as exc:
            self._console.print(
                f"[error]{self._t('cleanup.failed', error=escape(exc.message))}[/error]"
            )
            return

        source = Path(path)
        out_path = save_text(
            cleaned,
            output_dir=self._output_dir,
            stem=f"{source.stem}.clean",
            ext=source.suffix or ".txt",
        )
        self._console.print(
            Panel(escape(str(out_path)), title=self._t("cleanup.saved"), border_style="success")
        )

    def _pause(self) -> None:
        if self._console.is_terminal:
            self._console.input(f"[muted]{self._t('shell.press_enter')}[/muted] ")
