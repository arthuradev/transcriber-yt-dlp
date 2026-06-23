"""Tests for the first-run setup service.

Uses an in-memory repository and a scripted prompts object (both structurally
satisfy their ports) so the flow runs without a terminal or filesystem.
"""

from __future__ import annotations

from collections.abc import Sequence

from transcriber.application.first_run import FirstRunService
from transcriber.config.models import Language, UserConfig


class _FakeRepo:
    def __init__(self) -> None:
        self.saved: UserConfig | None = None

    def exists(self) -> bool:
        return self.saved is not None

    def load(self) -> UserConfig:
        assert self.saved is not None
        return self.saved

    def save(self, config: UserConfig) -> None:
        self.saved = config


class _ScriptedPrompts:
    def __init__(
        self,
        *,
        language: Language = Language.PT_BR,
        theme: str = "blue",
        weather: bool = True,
        city: str = "Lisbon",
        download_dir: str = "out",
        llm: bool = True,
        gpu: bool = True,
    ) -> None:
        self._language = language
        self._theme = theme
        self._weather = weather
        self._city = city
        self._download_dir = download_dir
        self._llm = llm
        self._gpu = gpu
        self.offered_themes: list[str] = []

    def ask_language(self) -> Language:
        return self._language

    def ask_theme(self, available: Sequence[str]) -> str:
        self.offered_themes = list(available)
        return self._theme

    def ask_weather_enabled(self) -> bool:
        return self._weather

    def ask_city(self) -> str:
        return self._city

    def ask_download_dir(self, default: str) -> str:
        return self._download_dir

    def ask_llm_enabled(self) -> bool:
        return self._llm

    def acknowledge_gpu_only(self) -> bool:
        return self._gpu


def test_is_first_run_true_for_empty_repo() -> None:
    assert FirstRunService(_FakeRepo()).is_first_run()


def test_setup_builds_persists_and_returns_config() -> None:
    repo = _FakeRepo()
    prompts = _ScriptedPrompts()
    config = FirstRunService(repo).setup(prompts, themes=["default", "blue"])

    assert config.language is Language.PT_BR
    assert config.ui.theme == "blue"
    assert config.weather.enabled is True
    assert config.weather.query == "Lisbon"
    assert config.paths.download_dir == "out"
    assert config.llm.enabled is True
    assert config.gpu.acknowledged_gpu_only is True
    assert repo.saved == config
    assert prompts.offered_themes == ["default", "blue"]


def test_setup_skips_city_when_weather_disabled() -> None:
    prompts = _ScriptedPrompts(weather=False, city="ShouldBeIgnored")
    config = FirstRunService(_FakeRepo()).setup(prompts, themes=["default"])
    assert config.weather.enabled is False
    assert config.weather.query == ""


def test_not_first_run_after_setup() -> None:
    repo = _FakeRepo()
    FirstRunService(repo).setup(_ScriptedPrompts(), themes=["default"])
    assert not FirstRunService(repo).is_first_run()
