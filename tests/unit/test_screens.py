"""Tests for the clean-screen success flow."""

from __future__ import annotations

import io

from rich.console import Console

from transcriber.ui.ascii_art import AsciiArt
from transcriber.ui.screens import SuccessScreenSettings, clear_screen, show_success_screen


def _art(width: int) -> AsciiArt:
    return AsciiArt(name="art", lines=("#" * width,))


def test_clear_screen_is_noop_on_non_terminal(
    console_buffer: tuple[Console, io.StringIO],
) -> None:
    console, buffer = console_buffer
    clear_screen(console)
    assert buffer.getvalue() == ""


def test_success_screen_shows_summary_and_holds(
    console_buffer: tuple[Console, io.StringIO],
) -> None:
    console, buffer = console_buffer
    slept: list[float] = []
    show_success_screen(console, "Done: 1 file", sleep=slept.append)
    assert "Done: 1 file" in buffer.getvalue()
    assert slept == [3.0]


def test_success_screen_renders_fitting_art(
    console_buffer: tuple[Console, io.StringIO],
) -> None:
    console, buffer = console_buffer  # width 100
    settings = SuccessScreenSettings(art_min_width=10)
    show_success_screen(console, "ok", art=_art(50), settings=settings, sleep=lambda _s: None)
    assert "#" * 50 in buffer.getvalue()


def test_success_screen_hides_art_when_terminal_too_small(
    console_buffer: tuple[Console, io.StringIO],
) -> None:
    console, buffer = console_buffer  # width 100, default art_min_width 110
    show_success_screen(console, "ok", art=_art(50), sleep=lambda _s: None)
    output = buffer.getvalue()
    assert "art hidden" in output
    assert "#" * 50 not in output
