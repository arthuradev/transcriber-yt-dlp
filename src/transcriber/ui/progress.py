"""Live download progress display.

A thin wrapper over Rich's ``Progress``. It renders only on a real terminal; on
captured/non-interactive streams (tests) it is a no-op, so the executor can run
without emitting control sequences.
"""

from __future__ import annotations

from types import TracebackType

from rich.console import Console
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TaskID,
    TaskProgressColumn,
    TextColumn,
    TransferSpeedColumn,
)

from transcriber.core.download import DownloadProgress
from transcriber.core.transcription import TranscriptionProgress
from transcriber.ui.i18n import Translator


class ProgressPresenter:
    """Context manager that shows download progress on a terminal."""

    def __init__(self, console: Console, translator: Translator) -> None:
        self._console = console
        self._t = translator
        self._progress: Progress | None = None
        self._task: TaskID | None = None

    def __enter__(self) -> ProgressPresenter:
        if self._console.is_terminal:
            self._progress = Progress(
                TextColumn("[accent]{task.description}[/accent]"),
                BarColumn(),
                TaskProgressColumn(),
                DownloadColumn(),
                TransferSpeedColumn(),
                console=self._console,
                transient=True,
            )
            self._progress.start()
            self._task = self._progress.add_task(self._t("download.downloading"), total=None)
        return self

    def update(self, progress: DownloadProgress) -> None:
        if self._progress is None or self._task is None:
            return
        total = float(progress.total_bytes) if progress.total_bytes else None
        self._progress.update(
            self._task,
            total=total,
            completed=float(progress.downloaded_bytes),
        )

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if self._progress is not None:
            self._progress.stop()


class TranscriptionProgressPresenter:
    """Context manager that shows transcription progress (by media seconds)."""

    def __init__(self, console: Console, translator: Translator) -> None:
        self._console = console
        self._t = translator
        self._progress: Progress | None = None
        self._task: TaskID | None = None

    def __enter__(self) -> TranscriptionProgressPresenter:
        if self._console.is_terminal:
            self._progress = Progress(
                TextColumn("[accent]{task.description}[/accent]"),
                BarColumn(),
                TaskProgressColumn(),
                console=self._console,
                transient=True,
            )
            self._progress.start()
            self._task = self._progress.add_task(self._t("transcribe.working"), total=None)
        return self

    def update(self, progress: TranscriptionProgress) -> None:
        if self._progress is None or self._task is None:
            return
        total = progress.total_seconds if progress.total_seconds > 0 else None
        self._progress.update(self._task, total=total, completed=progress.processed_seconds)

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if self._progress is not None:
            self._progress.stop()
