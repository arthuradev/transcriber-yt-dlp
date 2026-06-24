"""Port for downloading existing subtitle tracks."""

from __future__ import annotations

from typing import Protocol

from transcriber.core.subtitles import SubtitleRequest, SubtitleResult


class SubtitleEnginePort(Protocol):
    """Contract for downloading existing subtitles/captions."""

    def download_subtitles(self, request: SubtitleRequest) -> SubtitleResult:
        """Download the requested subtitle tracks."""
        ...
