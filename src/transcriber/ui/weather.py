"""Weather display formatting."""

from __future__ import annotations

from transcriber.core.weather import WeatherSnapshot
from transcriber.ui.i18n import Translator


def format_weather(snapshot: WeatherSnapshot) -> str:
    """Format a snapshot as a compact one-line string (no markup)."""
    temperature = f"{snapshot.temperature:.0f}°{snapshot.unit}"
    return f"{snapshot.location} · {temperature} · {snapshot.condition} · {snapshot.local_time}"


def render_weather_line(snapshot: WeatherSnapshot | None, translator: Translator) -> str:
    """Return a styled weather line, or a discreet warning when unavailable."""
    if snapshot is None:
        return f"[muted]{translator('weather.unavailable')}[/muted]"
    return f"[info]{format_weather(snapshot)}[/info]"
