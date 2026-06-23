"""Tests for the startup animation guards."""

from __future__ import annotations

import io

from rich.console import Console

from transcriber.ui.animation import play_startup_animation


def test_animation_is_noop_when_disabled(console_buffer: tuple[Console, io.StringIO]) -> None:
    console, buffer = console_buffer
    play_startup_animation(console, enabled=False)
    assert buffer.getvalue() == ""


def test_animation_is_noop_on_non_terminal(console_buffer: tuple[Console, io.StringIO]) -> None:
    console, buffer = console_buffer
    play_startup_animation(console, enabled=True)
    assert buffer.getvalue() == ""
