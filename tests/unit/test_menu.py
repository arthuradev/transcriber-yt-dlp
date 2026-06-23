"""Tests for the main-menu definition."""

from __future__ import annotations

from transcriber.config.models import Language
from transcriber.ui.i18n import Translator
from transcriber.ui.menu import MENU_ORDER, MenuAction, build_menu_items, label_for


def test_menu_order_covers_all_actions_uniquely() -> None:
    assert len(MENU_ORDER) == len(MenuAction)
    assert len(set(MENU_ORDER)) == len(MENU_ORDER)


def test_exit_is_the_last_item() -> None:
    assert MENU_ORDER[-1] is MenuAction.EXIT


def test_build_menu_items_english() -> None:
    items = build_menu_items(Translator(Language.EN_US))
    assert [item.action for item in items] == list(MENU_ORDER)
    assert all(item.label.strip() for item in items)
    assert label_for(MenuAction.SETTINGS, Translator(Language.EN_US)) == "Settings"


def test_build_menu_items_portuguese() -> None:
    labels = {item.action: item.label for item in build_menu_items(Translator(Language.PT_BR))}
    assert labels[MenuAction.SETTINGS] == "Configurações"
    assert labels[MenuAction.EXIT] == "Sair"
