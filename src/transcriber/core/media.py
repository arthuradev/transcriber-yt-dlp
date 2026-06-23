"""Media metadata domain model.

Pure data describing what a probe found (a single media item or a playlist),
plus the domain error raised when a probe fails. No network or yt-dlp here.
"""

from __future__ import annotations

from dataclasses import dataclass

from transcriber.core.errors import AppError, ErrorSeverity


@dataclass(frozen=True)
class MediaFormat:
    """A single downloadable format reported by the engine."""

    format_id: str
    ext: str
    height: int | None
    filesize: int | None
    vcodec: str | None
    acodec: str | None
    note: str | None


@dataclass(frozen=True)
class MediaMetadata:
    """Metadata for a single media item."""

    media_id: str
    title: str
    extractor: str
    webpage_url: str
    duration_seconds: float | None
    uploader: str | None
    formats: tuple[MediaFormat, ...]


@dataclass(frozen=True)
class PlaylistEntry:
    """A lightweight entry within a playlist (from a flat probe)."""

    media_id: str
    title: str
    url: str


@dataclass(frozen=True)
class PlaylistMetadata:
    """Metadata for a playlist."""

    playlist_id: str
    title: str
    extractor: str
    webpage_url: str
    entry_count: int
    entries: tuple[PlaylistEntry, ...]


ProbeResult = MediaMetadata | PlaylistMetadata


class MediaError(AppError):
    """Raised when media metadata cannot be probed or parsed."""

    def __init__(self, message: str, *, detail: str | None = None) -> None:
        super().__init__(
            "E_MEDIA",
            message,
            severity=ErrorSeverity.ERROR,
            detail=detail,
            recovery="Check the URL is valid and supported by yt-dlp.",
        )
