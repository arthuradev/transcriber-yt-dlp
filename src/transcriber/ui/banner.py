"""Startup banner rendering: Pyfiglet logo plus subtitle."""

from __future__ import annotations

from pyfiglet import figlet_format
from rich.align import Align
from rich.console import Console
from rich.text import Text

DEFAULT_FONT = "bloody"
DEFAULT_TITLE = "Transcriber"
DEFAULT_SUBTITLE = "Download • Transcription • Cleanup"


def render_figlet(text: str, font: str = DEFAULT_FONT) -> str:
    """Render ``text`` as Pyfiglet ASCII art using ``font``.

    Falls back to the bundled ``standard`` font if ``font`` is unavailable so a
    bad font name never crashes startup.
    """
    try:
        art = figlet_format(text, font=font)
    except Exception:
        art = figlet_format(text, font="standard")
    return art.rstrip("\n")


def render_banner(
    console: Console,
    *,
    title: str = DEFAULT_TITLE,
    subtitle: str = DEFAULT_SUBTITLE,
    font: str = DEFAULT_FONT,
) -> None:
    """Render the centered startup logo and subtitle to ``console``."""
    art = render_figlet(title, font=font)
    console.print(Align.center(Text(art, style="banner")))
    console.print(Align.center(Text(subtitle, style="subtitle")))
