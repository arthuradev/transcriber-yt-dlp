"""Tests for the interactive transcription flow."""

from __future__ import annotations

import io
from pathlib import Path

from rich.console import Console

from transcriber.application.transcription import TranscriptionService
from transcriber.config.models import Language, TranscriptionConfig
from transcriber.core.transcription import (
    Transcript,
    TranscriptionProgress,
    TranscriptionProgressCallback,
    TranscriptionRequest,
    TranscriptSegment,
)
from transcriber.ui.i18n import Translator
from transcriber.ui.transcribe_flow import TranscribeFlow


class _Engine:
    def __init__(self, *, gpu: bool, transcript: Transcript | None = None) -> None:
        self._gpu = gpu
        self._transcript = (
            transcript
            if transcript is not None
            else Transcript("en", (TranscriptSegment(0.0, 1.0, "hi"),))
        )

    def gpu_available(self) -> bool:
        return self._gpu

    def transcribe(
        self, request: TranscriptionRequest, on_progress: TranscriptionProgressCallback
    ) -> Transcript:
        on_progress(TranscriptionProgress(1.0, 1.0))
        return self._transcript


class _Prompts:
    def __init__(self, path: str) -> None:
        self._path = path

    def ask_file(self) -> str:
        return self._path


def _flow(
    console: Console,
    engine: _Engine,
    prompts: _Prompts,
    output_dir: str,
    *,
    exists: bool = True,
) -> TranscribeFlow:
    return TranscribeFlow(
        service=TranscriptionService(engine),
        console=console,
        translator=Translator(Language.EN_US),
        config=TranscriptionConfig(),
        output_dir=output_dir,
        prompts=prompts,
        path_exists=lambda p: exists,
    )


def test_flow_aborts_without_gpu(
    console_buffer: tuple[Console, io.StringIO], tmp_path: Path
) -> None:
    console, buffer = console_buffer
    _flow(console, _Engine(gpu=False), _Prompts("a.mp4"), str(tmp_path)).run()
    output = buffer.getvalue()
    assert "GPU required" in output
    assert "GPU-only" in output


def test_flow_transcribes_and_saves(
    console_buffer: tuple[Console, io.StringIO], tmp_path: Path
) -> None:
    console, buffer = console_buffer
    _flow(console, _Engine(gpu=True), _Prompts("video.mp4"), str(tmp_path)).run()
    assert "Transcript saved" in buffer.getvalue()
    assert (tmp_path / "video.txt").is_file()


def test_flow_missing_file(console_buffer: tuple[Console, io.StringIO], tmp_path: Path) -> None:
    console, buffer = console_buffer
    _flow(console, _Engine(gpu=True), _Prompts("nope.mp4"), str(tmp_path), exists=False).run()
    assert "File not found" in buffer.getvalue()
