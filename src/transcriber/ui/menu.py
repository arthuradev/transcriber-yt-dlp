"""Main menu definition and Questionary prompt.

The menu is presentation data only: it lists the available actions (localized via
the translator) and returns the one the user picked. Deciding what each action
*does* is the application layer's job in later phases.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import questionary

from transcriber.ui.i18n import Translator


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
    """A single menu entry pairing an action with its (localized) label."""

    action: MenuAction
    label: str


# Display order of the menu, ending with Exit.
MENU_ORDER: tuple[MenuAction, ...] = (
    MenuAction.DOWNLOAD_VIDEO,
    MenuAction.DOWNLOAD_AUDIO,
    MenuAction.DOWNLOAD_TRANSCRIPT,
    MenuAction.TRANSCRIBE_LOCAL,
    MenuAction.CLEAN_TRANSCRIPT,
    MenuAction.HISTORY,
    MenuAction.SETTINGS,
    MenuAction.EXIT,
)


def label_for(action: MenuAction, translator: Translator) -> str:
    """Return the localized display label for ``action``."""
    return translator(f"menu.{action.value}")


def build_menu_items(translator: Translator) -> list[MenuItem]:
    """Build the localized menu items in display order."""
    return [MenuItem(action, label_for(action, translator)) for action in MENU_ORDER]


def prompt_main_menu(translator: Translator) -> MenuAction:
    """Prompt the user to choose a main-menu action.

    Returns :data:`MenuAction.EXIT` if the prompt is cancelled (Ctrl-C / Esc).
    """
    choices = [
        questionary.Choice(title=item.label, value=item.action)
        for item in build_menu_items(translator)
    ]
    answer: MenuAction | None = questionary.select(translator("menu.prompt"), choices=choices).ask()
    if answer is None:
        return MenuAction.EXIT
    return answer
