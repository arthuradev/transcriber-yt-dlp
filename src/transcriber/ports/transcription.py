"""Port for the transcription engine (GPU-only)."""

from __future__ import annotations

from typing import Protocol

from transcriber.core.transcription import (
    Transcript,
    TranscriptionProgressCallback,
    TranscriptionRequest,
)


class TranscriptionEnginePort(Protocol):
    """Contract for a GPU-only transcription engine."""

    def gpu_available(self) -> bool:
        """Whether a CUDA GPU (and the engine) is available."""
        ...

    def transcribe(
        self,
        request: TranscriptionRequest,
        on_progress: TranscriptionProgressCallback,
    ) -> Transcript:
        """Transcribe the request, streaming progress. Raises ``TranscriptionError``."""
        ...
