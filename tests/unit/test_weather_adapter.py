"""Tests for the WeatherAPI adapter."""

from __future__ import annotations

import json
from collections.abc import Callable

import pytest

from transcriber.adapters.weatherapi import WeatherApiAdapter
from transcriber.core.weather import WeatherError

_SAMPLE = {
    "location": {"name": "London", "localtime": "2026-06-23 14:30"},
    "current": {"temp_c": 21.0, "temp_f": 69.8, "condition": {"text": "Partly cloudy"}},
}


def _fake_get(body: str) -> Callable[[str, float], str]:
    def get(url: str, timeout: float) -> str:
        return body

    return get


def test_fetch_parses_metric() -> None:
    adapter = WeatherApiAdapter("KEY", http_get=_fake_get(json.dumps(_SAMPLE)))
    snapshot = adapter.fetch("London", "metric")
    assert snapshot.location == "London"
    assert snapshot.temperature == 21.0
    assert snapshot.unit == "C"
    assert snapshot.condition == "Partly cloudy"
    assert snapshot.local_time == "2026-06-23 14:30"


def test_fetch_parses_imperial() -> None:
    adapter = WeatherApiAdapter("KEY", http_get=_fake_get(json.dumps(_SAMPLE)))
    snapshot = adapter.fetch("London", "imperial")
    assert snapshot.unit == "F"
    assert snapshot.temperature == 69.8


def test_fetch_sends_key_and_query() -> None:
    captured: dict[str, str] = {}

    def get(url: str, timeout: float) -> str:
        captured["url"] = url
        return json.dumps(_SAMPLE)

    WeatherApiAdapter("SECRETKEY", http_get=get).fetch("São Paulo", "metric")
    assert "key=SECRETKEY" in captured["url"]
    assert "q=S" in captured["url"]


def test_http_failure_raises_weather_error_and_redacts_key() -> None:
    def boom(url: str, timeout: float) -> str:
        raise OSError("network down for key=SECRETKEY")

    adapter = WeatherApiAdapter("SECRETKEY", http_get=boom)
    with pytest.raises(WeatherError) as exc_info:
        adapter.fetch("London", "metric")

    assert "SECRETKEY" not in str(exc_info.value)
    assert exc_info.value.detail is not None
    assert "SECRETKEY" not in exc_info.value.detail


def test_malformed_response_raises_weather_error() -> None:
    adapter = WeatherApiAdapter("KEY", http_get=_fake_get('{"unexpected": true}'))
    with pytest.raises(WeatherError):
        adapter.fetch("London", "metric")
