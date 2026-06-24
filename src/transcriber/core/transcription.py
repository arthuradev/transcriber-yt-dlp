"""Transcription domain model.

Pure data describing a transcription request, streamed progress, and the
resulting transcript. No faster-whisper, GPU, or I/O here.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from transcriber.core.errors import AppError, ErrorSeverity


@dataclass(frozen=True)
class TranscriptionRequest:
    """A request to transcribe one media file (GPU-only)."""

    audio_path: str
    model: str
    language: str  # "" means auto-detect
    translate: bool


@dataclass(frozen=True)
class TranscriptionProgress:
    """Progress of a transcription, measured in media seconds processed."""

    processed_seconds: float
    total_seconds: float

    @property
    def fraction(self) -> float | None:
        if self.total_seconds > 0:
            return min(self.processed_seconds / self.total_seconds, 1.0)
        return None


TranscriptionProgressCallback = Callable[[TranscriptionProgress], None]


@dataclass(frozen=True)
class TranscriptSegment:
    """A single timed transcript segment."""

    start: float
    end: float
    text: str


@dataclass(frozen=True)
class Transcript:
    """A full transcript with timed segments."""

    language: str
    segments: tuple[TranscriptSegment, ...]

    @property
    def text(self) -> str:
        return "\n".join(segment.text for segment in self.segments)

    @property
    def duration(self) -> float:
        return self.segments[-1].end if self.segments else 0.0


class TranscriptionError(AppError):
    """Raised when transcription cannot run (e.g. no CUDA GPU) or fails."""

    def __init__(self, message: str, *, detail: str | None = None) -> None:
        super().__init__(
            "E_TRANSCRIPTION",
            message,
            severity=ErrorSeverity.ERROR,
            detail=detail,
            recovery=(
                "Transcription is GPU-only. Install the transcription extra "
                "(faster-whisper) and CUDA, and ensure an NVIDIA GPU is available."
            ),
        )
