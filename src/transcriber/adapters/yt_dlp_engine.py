"""yt-dlp media engine adapter (probing and downloading).

This is the only module that imports yt-dlp (which ships only partial private
inline types), so the import and its untyped/loosely-typed calls are isolated
here behind a scoped pyright suppression. Dict mapping lives in
``yt_dlp_mapping`` and stays strictly typed. The info extractor and the
downloader are injectable so the engine is testable without yt-dlp or network.
"""
# yt-dlp exposes only partial, private inline types (_Params, _InfoDict), so its
# boundary is type-suppressed here and isolated from the rest of the codebase.
# pyright: reportMissingTypeStubs=false, reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false, reportUnknownArgumentType=false
# pyright: reportArgumentType=false, reportReturnType=false
# pyright: reportUnknownParameterType=false, reportMissingParameterType=false
# pyright: reportUnnecessaryComparison=false

from __future__ import annotations

import contextlib
from collections.abc import Callable
from typing import Any

from yt_dlp import YoutubeDL

from transcriber.adapters.yt_dlp_mapping import map_info, map_progress, output_template
from transcriber.core.download import (
    DownloadRequest,
    DownloadResult,
    ProgressCallback,
)
from transcriber.core.media import MediaError, ProbeResult

InfoExtractor = Callable[[str], dict[str, Any]]
Downloader = Callable[[DownloadRequest, ProgressCallback], DownloadResult]

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


def _final_path(ydl: Any, info: Any) -> str | None:
    if info is None:
        return None
    downloads = info.get("requested_downloads")
    if downloads:
        first = downloads[0]
        path = first.get("filepath") or first.get("_filename")
        if path:
            return str(path)
    try:
        return str(ydl.prepare_filename(info))
    except Exception:
        return None


def _default_download(request: DownloadRequest, on_progress: ProgressCallback) -> DownloadResult:
    """Download ``request`` with yt-dlp, streaming progress to ``on_progress``."""

    def hook(status: dict[str, Any]) -> None:
        with contextlib.suppress(Exception):
            on_progress(map_progress(status))

    options: dict[str, Any] = {
        "quiet": True,
        "no_warnings": True,
        "noprogress": True,
        "outtmpl": output_template(request.output_path),
        "progress_hooks": [hook],
    }
    if request.format_selector:
        options["format"] = request.format_selector
    if request.extract_audio:
        options["postprocessors"] = [
            {"key": "FFmpegExtractAudio", "preferredcodec": request.audio_format or "mp3"}
        ]

    try:
        with YoutubeDL(options) as ydl:
            info = ydl.extract_info(request.url, download=True)
            path = _final_path(ydl, info)
        return DownloadResult(ok=True, output_path=path, error=None)
    except Exception as exc:
        return DownloadResult(ok=False, output_path=None, error=str(exc))


class YtDlpEngine:
    """Probes and downloads media via yt-dlp."""

    def __init__(
        self,
        *,
        extract: InfoExtractor | None = None,
        download_fn: Downloader | None = None,
    ) -> None:
        self._extract = extract if extract is not None else _default_extract
        self._download = download_fn if download_fn is not None else _default_download

    def probe(self, url: str) -> ProbeResult:
        if not url.strip():
            raise MediaError("Empty URL")
        return map_info(self._extract(url))

    def download(self, request: DownloadRequest, on_progress: ProgressCallback) -> DownloadResult:
        return self._download(request, on_progress)
