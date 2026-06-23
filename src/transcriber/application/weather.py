"""Weather use case.

Wraps a ``WeatherPort`` with a time-to-live cache (to avoid unnecessary API
calls) and graceful degradation: any ``WeatherError`` becomes ``None`` so weather
never blocks or breaks the app. The clock is injectable for tests.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass

from transcriber.core.weather import WeatherError, WeatherSnapshot
from transcriber.ports.weather import WeatherPort


@dataclass
class _CacheEntry:
    fetched_at: float
    query: str
    units: str
    snapshot: WeatherSnapshot


class WeatherService:
    """Fetches weather with caching and graceful failure handling."""

    def __init__(
        self,
        port: WeatherPort,
        *,
        cache_minutes: int,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self._port = port
        self._ttl_seconds = max(cache_minutes, 0) * 60.0
        self._clock = clock
        self._cache: _CacheEntry | None = None

    def get(self, query: str, units: str) -> WeatherSnapshot | None:
        """Return the current weather, or ``None`` if it cannot be fetched."""
        now = self._clock()
        cached = self._cache
        if (
            cached is not None
            and cached.query == query
            and cached.units == units
            and (now - cached.fetched_at) < self._ttl_seconds
        ):
            return cached.snapshot

        try:
            snapshot = self._port.fetch(query, units)
        except WeatherError:
            return None

        self._cache = _CacheEntry(fetched_at=now, query=query, units=units, snapshot=snapshot)
        return snapshot
