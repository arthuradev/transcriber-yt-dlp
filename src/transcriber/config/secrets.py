"""Secret lookup from the environment.

Secrets (API keys) live in the environment / ``.env`` and never in the persisted
config (see ADR 0013). These helpers centralize the environment variable names.
Returned values must never be logged.
"""

from __future__ import annotations

import os


def weather_api_key() -> str | None:
    """Return the WeatherAPI key from the environment, or ``None`` if unset."""
    return os.environ.get("WEATHERAPI_KEY") or None
