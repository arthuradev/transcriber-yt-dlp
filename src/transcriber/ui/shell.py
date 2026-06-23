"""Application TUI shell.

Owns the startup sequence and the main-menu loop. It is pure presentation:
non-exit actions render a placeholder until later phases wire real use cases.
The action selector is injectable so the loop can be driven in tests without a
terminal.
"""

from __future__ import annotations

from collections.abc import Callable

from rich.console import Console
from rich.panel import Panel

from transcriber.ui.animation import play_startup_animation
from transcriber.ui.ascii_art import AsciiArt, fits, render_art
from transcriber.ui.banner import render_banner
from transcriber.ui.console import build_console
from transcriber.ui.menu import MenuAction, label_for, prompt_main_menu
from transcriber.ui.screens import clear_screen
from transcriber.ui.theme import DEFAULT_THEME_NAME

SelectAction = Callable[[], MenuAction]

WELCOME_ART_MIN_WIDTH = 110


class AppShell:
    """Drives startup and the interactive main-menu loop."""

    def __init__(
        self,
        console: Console | None = None,
        *,
        select_action: SelectAction = prompt_main_menu,
        animate: bool | None = None,
        theme_name: str = DEFAULT_THEME_NAME,
        welcome_art: AsciiArt | None = None,
    ) -> None:
        self.console = console if console is not None else build_console(theme_name)
        self._select_action = select_action
        self._animate = animate
        self._welcome_art = welcome_art

    def run(self) -> int:
        """Run the main loop until the user exits. Returns a process exit code."""
        animate = self.console.is_terminal if self._animate is None else self._animate
        self._render_header(animate=animate, welcome=True)
        while True:
            action = self._select_action()
            if action is MenuAction.EXIT:
                self._render_goodbye()
                return 0
            self._render_placeholder(action)
            self._render_header(animate=False, welcome=False)

    def _render_header(self, *, animate: bool, welcome: bool) -> None:
        clear_screen(self.console)
        play_startup_animation(self.console, enabled=animate)
        render_banner(self.console)
        if (
            welcome
            and self._welcome_art is not None
            and fits(self._welcome_art, self.console.width, min_width=WELCOME_ART_MIN_WIDTH)
        ):
            render_art(self.console, self._welcome_art)

    def _render_placeholder(self, action: MenuAction) -> None:
        message = f"'{label_for(action)}' is not implemented yet (coming in a later phase)."
        self.console.print(Panel(message, title="Coming soon", border_style="warning"))
        if self.console.is_terminal:
            self.console.input("[muted]Press Enter to return to the menu[/muted] ")

    def _render_goodbye(self) -> None:
        self.console.print("[success]Goodbye.[/success]")
