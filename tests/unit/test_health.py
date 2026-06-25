"""Tests for the health report and builder."""

from __future__ import annotations

from transcriber.application.health import build_health_report
from transcriber.core.health import HealthCheck, HealthReport


class _Probe:
    def __init__(self, *, windows: bool = True, ffmpeg: bool = True, gpu: bool = False) -> None:
        self._windows = windows
        self._ffmpeg = ffmpeg
        self._gpu = gpu

    def is_windows(self) -> bool:
        return self._windows

    def has_ffmpeg(self) -> bool:
        return self._ffmpeg

    def gpu_available(self) -> bool:
        return self._gpu


def test_report_all_ok() -> None:
    report = HealthReport((HealthCheck("a", True, "x"), HealthCheck("b", True, "y")))
    assert report.all_ok


def test_report_not_all_ok() -> None:
    report = HealthReport((HealthCheck("a", True, "x"), HealthCheck("b", False, "y")))
    assert not report.all_ok


def test_build_health_report() -> None:
    report = build_health_report(_Probe(windows=True, ffmpeg=True, gpu=False))
    by_name = {check.name: check.ok for check in report.checks}
    assert by_name["windows"] is True
    assert by_name["ffmpeg"] is True
    assert by_name["gpu"] is False
    assert not report.all_ok
