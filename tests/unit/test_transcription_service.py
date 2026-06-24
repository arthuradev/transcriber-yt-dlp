"""Tests for the GPU-only transcription service."""

from __future__ import annotations

import pytest

from transcriber.application.transcription import TranscriptionService
from transcriber.core.transcription import (
    Transcript,
    TranscriptionError,
    TranscriptionProgress,
    TranscriptionProgressCallback,
    TranscriptionRequest,
    TranscriptSegment,
)


def _request() -> TranscriptionRequest:
    return TranscriptionRequest("a.mp4", "large-v3", "", False)


class _Engine:
    def __init__(self, *, gpu: bool, transcript: Transcript | None = None) -> None:
        self._gpu = gpu
        self._transcript = transcript if transcript is not None else Transcript("en", ())
        self.called = False

    def gpu_available(self) -> bool:
        return self._gpu

    def transcribe(
        self, request: TranscriptionRequest, on_progress: TranscriptionProgressCallback
    ) -> Transcript:
        self.called = True
        on_progress(TranscriptionProgress(1.0, 2.0))
        return self._transcript


def test_aborts_without_gpu() -> None:
    engine = _Engine(gpu=False)
    with pytest.raises(TranscriptionError):
        TranscriptionService(engine).transcribe(_request(), lambda p: None)
    assert not engine.called


def test_transcribes_with_gpu() -> None:
    transcript = Transcript("en", (TranscriptSegment(0.0, 1.0, "hi"),))
    engine = _Engine(gpu=True, transcript=transcript)
    result = TranscriptionService(engine).transcribe(_request(), lambda p: None)
    assert result is transcript
    assert engine.called
