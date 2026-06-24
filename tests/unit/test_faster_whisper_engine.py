"""Tests for the faster-whisper engine adapter (no GPU / dependency needed)."""

from __future__ import annotations

from transcriber.adapters.faster_whisper_engine import FasterWhisperEngine
from transcriber.core.transcription import Transcript, TranscriptionRequest, TranscriptSegment


def test_default_gpu_unavailable_without_cuda() -> None:
    # No CUDA / ctranslate2 in the test environment: must report False, not crash.
    assert FasterWhisperEngine().gpu_available() is False


def test_injected_engine_transcribes() -> None:
    engine = FasterWhisperEngine(
        gpu_check=lambda: True,
        transcribe_fn=lambda r, cb: Transcript("en", (TranscriptSegment(0.0, 1.0, "x"),)),
    )
    assert engine.gpu_available() is True
    result = engine.transcribe(TranscriptionRequest("a", "m", "", False), lambda p: None)
    assert result.segments[0].text == "x"
