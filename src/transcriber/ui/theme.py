"""UI theme registry.

All themes are dark and share the same style keys, so any theme can be swapped
in without the rest of the UI knowing which one is active. Themes differ only in
their accent/banner colors; status colors (info/warning/error/success) stay
readable across every theme.
"""

from __future__ import annotations

from rich.theme import Theme

DEFAULT_THEME_NAME = "default"

# The stable set of style names the UI renders against.
STYLE_KEYS: tuple[str, ...] = (
    "banner",
    "subtitle",
    "accent",
    "menu.title",
    "menu.item",
    "info",
    "warning",
    "error",
    "success",
    "muted",
)

_PALETTES: dict[str, dict[str, str]] = {
    "default": {
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
    },
    "purple": {
        "banner": "bold #b48ead",
        "subtitle": "dim #b48ead",
        "accent": "#b48ead",
        "menu.title": "bold white",
        "menu.item": "white",
        "info": "#c8a2e0",
        "warning": "yellow",
        "error": "bold red",
        "success": "bold green",
        "muted": "dim white",
    },
    "red": {
        "banner": "bold #e06c75",
        "subtitle": "dim #e06c75",
        "accent": "#e06c75",
        "menu.title": "bold white",
        "menu.item": "white",
        "info": "#ff8787",
        "warning": "yellow",
        "error": "bold red",
        "success": "bold green",
        "muted": "dim white",
    },
    "blue": {
        "banner": "bold #61afef",
        "subtitle": "dim #61afef",
        "accent": "#61afef",
        "menu.title": "bold white",
        "menu.item": "white",
        "info": "#56b6c2",
        "warning": "yellow",
        "error": "bold red",
        "success": "bold green",
        "muted": "dim white",
    },
    "monochrome": {
        "banner": "bold #ffffff",
        "subtitle": "dim #a0a0a0",
        "accent": "#d0d0d0",
        "menu.title": "bold #ffffff",
        "menu.item": "#d0d0d0",
        "info": "#a0a0a0",
        "warning": "#d0d0d0",
        "error": "bold #ffffff",
        "success": "bold #ffffff",
        "muted": "#808080",
    },
    "anime": {
        "banner": "bold #ff79c6",
        "subtitle": "dim #bd93f9",
        "accent": "#ff79c6",
        "menu.title": "bold #ffb8d1",
        "menu.item": "#f8f8f2",
        "info": "#8be9fd",
        "warning": "#f1fa8c",
        "error": "bold #ff5555",
        "success": "bold #50fa7b",
        "muted": "#6272a4",
    },
}


def available_themes() -> tuple[str, ...]:
    """Return the names of all registered themes."""
    return tuple(_PALETTES)


def get_theme(name: str = DEFAULT_THEME_NAME) -> Theme:
    """Return the Rich theme for ``name``, falling back to the default."""
    palette = _PALETTES.get(name, _PALETTES[DEFAULT_THEME_NAME])
    return Theme(palette)


# Backwards-compatible default used by the console factory and tests.
DEFAULT_THEME = get_theme()
