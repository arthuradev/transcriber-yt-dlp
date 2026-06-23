"""yt-dlp media engine adapter (implements MediaEnginePort).

This is the only module that imports yt-dlp (which ships no type information),
so the import and its untyped calls are isolated here behind a scoped pyright
suppression. The dict -> domain mapping lives in ``yt_dlp_mapping`` and stays
strictly typed. The info extractor is injectable so the engine is testable
without yt-dlp or network access.
"""
# yt-dlp exposes only partial, private inline types (_Params, _InfoDict), so its
# boundary is type-suppressed here and isolated from the rest of the codebase.
# pyright: reportMissingTypeStubs=false, reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false, reportUnknownArgumentType=false
# pyright: reportArgumentType=false, reportReturnType=false
# pyright: reportUnnecessaryComparison=false

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from yt_dlp import YoutubeDL

from transcriber.adapters.yt_dlp_mapping import map_info
from transcriber.core.media import MediaError, ProbeResult

InfoExtractor = Callable[[str], dict[str, Any]]

_PROBE_OPTIONS: dict[str, Any] = {
    "quiet": True,
    "no_warnings": True,
    "skip_download": True,
    "extract_flat": "in_playlist",
}


def _default_extract(url: str) -> dict[str, Any]:
    """Probe ``url`` with yt-dlp, returning a sanitized info dict."""
    try:
        with YoutubeDL(_PROBE_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            if info is None:
                raise MediaError("No metadata returned for URL")
            return ydl.sanitize_info(info)
    except MediaError:
        raise
    except Exception as exc:  # yt-dlp raises a variety of error types
        raise MediaError("Failed to probe URL", detail=str(exc)) from exc


class YtDlpEngine:
    """Probes media metadata via yt-dlp."""

    def __init__(self, *, extract: InfoExtractor | None = None) -> None:
        self._extract = extract if extract is not None else _default_extract

    def probe(self, url: str) -> ProbeResult:
        if not url.strip():
            raise MediaError("Empty URL")
        return map_info(self._extract(url))
