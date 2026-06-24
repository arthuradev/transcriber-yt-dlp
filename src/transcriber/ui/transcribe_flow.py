"""Interactive transcription flow (local file -> GPU transcribe -> save).

Prompts for a local media file, runs GPU-only transcription (aborting with a
helpful message when no CUDA GPU is available), saves the raw transcript, and
shows a summary. Prompts and the file-existence check are injectable so the flow
is testable without a terminal or real files.
"""

from __future__ import annotations

import os
from collections.abc import Callable
from pathlib import Path
from typing import Protocol

import questionary
from rich.console import Console
from rich.markup import escape
from rich.panel import Panel

from transcriber.application.transcription import TranscriptionService
from transcriber.config.models import TranscriptionConfig
from transcriber.core.transcription import TranscriptionError, TranscriptionRequest
from transcriber.storage.transcript_store import save_transcript
from transcriber.ui.i18n import Translator
from transcriber.ui.progress import TranscriptionProgressPresenter


class TranscribeFlowPrompts(Protocol):
    """Prompts the transcription flow needs."""

    def ask_file(self) -> str: ...


class QuestionaryTranscribeFlowPrompts:
    """Questionary-backed prompts for the transcription flow."""

    def __init__(self, translator: Translator) -> None:
        self._t = translator

    def ask_file(self) -> str:
        answer: str | None = questionary.text(self._t("transcribe.enter_file")).ask()
        return answer or ""


class TranscribeFlow:
    """Drives the local-file -> transcribe -> save sequence."""

    def __init__(
        self,
        *,
        service: TranscriptionService,
        console: Console,
        translator: Translator,
        config: TranscriptionConfig,
        output_dir: str,
        prompts: TranscribeFlowPrompts,
        path_exists: Callable[[str], bool] = os.path.isfile,
    ) -> None:
        self._service = service
        self._console = console
        self._t = translator
        self._config = config
        self._output_dir = output_dir
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
                f"[error]{self._t('transcribe.file_missing', path=escape(path))}[/error]"
            )
            return

        request = TranscriptionRequest(
            audio_path=path,
            model=self._config.model,
            language=self._config.language,
            translate=self._config.translate,
        )
        try:
            with TranscriptionProgressPresenter(self._console, self._t) as presenter:
                transcript = self._service.transcribe(request, presenter.update)
        except TranscriptionError as exc:
            body = escape(exc.message)
            if exc.recovery:
                body = f"{body}\n{escape(exc.recovery)}"
            self._console.print(
                Panel(body, title=self._t("transcribe.gpu_required"), border_style="error")
            )
            return

        out_path = save_transcript(
            transcript,
            output_dir=self._output_dir,
            stem=Path(path).stem,
            fmt=self._config.output_format,
        )
        summary = self._t(
            "transcribe.summary",
            language=transcript.language or "?",
            segments=len(transcript.segments),
        )
        self._console.print(
            Panel(
                f"{summary}\n{escape(str(out_path))}",
                title=self._t("transcribe.saved"),
                border_style="success",
            )
        )

    def _pause(self) -> None:
        if self._console.is_terminal:
            self._console.input(f"[muted]{self._t('shell.press_enter')}[/muted] ")
