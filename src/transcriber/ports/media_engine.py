"""Ports for the media engine (metadata probing and downloading)."""

from __future__ import annotations

from collections.abc import Callable
from typing import Protocol

from transcriber.core.download import DownloadProgress, DownloadRequest, DownloadResult
from transcriber.core.media import ProbeResult


class MediaEnginePort(Protocol):
    """Contract for probing media metadata."""

    def probe(self, url: str) -> ProbeResult:
        """Probe ``url`` for metadata without downloading. Raises ``MediaError``."""
        ...


class DownloadEnginePort(Protocol):
    """Contract for downloading a single media item with progress."""

    def download(
        self,
        request: DownloadRequest,
        on_progress: Callable[[DownloadProgress], None],
    ) -> DownloadResult:
        """Download one item, calling ``on_progress`` as it advances."""
        ...
