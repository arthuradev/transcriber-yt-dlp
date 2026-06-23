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
from transcriber.ui.i18n import Translator
from transcriber.ui.menu import MenuAction, label_for, prompt_main_menu
from transcriber.ui.screens import clear_screen
from transcriber.ui.theme import DEFAULT_THEME_NAME

SelectAction = Callable[[], MenuAction]
WeatherLineProvider = Callable[[], str | None]

WELCOME_ART_MIN_WIDTH = 110


class AppShell:
    """Drives startup and the interactive main-menu loop."""

    def __init__(
        self,
        console: Console | None = None,
        *,
        select_action: SelectAction | None = None,
        animate: bool | None = None,
        theme_name: str = DEFAULT_THEME_NAME,
        translator: Translator | None = None,
        welcome_art: AsciiArt | None = None,
        weather_line_provider: WeatherLineProvider | None = None,
    ) -> None:
        self.console = console if console is not None else build_console(theme_name)
        self._translator = translator if translator is not None else Translator()
        self._select_action = select_action if select_action is not None else self._default_select
        self._animate = animate
        self._welcome_art = welcome_art
        self._weather_line_provider = weather_line_provider

    def _default_select(self) -> MenuAction:
        return prompt_main_menu(self._translator)

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
        if self._weather_line_provider is not None:
            line = self._weather_line_provider()
            if line:
                self.console.print(line)

    def _render_placeholder(self, action: MenuAction) -> None:
        message = self._translator(
            "shell.not_implemented", label=label_for(action, self._translator)
        )
        title = self._translator("shell.coming_soon_title")
        self.console.print(Panel(message, title=title, border_style="warning"))
        if self.console.is_terminal:
            self.console.input(f"[muted]{self._translator('shell.press_enter')}[/muted] ")

    def _render_goodbye(self) -> None:
        self.console.print(f"[success]{self._translator('shell.goodbye')}[/success]")
