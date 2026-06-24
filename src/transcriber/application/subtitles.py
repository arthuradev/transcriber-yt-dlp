"""Subtitle download use case.

Thin coordinator the UI calls to download existing subtitle tracks. Validates
input and delegates to the ``SubtitleEnginePort``.
"""

from __future__ import annotations

from transcriber.core.subtitles import SubtitleRequest, SubtitleResult
from transcriber.ports.subtitle_engine import SubtitleEnginePort


class SubtitleService:
    """Downloads existing subtitles via the subtitle engine port."""

    def __init__(self, engine: SubtitleEnginePort) -> None:
        self._engine = engine

    def download(self, request: SubtitleRequest) -> SubtitleResult:
        if not request.languages:
            return SubtitleResult(ok=False, files=(), error="No language selected")
        return self._engine.download_subtitles(request)
