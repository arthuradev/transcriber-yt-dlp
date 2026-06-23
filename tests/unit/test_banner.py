"""Tests for the startup banner."""

from __future__ import annotations

import io

from rich.console import Console

from transcriber.ui.banner import DEFAULT_SUBTITLE, render_banner, render_figlet


def test_render_figlet_is_multiline_ascii_art() -> None:
    art = render_figlet("Transcriber")
    assert art.strip() != ""
    assert "\n" in art


def test_render_figlet_unknown_font_falls_back() -> None:
    art = render_figlet("Hi", font="font-that-does-not-exist")
    assert art.strip() != ""


def test_render_banner_includes_subtitle(console_buffer: tuple[Console, io.StringIO]) -> None:
    console, buffer = console_buffer
    render_banner(console)
    assert DEFAULT_SUBTITLE in buffer.getvalue()
