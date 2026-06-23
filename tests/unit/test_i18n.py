"""Tests for the translator."""

from __future__ import annotations

from transcriber.config.models import Language
from transcriber.ui.i18n import Translator


def test_translates_known_key_per_language() -> None:
    assert Translator(Language.EN_US)("menu.settings") == "Settings"
    assert Translator(Language.PT_BR)("menu.settings") == "Configurações"


def test_unknown_key_returns_the_key() -> None:
    assert Translator()("does.not.exist") == "does.not.exist"


def test_formats_keyword_arguments() -> None:
    message = Translator(Language.EN_US)("shell.not_implemented", label="History")
    assert "History" in message
