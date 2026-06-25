"""Tests for the settings flow."""

from __future__ import annotations

import io
from collections.abc import Sequence

from rich.console import Console

from transcriber.config.models import Language, UserConfig
from transcriber.core.health import HealthCheck, HealthReport
from transcriber.ui.i18n import Translator
from transcriber.ui.settings_flow import SettingsFlow


class _Store:
    def __init__(self) -> None:
        self.saved: UserConfig | None = None

    def exists(self) -> bool:
        return True

    def load(self) -> UserConfig:
        return UserConfig()

    def save(self, config: UserConfig) -> None:
        self.saved = config


class _Prompts:
    def __init__(
        self,
        *,
        action: str | None = None,
        theme: str | None = None,
        language: Language | None = None,
    ) -> None:
        self._action = action
        self._theme = theme
        self._language = language

    def choose_action(self) -> str | None:
        return self._action

    def select_theme(self, themes: Sequence[str]) -> str | None:
        return self._theme

    def select_language(self) -> Language | None:
        return self._language


def _flow(console: Console, store: _Store, prompts: _Prompts) -> SettingsFlow:
    return SettingsFlow(
        config=UserConfig(),
        store=store,
        console=console,
        translator=Translator(Language.EN_US),
        themes=("default", "blue", "anime"),
        prompts=prompts,
    )


def test_renders_current_settings(console_buffer: tuple[Console, io.StringIO]) -> None:
    console, buffer = console_buffer
    _flow(console, _Store(), _Prompts(action=None)).run()
    output = buffer.getvalue()
    assert "Settings" in output
    assert "default" in output


def test_change_theme_saves(console_buffer: tuple[Console, io.StringIO]) -> None:
    console, buffer = console_buffer
    store = _Store()
    _flow(console, store, _Prompts(action="theme", theme="blue")).run()
    assert store.saved is not None
    assert store.saved.ui.theme == "blue"
    assert "Saved" in buffer.getvalue()


def test_change_language_saves(console_buffer: tuple[Console, io.StringIO]) -> None:
    console, _ = console_buffer
    store = _Store()
    _flow(console, store, _Prompts(action="language", language=Language.PT_BR)).run()
    assert store.saved is not None
    assert store.saved.language is Language.PT_BR


def test_back_does_not_save(console_buffer: tuple[Console, io.StringIO]) -> None:
    console, _ = console_buffer
    store = _Store()
    _flow(console, store, _Prompts(action=None)).run()
    assert store.saved is None


def test_renders_health_report(console_buffer: tuple[Console, io.StringIO]) -> None:
    console, buffer = console_buffer
    report = HealthReport((HealthCheck("ffmpeg", True, "x"),))
    SettingsFlow(
        config=UserConfig(),
        store=_Store(),
        console=console,
        translator=Translator(Language.EN_US),
        themes=("default",),
        prompts=_Prompts(action=None),
        health_report=report,
    ).run()
    assert "Diagnostics" in buffer.getvalue()
