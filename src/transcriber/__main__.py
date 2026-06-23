"""Application entry point.

Launches the TUI shell (startup banner, animation, and main menu). Menu actions
are placeholders until later phases wire the real download/transcription/cleanup
use cases.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from transcriber.config.models import UserConfig
    from transcriber.ui.i18n import Translator


def _build_weather_line_provider(
    config: UserConfig, translator: Translator
) -> Callable[[], str | None] | None:
    """Build a cached weather-line provider, or ``None`` when weather is off.

    When enabled but the API key is missing, returns a provider that renders the
    discreet "unavailable" warning. Weather never blocks or breaks startup.
    """
    if not (config.weather.enabled and config.weather.show_on_startup):
        return None

    from transcriber.config.secrets import weather_api_key
    from transcriber.ui.weather import render_weather_line

    key = weather_api_key()
    if not key:
        return lambda: render_weather_line(None, translator)

    from transcriber.adapters.weatherapi import WeatherApiAdapter
    from transcriber.application.weather import WeatherService

    service = WeatherService(WeatherApiAdapter(key), cache_minutes=config.weather.cache_minutes)
    query = config.weather.query
    units = config.weather.units
    return lambda: render_weather_line(service.get(query, units), translator)


def main() -> int:
    """Run the application. Returns a process exit code."""
    from transcriber.application.first_run import FirstRunService
    from transcriber.storage.config_store import ConfigStore, default_config_path
    from transcriber.ui.ascii_art import choose_art, load_art_dir, locate_ascii_dir
    from transcriber.ui.first_run_prompts import QuestionaryFirstRunPrompts
    from transcriber.ui.i18n import Translator
    from transcriber.ui.shell import AppShell
    from transcriber.ui.theme import available_themes

    store = ConfigStore(default_config_path())
    first_run = FirstRunService(store)
    if first_run.is_first_run():
        config = first_run.setup(QuestionaryFirstRunPrompts(), themes=available_themes())
    else:
        config = store.load()

    translator = Translator(config.language)
    welcome_dir = locate_ascii_dir("welcome")
    welcome_art = choose_art(load_art_dir(welcome_dir)) if welcome_dir is not None else None
    return AppShell(
        theme_name=config.ui.theme,
        translator=translator,
        welcome_art=welcome_art,
        weather_line_provider=_build_weather_line_provider(config, translator),
    ).run()


if __name__ == "__main__":
    raise SystemExit(main())
