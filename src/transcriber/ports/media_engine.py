"""Port for the media engine (metadata probing)."""

from __future__ import annotations

from typing import Protocol

from transcriber.core.media import ProbeResult


class MediaEnginePort(Protocol):
    """Contract for the media engine."""

    def probe(self, url: str) -> ProbeResult:
        """Probe ``url`` for metadata without downloading. Raises ``MediaError``."""
        ...
