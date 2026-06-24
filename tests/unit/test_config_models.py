"""Tests for the Pydantic user-configuration models."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from transcriber.config.models import Language, PathsConfig, UserConfig, WeatherConfig


def test_defaults_are_safe() -> None:
    config = UserConfig()
    assert config.language is Language.EN_US
    assert config.ui.theme == "default"
    assert config.weather.enabled is False
    assert config.weather.query == ""
    assert config.paths.overwrite_policy == "ask"
    assert config.gpu.acknowledged_gpu_only is False


def test_transcription_defaults() -> None:
    transcription = UserConfig().transcription
    assert transcription.model == "large-v3"
    assert transcription.language == ""
    assert transcription.translate is False
    assert transcription.output_format == "txt"


def test_invalid_units_rejected() -> None:
    with pytest.raises(ValidationError):
        WeatherConfig.model_validate({"units": "kelvin"})


def test_invalid_overwrite_policy_rejected() -> None:
    with pytest.raises(ValidationError):
        PathsConfig.model_validate({"overwrite_policy": "nuke"})


def test_round_trip_through_json_dict() -> None:
    config = UserConfig(language=Language.PT_BR)
    data = config.model_dump(mode="json")
    assert data["language"] == "pt-BR"
    assert UserConfig.model_validate(data) == config
