"""Tests for the TUI shell loop."""

from __future__ import annotations

import io
from collections.abc import Callable

from rich.console import Console

from transcriber.ui.menu import MenuAction
from transcriber.ui.shell import AppShell


def _selector(actions: list[MenuAction]) -> Callable[[], MenuAction]:
    sequence = iter(actions)

    def select() -> MenuAction:
        return next(sequence)

    return select


def test_shell_exits_immediately(console_buffer: tuple[Console, io.StringIO]) -> None:
    console, buffer = console_buffer
    shell = AppShell(console, select_action=_selector([MenuAction.EXIT]), animate=False)
    assert shell.run() == 0
    assert "Goodbye" in buffer.getvalue()


def test_shell_renders_placeholder_then_exits(
    console_buffer: tuple[Console, io.StringIO],
) -> None:
    console, buffer = console_buffer
    shell = AppShell(
        console,
        select_action=_selector([MenuAction.SETTINGS, MenuAction.EXIT]),
        animate=False,
    )
    assert shell.run() == 0
    output = buffer.getvalue()
    assert "not implemented" in output
    assert "Goodbye" in output
