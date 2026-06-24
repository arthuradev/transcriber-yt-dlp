"""Download execution domain model.

Pure data describing a download request, streamed progress, and results. No I/O
or yt-dlp here.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum

from transcriber.core.errors import AppError, ErrorSeverity


class DownloadStatus(StrEnum):
    """Lifecycle status reported during a download."""

    DOWNLOADING = "downloading"
    POST_PROCESSING = "post_processing"
    FINISHED = "finished"
    ERROR = "error"


@dataclass(frozen=True)
class DownloadProgress:
    """A single progress update for one item."""

    status: DownloadStatus
    downloaded_bytes: int
    total_bytes: int | None
    speed: float | None
    eta_seconds: int | None
    filename: str | None

    @property
    def fraction(self) -> float | None:
        """Completion fraction in [0, 1], or ``None`` if total is unknown."""
        if self.total_bytes and self.total_bytes > 0:
            return min(self.downloaded_bytes / self.total_bytes, 1.0)
        return None


ProgressCallback = Callable[[DownloadProgress], None]


@dataclass(frozen=True)
class DownloadRequest:
    """A request to download one item."""

    url: str
    format_selector: str
    output_path: str
    extract_audio: bool
    audio_format: str | None


@dataclass(frozen=True)
class DownloadResult:
    """The result of downloading one item."""

    ok: bool
    output_path: str | None
    error: str | None
    skipped: bool = False


@dataclass(frozen=True)
class DownloadOutcome:
    """Aggregate result of executing a plan."""

    results: tuple[DownloadResult, ...]

    @property
    def ok(self) -> bool:
        return bool(self.results) and all(result.ok for result in self.results)

    @property
    def succeeded(self) -> int:
        return sum(1 for result in self.results if result.ok and not result.skipped)

    @property
    def skipped(self) -> int:
        return sum(1 for result in self.results if result.skipped)

    @property
    def failed(self) -> int:
        return sum(1 for result in self.results if not result.ok)

    @property
    def output_paths(self) -> tuple[str, ...]:
        return tuple(
            r.output_path for r in self.results if r.ok and not r.skipped and r.output_path
        )


class DownloadError(AppError):
    """Raised when a download fails irrecoverably."""

    def __init__(self, message: str, *, detail: str | None = None) -> None:
        super().__init__(
            "E_DOWNLOAD",
            message,
            severity=ErrorSeverity.ERROR,
            detail=detail,
            recovery="Check the network connection, the URL, and available disk space.",
        )
