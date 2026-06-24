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


def llm_api_key() -> str | None:
    """Return the LLM provider key (DeepSeek or OpenAI-compatible), or ``None``."""
    return os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("OPENAI_COMPATIBLE_API_KEY") or None
