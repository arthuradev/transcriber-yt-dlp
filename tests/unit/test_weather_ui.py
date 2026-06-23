"""Tests for weather display formatting and shell integration."""

from __future__ import annotations

import io
from collections.abc import Callable

from rich.console import Console

from transcriber.config.models import Language
from transcriber.core.weather import WeatherSnapshot
from transcriber.ui.i18n import Translator
from transcriber.ui.menu import MenuAction
from transcriber.ui.shell import AppShell
from transcriber.ui.weather import format_weather, render_weather_line


def _snapshot() -> WeatherSnapshot:
    return WeatherSnapshot(
        location="London",
        temperature=21.4,
        unit="C",
        condition="Cloudy",
        local_time="2026-06-23 14:30",
    )


def _exit_selector() -> Callable[[], MenuAction]:
    actions = iter([MenuAction.EXIT])

    def select() -> MenuAction:
        return next(actions)

    return select


def test_format_weather_includes_all_fields() -> None:
    text = format_weather(_snapshot())
    assert "London" in text
    assert "21°C" in text
    assert "Cloudy" in text
    assert "2026-06-23 14:30" in text


def test_render_weather_line_with_snapshot() -> None:
    line = render_weather_line(_snapshot(), Translator(Language.EN_US))
    assert "London" in line
    assert "[info]" in line


def test_render_weather_line_unavailable_is_localized() -> None:
    assert "Weather unavailable" in render_weather_line(None, Translator(Language.EN_US))
    assert "Clima indisponível" in render_weather_line(None, Translator(Language.PT_BR))


def test_shell_renders_weather_line(console_buffer: tuple[Console, io.StringIO]) -> None:
    console, buffer = console_buffer
    shell = AppShell(
        console,
        select_action=_exit_selector(),
        animate=False,
        weather_line_provider=lambda: "London weather",
    )
    shell.run()
    assert "London weather" in buffer.getvalue()
