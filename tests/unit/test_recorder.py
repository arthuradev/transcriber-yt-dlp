"""Tests for the operation recorder."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from transcriber.core.history import HistoryEntry
from transcriber.core.report import OperationReport
from transcriber.observability.logs import FileLogger
from transcriber.observability.recorder import OperationRecorder


class _History:
    def __init__(self) -> None:
        self.entries: list[HistoryEntry] = []

    def add(self, entry: HistoryEntry) -> None:
        self.entries.append(entry)

    def recent(self, limit: int = 20) -> list[HistoryEntry]:
        return list(self.entries)


def _report() -> OperationReport:
    return OperationReport(
        kind="download",
        status="ok",
        item_count=1,
        succeeded=1,
        skipped=0,
        failed=0,
        outputs=("a.mp4",),
        warnings=(),
        timestamp=datetime(2026, 6, 24, 12, 30, 45, tzinfo=UTC),
        detail="profile=x",
    )


def test_records_to_history_log_and_report(tmp_path: Path) -> None:
    history = _History()
    logger = FileLogger(tmp_path / "t.log")
    recorder = OperationRecorder(
        history=history, logger=logger, report_dir=str(tmp_path / "reports")
    )
    recorder.record(_report())

    assert len(history.entries) == 1
    assert (tmp_path / "t.log").is_file()
    reports = list((tmp_path / "reports").glob("*.json"))
    assert len(reports) == 1
    assert "report-20260624-123045-download" in reports[0].name


def test_record_with_no_sinks_is_noop() -> None:
    OperationRecorder().record(_report())
