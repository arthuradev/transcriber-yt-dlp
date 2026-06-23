"""Shared Rich console factory."""

from __future__ import annotations

from rich.console import Console

from transcriber.ui.theme import DEFAULT_THEME_NAME, get_theme


def build_console(theme_name: str = DEFAULT_THEME_NAME) -> Console:
    """Build the application console using the named dark theme."""
    return Console(theme=get_theme(theme_name))
