"""Tests for the download summary renderer."""

from __future__ import annotations

import io

from rich.console import Console

from transcriber.config.models import Language
from transcriber.core.download import DownloadOutcome, DownloadResult
from transcriber.ui.download_result import render_download_summary
from transcriber.ui.i18n import Translator


def test_summary_success(console_buffer: tuple[Console, io.StringIO]) -> None:
    console, buffer = console_buffer
    outcome = DownloadOutcome((DownloadResult(True, "out/a.mp4", None),))
    render_download_summary(console, outcome, Translator(Language.EN_US))
    output = buffer.getvalue()
    assert "Download complete" in output
    assert "out/a.mp4" in output
    assert "1 succeeded" in output


def test_summary_failure_shows_error(console_buffer: tuple[Console, io.StringIO]) -> None:
    console, buffer = console_buffer
    outcome = DownloadOutcome((DownloadResult(False, None, "network error"),))
    render_download_summary(console, outcome, Translator(Language.EN_US))
    output = buffer.getvalue()
    assert "Download failed" in output
    assert "network error" in output


def test_summary_partial(console_buffer: tuple[Console, io.StringIO]) -> None:
    console, buffer = console_buffer
    outcome = DownloadOutcome((DownloadResult(True, "a", None), DownloadResult(False, None, "x")))
    render_download_summary(console, outcome, Translator(Language.EN_US))
    assert "Partly completed" in buffer.getvalue()
