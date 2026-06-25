"""Settings screen: view and edit theme/language, persisted to config.

Theme/language changes are saved immediately but apply on the next launch (the
console and translator are built at startup). No architecture change: this is a
UI controller over the existing config repository.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

import questionary
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from transcriber.config.models import Language, UserConfig
from transcriber.ports.config_repository import ConfigRepository
from transcriber.ui.i18n import Translator


class SettingsFlowPrompts(Protocol):
    """Prompts the settings flow needs."""

    def choose_action(self) -> str | None: ...
    def select_theme(self, themes: Sequence[str]) -> str | None: ...
    def select_language(self) -> Language | None: ...


class QuestionarySettingsFlowPrompts:
    """Questionary-backed prompts for the settings flow."""

    def __init__(self, translator: Translator) -> None:
        self._t = translator

    def choose_action(self) -> str | None:
        choices = [
            questionary.Choice(title=self._t("settings.change_theme"), value="theme"),
            questionary.Choice(title=self._t("settings.change_language"), value="language"),
            questionary.Choice(title=self._t("settings.back"), value=None),
        ]
        answer: str | None = questionary.select(self._t("settings.prompt"), choices=choices).ask()
        return answer

    def select_theme(self, themes: Sequence[str]) -> str | None:
        choices = [questionary.Choice(title=name, value=name) for name in themes]
        answer: str | None = questionary.select(self._t("settings.theme"), choices=choices).ask()
        return answer

    def select_language(self) -> Language | None:
        choices = [
            questionary.Choice(title="Português", value=Language.PT_BR.value),
            questionary.Choice(title="English", value=Language.EN_US.value),
        ]
        answer: str | None = questionary.select(self._t("settings.language"), choices=choices).ask()
        return Language(answer) if answer is not None else None


class SettingsFlow:
    """Shows current settings and lets the user change theme/language."""

    def __init__(
        self,
        *,
        config: UserConfig,
        store: ConfigRepository,
        console: Console,
        translator: Translator,
        themes: Sequence[str],
        prompts: SettingsFlowPrompts,
    ) -> None:
        self._config = config
        self._store = store
        self._console = console
        self._t = translator
        self._themes = themes
        self._prompts = prompts

    def run(self) -> None:
        self._render_settings()
        action = self._prompts.choose_action()
        if action == "theme":
            theme = self._prompts.select_theme(self._themes)
            if theme is not None:
                new_ui = self._config.ui.model_copy(update={"theme": theme})
                self._save(self._config.model_copy(update={"ui": new_ui}))
        elif action == "language":
            language = self._prompts.select_language()
            if language is not None:
                self._save(self._config.model_copy(update={"language": language}))
        self._pause()

    def _render_settings(self) -> None:
        on, off = self._t("common.on"), self._t("common.off")
        table = Table(show_header=False, box=None)
        table.add_column(style="muted")
        table.add_column(style="info")
        table.add_row(self._t("settings.theme"), self._config.ui.theme)
        table.add_row(self._t("settings.language"), self._config.language.value)
        table.add_row(self._t("settings.weather"), on if self._config.weather.enabled else off)
        table.add_row(self._t("settings.llm"), on if self._config.llm.enabled else off)
        table.add_row(self._t("settings.output"), self._config.paths.download_dir)
        self._console.print(Panel(table, title=self._t("settings.title"), border_style="accent"))

    def _save(self, config: UserConfig) -> None:
        self._store.save(config)
        self._config = config
        self._console.print(f"[success]{self._t('settings.saved')}[/success]")

    def _pause(self) -> None:
        if self._console.is_terminal:
            self._console.input(f"[muted]{self._t('shell.press_enter')}[/muted] ")
