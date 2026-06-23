"""Tests for the main-menu definition."""

from __future__ import annotations

from transcriber.ui.menu import MAIN_MENU, MenuAction, label_for


def test_main_menu_covers_all_actions_uniquely() -> None:
    actions = [item.action for item in MAIN_MENU]
    assert len(actions) == len(MenuAction)
    assert len(actions) == len(set(actions))


def test_exit_is_the_last_item() -> None:
    assert MAIN_MENU[-1].action is MenuAction.EXIT


def test_every_item_has_a_label() -> None:
    assert all(item.label.strip() for item in MAIN_MENU)


def test_label_for_returns_display_label() -> None:
    assert label_for(MenuAction.SETTINGS) == "Settings"
