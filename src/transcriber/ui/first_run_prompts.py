"""Questionary-backed first-run prompts (implements the FirstRunPrompts port)."""

from __future__ import annotations

from collections.abc import Sequence

import questionary

from transcriber.config.models import Language
from transcriber.ui.i18n import Translator

_LANGUAGE_PROMPT = "Choose your language / Escolha seu idioma:"


class QuestionaryFirstRunPrompts:
    """Collects first-run answers via keyboard prompts."""

    def __init__(self) -> None:
        # Localized once the language is chosen.
        self._translator = Translator()

    def ask_language(self) -> Language:
        choices = [
            questionary.Choice(title="Português", value=Language.PT_BR.value),
            questionary.Choice(title="English", value=Language.EN_US.value),
        ]
        answer: str | None = questionary.select(_LANGUAGE_PROMPT, choices=choices).ask()
        language = Language(answer) if answer is not None else Language.EN_US
        self._translator = Translator(language)
        return language

    def ask_theme(self, available: Sequence[str]) -> str:
        choices = [questionary.Choice(title=name, value=name) for name in available]
        answer: str | None = questionary.select(
            self._translator("firstrun.choose_theme"), choices=choices
        ).ask()
        if answer is not None:
            return answer
        return available[0] if available else "default"

    def ask_weather_enabled(self) -> bool:
        return bool(questionary.confirm(self._translator("firstrun.weather_enable")).ask())

    def ask_city(self) -> str:
        answer: str | None = questionary.text(self._translator("firstrun.weather_city")).ask()
        return answer or ""

    def ask_download_dir(self, default: str) -> str:
        answer: str | None = questionary.text(
            self._translator("firstrun.output_dir"), default=default
        ).ask()
        return answer or default

    def ask_llm_enabled(self) -> bool:
        return bool(questionary.confirm(self._translator("firstrun.llm_enable")).ask())

    def acknowledge_gpu_only(self) -> bool:
        return bool(questionary.confirm(self._translator("firstrun.gpu_ack"), default=True).ask())
