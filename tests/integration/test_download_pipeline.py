"""Integration test: plan -> execute -> archive -> history -> report.

Exercises multiple real components together (planner, executor, file archive,
SQLite history, recorder, reporting) with a fake engine at the boundary.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, date, datetime
from pathlib import Path

from transcriber.application.executor import DownloadExecutor
from transcriber.application.planner import DownloadPlanner
from transcriber.application.reporting import build_download_report
from transcriber.config.models import PathsConfig
from transcriber.core.download import (
    DownloadProgress,
    DownloadRequest,
    DownloadResult,
    DownloadStatus,
)
from transcriber.core.media import MediaMetadata
from transcriber.core.profiles import DOWNLOAD_PROFILES
from transcriber.observability.recorder import OperationRecorder
from transcriber.storage.archive import FileDownloadArchive
from transcriber.storage.history import SqliteHistoryRepository


class _Engine:
    def __init__(self) -> None:
        self.calls = 0

    def download(
        self,
        request: DownloadRequest,
        on_progress: Callable[[DownloadProgress], None],
    ) -> DownloadResult:
        self.calls += 1
        on_progress(DownloadProgress(DownloadStatus.FINISHED, 1, 1, None, None, None))
        return DownloadResult(True, request.output_path, None)


def _now() -> datetime:
    return datetime(2026, 6, 24, tzinfo=UTC)


def test_full_download_pipeline_with_archive_and_history(tmp_path: Path) -> None:
    archive = FileDownloadArchive(tmp_path / "archive.txt")
    history = SqliteHistoryRepository(tmp_path / "history.sqlite")
    recorder = OperationRecorder(history=history, report_dir=str(tmp_path / "reports"))
    planner = DownloadPlanner(today=lambda: date(2026, 6, 24), archive=archive)
    engine = _Engine()
    executor = DownloadExecutor(engine, archive=archive)
    paths = PathsConfig(download_dir=str(tmp_path / "out"))
    media = MediaMetadata("vid1", "Title", "Yt", "https://x/vid1", 10.0, None, ())

    plan = planner.plan(media, DOWNLOAD_PROFILES["video_best"], paths)
    outcome = executor.execute(plan, on_progress=lambda p: None)
    recorder.record(build_download_report(plan, outcome, now=_now))

    assert outcome.ok
    assert engine.calls == 1
    assert "Yt:vid1" in (tmp_path / "archive.txt").read_text(encoding="utf-8")
    assert len(history.recent()) == 1
    assert list((tmp_path / "reports").glob("*.json"))

    # Re-running the same item is detected as a duplicate and skipped.
    plan2 = planner.plan(media, DOWNLOAD_PROFILES["video_best"], paths)
    assert plan2.items[0].is_duplicate
    outcome2 = executor.execute(plan2, on_progress=lambda p: None)
    assert outcome2.skipped == 1
    assert engine.calls == 1
