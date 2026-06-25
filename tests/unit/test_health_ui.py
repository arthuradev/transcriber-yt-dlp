"""Tests for the health renderer."""

from __future__ import annotations

import io

from rich.console import Console

from transcriber.config.models import Language
from transcriber.core.health import HealthCheck, HealthReport
from transcriber.ui.health import render_health
from transcriber.ui.i18n import Translator


def test_render_health(console_buffer: tuple[Console, io.StringIO]) -> None:
    console, buffer = console_buffer
    report = HealthReport(
        (
            HealthCheck("ffmpeg", True, "Needed for audio."),
            HealthCheck("gpu", False, "Needed for transcription."),
        )
    )
    render_health(console, report, Translator(Language.EN_US))
    output = buffer.getvalue()
    assert "Diagnostics" in output
    assert "ffmpeg" in output
    assert "gpu" in output
    assert "missing" in output
