"""Tests for building download reports."""

from __future__ import annotations

from datetime import UTC, datetime

from transcriber.application.reporting import build_download_report
from transcriber.core.download import DownloadOutcome, DownloadResult
from transcriber.core.operations import RiskLevel
from transcriber.core.plan import DownloadPlan, PlannedItem


def _now() -> datetime:
    return datetime(2026, 6, 24, tzinfo=UTC)


def _plan(items: tuple[PlannedItem, ...], *, cookies: str | None = None) -> DownloadPlan:
    return DownloadPlan(
        profile_id="video_best",
        format_selector="bv",
        output_dir="out",
        is_playlist=False,
        items=items,
        risk=RiskLevel.MEDIUM,
        requires_confirmation=True,
        requires_strong_confirmation=False,
        requires_ffmpeg=False,
        warnings=("w1",),
        cookies_from_browser=cookies,
    )


def test_report_ok() -> None:
    plan = _plan((PlannedItem("T", "id", "u", "out/T.mp4"),))
    outcome = DownloadOutcome((DownloadResult(True, "out/T.mp4", None),))
    report = build_download_report(plan, outcome, now=_now)
    assert report.kind == "download"
    assert report.status == "ok"
    assert report.item_count == 1
    assert report.succeeded == 1
    assert report.outputs == ("out/T.mp4",)
    assert report.warnings == ("w1",)
    assert "profile=video_best" in report.detail
    assert "cookies=no" in report.detail


def test_report_partial() -> None:
    plan = _plan((PlannedItem("T", "i", "u", "p"), PlannedItem("T2", "i2", "u2", "p2")))
    outcome = DownloadOutcome((DownloadResult(True, "p", None), DownloadResult(False, None, "err")))
    assert build_download_report(plan, outcome, now=_now).status == "partial"


def test_report_failed() -> None:
    plan = _plan((PlannedItem("T", "i", "u", "p"),))
    outcome = DownloadOutcome((DownloadResult(False, None, "err"),))
    assert build_download_report(plan, outcome, now=_now).status == "failed"


def test_report_cookies_flag() -> None:
    plan = _plan((PlannedItem("T", "i", "u", "p"),), cookies="chrome")
    outcome = DownloadOutcome((DownloadResult(True, "p", None),))
    assert "cookies=yes" in build_download_report(plan, outcome, now=_now).detail
