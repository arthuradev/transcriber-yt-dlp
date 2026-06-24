"""Tests for shell action-handler routing."""

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


def test_handled_action_skips_placeholder(console_buffer: tuple[Console, io.StringIO]) -> None:
    console, buffer = console_buffer
    handled: list[MenuAction] = []

    def handler(action: MenuAction) -> bool:
        handled.append(action)
        return True

    shell = AppShell(
        console,
        select_action=_selector([MenuAction.DOWNLOAD_VIDEO, MenuAction.EXIT]),
        animate=False,
        action_handler=handler,
    )
    assert shell.run() == 0
    assert MenuAction.DOWNLOAD_VIDEO in handled
    assert "not implemented" not in buffer.getvalue()


def test_unhandled_action_falls_back_to_placeholder(
    console_buffer: tuple[Console, io.StringIO],
) -> None:
    console, buffer = console_buffer

    def handler(action: MenuAction) -> bool:
        return False

    shell = AppShell(
        console,
        select_action=_selector([MenuAction.SETTINGS, MenuAction.EXIT]),
        animate=False,
        action_handler=handler,
    )
    shell.run()
    assert "not implemented" in buffer.getvalue()
