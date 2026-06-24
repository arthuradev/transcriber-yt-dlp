"""Tests for the dry-run plan renderer."""

from __future__ import annotations

import io

from rich.console import Console

from transcriber.config.models import Language
from transcriber.core.operations import RiskLevel
from transcriber.core.plan import DownloadPlan, PlannedItem
from transcriber.ui.i18n import Translator
from transcriber.ui.plan import render_plan


def _plan() -> DownloadPlan:
    return DownloadPlan(
        profile_id="video_1080p",
        format_selector="bv*[height<=1080]+ba/b[height<=1080]",
        output_dir="out",
        is_playlist=False,
        items=(PlannedItem("My Video", "abc", "u", "out/My Video [abc].mp4"),),
        risk=RiskLevel.MEDIUM,
        requires_confirmation=True,
        requires_strong_confirmation=False,
        requires_ffmpeg=True,
        warnings=("Requires ffmpeg to be installed.",),
    )


def test_render_plan_shows_key_fields(console_buffer: tuple[Console, io.StringIO]) -> None:
    console, buffer = console_buffer
    render_plan(console, _plan(), Translator(Language.EN_US))
    output = buffer.getvalue()
    assert "video_1080p" in output
    assert "My Video" in output
    assert "medium" in output
    assert "ffmpeg" in output


def test_render_plan_with_bracketed_format_does_not_crash(
    console_buffer: tuple[Console, io.StringIO],
) -> None:
    console, buffer = console_buffer
    # The format selector contains '[' which must be escaped, not parsed as markup.
    render_plan(console, _plan(), Translator(Language.EN_US))
    assert "height<=1080" in buffer.getvalue()
