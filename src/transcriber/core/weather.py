"""Weather domain model.

Pure data describing a weather snapshot, plus the domain error raised when a
snapshot cannot be obtained. No I/O, no network, no API client here.
"""

from __future__ import annotations

from dataclasses import dataclass

from transcriber.core.errors import AppError, ErrorSeverity


@dataclass(frozen=True)
class WeatherSnapshot:
    """A point-in-time weather reading for a location."""

    location: str
    temperature: float
    unit: str  # "C" or "F"
    condition: str
    local_time: str


class WeatherError(AppError):
    """Raised when a weather snapshot cannot be fetched.

    Weather is cosmetic; callers are expected to degrade gracefully rather than
    propagate this to the user as a failure.
    """

    def __init__(self, message: str, *, detail: str | None = None) -> None:
        super().__init__(
            "E_WEATHER",
            message,
            severity=ErrorSeverity.WARNING,
            detail=detail,
            recovery="Check the WEATHERAPI_KEY, the city/query, and your internet connection.",
        )
