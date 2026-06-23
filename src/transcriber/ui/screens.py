"""Clean-screen flow and the post-operation success screen.

The success screen renders a summary plus optional success art, enforces a
minimum on-screen time, then waits for Enter before the caller clears and
returns to the menu. Time and input are injectable/guarded so the flow can be
driven in tests without sleeping or blocking.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass

from rich.console import Console
from rich.panel import Panel

from transcriber.ui.ascii_art import AsciiArt, fits, render_art


@dataclass(frozen=True)
class SuccessScreenSettings:
    """Tunables for the success screen (defaults mirror ascii.example.yaml)."""

    min_display_seconds: float = 3.0
    wait_for_enter: bool = True
    show_art: bool = True
    art_min_width: int = 110


def clear_screen(console: Console) -> None:
    """Clear the screen on a real terminal; a no-op otherwise."""
    if console.is_terminal:
        console.clear()


def show_success_screen(
    console: Console,
    summary: str,
    *,
    art: AsciiArt | None = None,
    settings: SuccessScreenSettings | None = None,
    sleep: Callable[[float], None] = time.sleep,
) -> None:
    """Render the success summary and art, hold, then wait for Enter."""
    settings = settings if settings is not None else SuccessScreenSettings()
    console.print(Panel(summary, title="Success", border_style="success"))

    if settings.show_art and art is not None:
        if fits(art, console.width, min_width=settings.art_min_width):
            render_art(console, art)
        else:
            console.print(f"[muted]({art.name} art hidden: terminal too small)[/muted]")

    if settings.min_display_seconds > 0:
        sleep(settings.min_display_seconds)
    if settings.wait_for_enter and console.is_terminal:
        console.input("[muted]Press Enter to return to the menu[/muted] ")
