"""Tests for the weather service (caching + graceful degradation)."""

from __future__ import annotations

from transcriber.application.weather import WeatherService
from transcriber.core.weather import WeatherError, WeatherSnapshot


def _snapshot(name: str = "London") -> WeatherSnapshot:
    return WeatherSnapshot(
        location=name, temperature=20.0, unit="C", condition="Clear", local_time="t"
    )


class _CountingPort:
    def __init__(self, snapshot: WeatherSnapshot) -> None:
        self.calls = 0
        self._snapshot = snapshot

    def fetch(self, query: str, units: str) -> WeatherSnapshot:
        self.calls += 1
        return self._snapshot


class _FailingPort:
    def fetch(self, query: str, units: str) -> WeatherSnapshot:
        raise WeatherError("nope")


class _Clock:
    def __init__(self) -> None:
        self.now = 0.0

    def __call__(self) -> float:
        return self.now


def test_caches_within_ttl() -> None:
    port = _CountingPort(_snapshot())
    service = WeatherService(port, cache_minutes=15, clock=_Clock())
    first = service.get("London", "metric")
    second = service.get("London", "metric")
    assert first is second
    assert port.calls == 1


def test_refetches_after_ttl() -> None:
    port = _CountingPort(_snapshot())
    clock = _Clock()
    service = WeatherService(port, cache_minutes=15, clock=clock)
    service.get("London", "metric")
    clock.now = 15 * 60 + 1
    service.get("London", "metric")
    assert port.calls == 2


def test_query_change_refetches() -> None:
    port = _CountingPort(_snapshot())
    service = WeatherService(port, cache_minutes=15, clock=_Clock())
    service.get("London", "metric")
    service.get("Paris", "metric")
    assert port.calls == 2


def test_failure_returns_none() -> None:
    service = WeatherService(_FailingPort(), cache_minutes=15, clock=_Clock())
    assert service.get("London", "metric") is None
