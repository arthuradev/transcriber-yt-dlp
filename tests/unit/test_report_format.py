"""Tests for report serialization and the history projection."""

from __future__ import annotations

import json
from datetime import UTC, datetime

from transcriber.core.report import OperationReport
from transcriber.observability.report_format import report_to_json, report_to_markdown


def _report() -> OperationReport:
    return OperationReport(
        kind="download",
        status="ok",
        item_count=2,
        succeeded=2,
        skipped=0,
        failed=0,
        outputs=("a.mp4", "b.mp4"),
        warnings=("w",),
        timestamp=datetime(2026, 6, 24, tzinfo=UTC),
        detail="profile=x",
    )


def test_to_history_entry() -> None:
    entry = _report().to_history_entry()
    assert entry.kind == "download"
    assert entry.status == "ok"
    assert entry.item_count == 2
    assert entry.detail == "profile=x"


def test_report_to_json() -> None:
    data = json.loads(report_to_json(_report()))
    assert data["kind"] == "download"
    assert data["status"] == "ok"
    assert data["outputs"] == ["a.mp4", "b.mp4"]
    assert data["timestamp"].startswith("2026-06-24")


def test_report_to_markdown() -> None:
    markdown = report_to_markdown(_report())
    assert markdown.startswith("# download report")
    assert "Status: ok" in markdown
    assert "a.mp4" in markdown
    assert "## Warnings" in markdown
