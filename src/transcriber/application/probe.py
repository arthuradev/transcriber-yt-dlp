"""Metadata probe use case.

Thin coordinator the UI calls to probe a URL. Validates input and delegates to
the ``MediaEnginePort``; the UI never talks to the engine adapter directly.
"""

from __future__ import annotations

from transcriber.core.media import MediaError, ProbeResult
from transcriber.ports.media_engine import MediaEnginePort


class MediaProbeService:
    """Probes URLs for metadata via the media engine port."""

    def __init__(self, engine: MediaEnginePort) -> None:
        self._engine = engine

    def probe(self, url: str) -> ProbeResult:
        """Probe ``url`` for metadata. Raises ``MediaError`` on empty/invalid input."""
        cleaned = url.strip()
        if not cleaned:
            raise MediaError("Empty URL")
        return self._engine.probe(cleaned)
