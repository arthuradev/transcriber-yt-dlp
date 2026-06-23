"""Port for fetching weather snapshots."""

from __future__ import annotations

from typing import Protocol

from transcriber.core.weather import WeatherSnapshot


class WeatherPort(Protocol):
    """Contract for a weather provider."""

    def fetch(self, query: str, units: str) -> WeatherSnapshot:
        """Fetch the current weather for ``query`` in the given ``units``.

        ``units`` is ``"metric"`` or ``"imperial"``. Raises ``WeatherError`` on
        any failure.
        """
        ...
