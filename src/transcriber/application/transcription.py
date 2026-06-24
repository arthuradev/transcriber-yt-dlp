"""Transcription use case.

Enforces the GPU-only policy (no CPU fallback): if no CUDA GPU is available it
aborts with a helpful ``TranscriptionError`` before doing any work. Otherwise it
delegates to the ``TranscriptionEnginePort``.
"""

from __future__ import annotations

from transcriber.core.transcription import (
    Transcript,
    TranscriptionError,
    TranscriptionProgressCallback,
    TranscriptionRequest,
)
from transcriber.ports.transcription import TranscriptionEnginePort


class TranscriptionService:
    """Coordinates GPU-only transcription."""

    def __init__(self, engine: TranscriptionEnginePort) -> None:
        self._engine = engine

    def transcribe(
        self,
        request: TranscriptionRequest,
        on_progress: TranscriptionProgressCallback,
    ) -> Transcript:
        if not self._engine.gpu_available():
            raise TranscriptionError(
                "No CUDA GPU available; transcription is GPU-only (no CPU fallback)."
            )
        return self._engine.transcribe(request, on_progress)
