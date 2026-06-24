"""Batch probe use case.

Reads a ``.txt`` URL list (via a ``TextFileReader`` port), parses the URLs, and
probes each through the ``MediaEnginePort``, collecting successes and per-URL
errors. Never raises for individual failures.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from transcriber.core.batch import parse_url_list
from transcriber.core.media import MediaError, ProbeResult
from transcriber.ports.file_reader import TextFileReader
from transcriber.ports.media_engine import MediaEnginePort


@dataclass(frozen=True)
class BatchProbeResult:
    """The probed items and any per-URL errors from a batch file."""

    results: tuple[ProbeResult, ...]
    errors: tuple[str, ...]


class BatchProbeService:
    """Reads and probes a batch URL file."""

    def __init__(self, engine: MediaEnginePort, reader: TextFileReader) -> None:
        self._engine = engine
        self._reader = reader

    def probe_file(self, path: str) -> BatchProbeResult:
        try:
            text = self._reader.read_text(path)
        except OSError as exc:
            return BatchProbeResult(results=(), errors=(f"Could not read file: {exc}",))

        return self._probe_urls(parse_url_list(text))

    def _probe_urls(self, urls: Sequence[str]) -> BatchProbeResult:
        results: list[ProbeResult] = []
        errors: list[str] = []
        for url in urls:
            try:
                results.append(self._engine.probe(url))
            except MediaError as exc:
                errors.append(f"{url}: {exc.message}")
        return BatchProbeResult(results=tuple(results), errors=tuple(errors))
