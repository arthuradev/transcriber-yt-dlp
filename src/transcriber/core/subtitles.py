"""Subtitle download domain model (pure)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SubtitleRequest:
    """A request to download subtitle tracks for one media URL."""

    url: str
    languages: tuple[str, ...]
    fmt: str  # "srt" | "vtt"
    output_base: str  # path stem (no extension); the engine appends .<lang>.<fmt>


@dataclass(frozen=True)
class SubtitleResult:
    """The result of a subtitle download."""

    ok: bool
    files: tuple[str, ...]
    error: str | None
