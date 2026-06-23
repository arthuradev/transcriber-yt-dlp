"""Tests for the theme registry."""

from __future__ import annotations

from transcriber.ui.theme import (
    DEFAULT_THEME_NAME,
    STYLE_KEYS,
    available_themes,
    get_theme,
)


def test_expected_themes_are_registered() -> None:
    assert set(available_themes()) == {
        "default",
        "purple",
        "red",
        "blue",
        "monochrome",
        "anime",
    }


def test_every_theme_defines_all_style_keys() -> None:
    for name in available_themes():
        theme = get_theme(name)
        for key in STYLE_KEYS:
            assert key in theme.styles, f"theme '{name}' is missing style '{key}'"


def test_unknown_theme_falls_back_to_default() -> None:
    assert (
        get_theme("does-not-exist").styles["banner"]
        == get_theme(DEFAULT_THEME_NAME).styles["banner"]
    )
