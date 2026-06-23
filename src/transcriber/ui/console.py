"""Shared Rich console factory."""

from __future__ import annotations

from rich.console import Console

from transcriber.ui.theme import DEFAULT_THEME


def build_console() -> Console:
    """Build the application console with the default dark theme."""
    return Console(theme=DEFAULT_THEME)
