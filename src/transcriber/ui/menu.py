"""Main menu definition and Questionary prompt.

The menu is presentation data only: it lists the available actions and returns
the one the user picked. Deciding what each action *does* is the application
layer's job in later phases.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import questionary


class MenuAction(Enum):
    """Selectable actions on the main menu."""

    DOWNLOAD_VIDEO = "download_video"
    DOWNLOAD_AUDIO = "download_audio"
    DOWNLOAD_TRANSCRIPT = "download_transcript"
    TRANSCRIBE_LOCAL = "transcribe_local"
    CLEAN_TRANSCRIPT = "clean_transcript"
    HISTORY = "history"
    SETTINGS = "settings"
    EXIT = "exit"


@dataclass(frozen=True)
class MenuItem:
    """A single menu entry pairing an action with its display label."""

    action: MenuAction
    label: str


MAIN_MENU: tuple[MenuItem, ...] = (
    MenuItem(MenuAction.DOWNLOAD_VIDEO, "Download video"),
    MenuItem(MenuAction.DOWNLOAD_AUDIO, "Download audio"),
    MenuItem(MenuAction.DOWNLOAD_TRANSCRIPT, "Download transcript / subtitles"),
    MenuItem(MenuAction.TRANSCRIBE_LOCAL, "Transcribe local file"),
    MenuItem(MenuAction.CLEAN_TRANSCRIPT, "Clean transcript with AI"),
    MenuItem(MenuAction.HISTORY, "History"),
    MenuItem(MenuAction.SETTINGS, "Settings"),
    MenuItem(MenuAction.EXIT, "Exit"),
)


def label_for(action: MenuAction) -> str:
    """Return the display label for ``action``."""
    for item in MAIN_MENU:
        if item.action is action:
            return item.label
    return action.value


def prompt_main_menu(message: str = "Select an option:") -> MenuAction:
    """Prompt the user to choose a main-menu action.

    Returns :data:`MenuAction.EXIT` if the prompt is cancelled (Ctrl-C / Esc).
    """
    choices = [questionary.Choice(title=item.label, value=item.action) for item in MAIN_MENU]
    answer: MenuAction | None = questionary.select(message, choices=choices).ask()
    if answer is None:
        return MenuAction.EXIT
    return answer
