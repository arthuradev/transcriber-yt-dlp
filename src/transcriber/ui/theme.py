"""Default UI theme.

Phase 2 ships a single dark palette. The full selectable theme system (purple,
red, blue, monochrome, anime) arrives in Phase 3; the named styles here are the
stable contract those themes will later override.
"""

from __future__ import annotations

from rich.theme import Theme

DEFAULT_THEME = Theme(
    {
        "banner": "bold magenta",
        "subtitle": "dim cyan",
        "accent": "magenta",
        "menu.title": "bold white",
        "menu.item": "white",
        "info": "cyan",
        "warning": "yellow",
        "error": "bold red",
        "success": "bold green",
        "muted": "dim white",
    }
)
