"""Tests for YAML config persistence."""

from __future__ import annotations

from pathlib import Path

from transcriber.config.models import Language, PathsConfig, UIConfig, UserConfig
from transcriber.storage.config_store import ConfigStore, default_config_path


def test_default_config_path_is_under_transcriber() -> None:
    path = default_config_path()
    assert path.name == "config.yaml"
    assert path.parent.name == "Transcriber"


def test_save_creates_parents_and_round_trips(tmp_path: Path) -> None:
    store = ConfigStore(tmp_path / "nested" / "config.yaml")
    assert not store.exists()

    config = UserConfig(
        language=Language.PT_BR,
        ui=UIConfig(theme="anime"),
        paths=PathsConfig(download_dir="vids"),
    )
    store.save(config)

    assert store.exists()
    loaded = store.load()
    assert loaded == config
    assert loaded.language is Language.PT_BR
    assert loaded.ui.theme == "anime"


def test_saved_config_contains_no_secret_fields(tmp_path: Path) -> None:
    path = tmp_path / "config.yaml"
    ConfigStore(path).save(UserConfig())
    text = path.read_text(encoding="utf-8").lower()
    for secret_marker in ("api_key", "apikey", "token", "secret", "password"):
        assert secret_marker not in text
