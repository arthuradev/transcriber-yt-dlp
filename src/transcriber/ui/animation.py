"""Startup animation.

The animation is always enabled by design but only plays on a real terminal;
on captured/non-interactive streams (tests, pipes) it is a no-op so nothing
blocks and no control characters leak into output.
"""

from __future__ import annotations

import time

from rich.console import Console

_SPINNER_FRAMES = ("|", "/", "-", "\\")


def play_startup_animation(
    console: Console,
    *,
    enabled: bool = True,
    cycles: int = 3,
    frame_delay: float = 0.07,
) -> None:
    """Play a short spinner animation, then clear the line.

    Does nothing when ``enabled`` is ``False`` or the console is not a terminal.
    """
    if not enabled or not console.is_terminal:
        return
    for _ in range(cycles):
        for frame in _SPINNER_FRAMES:
            console.print(f"[accent]{frame}[/accent] [muted]starting...[/muted]", end="\r")
            time.sleep(frame_delay)
    console.print(" " * 16, end="\r")
