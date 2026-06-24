"""Tests for the SQLite history repository."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from transcriber.core.history import HistoryEntry
from transcriber.storage.history import SqliteHistoryRepository, default_history_path


def _entry(kind: str = "download", when: datetime | None = None) -> HistoryEntry:
    timestamp = when if when is not None else datetime(2026, 6, 24, tzinfo=UTC)
    return HistoryEntry(timestamp, kind, "ok", 1, 1, 0, 0, "d")


def test_default_history_path() -> None:
    path = default_history_path()
    assert path.name == "history.sqlite"
    assert path.parent.name == "Transcriber"


def test_add_and_recent_newest_first(tmp_path: Path) -> None:
    repo = SqliteHistoryRepository(tmp_path / "sub" / "history.sqlite")
    repo.add(_entry("download", datetime(2026, 6, 24, 10, tzinfo=UTC)))
    repo.add(_entry("transcribe", datetime(2026, 6, 24, 11, tzinfo=UTC)))
    recent = repo.recent()
    assert len(recent) == 2
    assert recent[0].kind == "transcribe"
    assert recent[1].kind == "download"


def test_recent_limit(tmp_path: Path) -> None:
    repo = SqliteHistoryRepository(tmp_path / "history.sqlite")
    for hour in range(5):
        repo.add(_entry("download", datetime(2026, 6, 24, hour, tzinfo=UTC)))
    assert len(repo.recent(limit=2)) == 2


def test_persists_across_instances(tmp_path: Path) -> None:
    path = tmp_path / "history.sqlite"
    SqliteHistoryRepository(path).add(_entry())
    assert len(SqliteHistoryRepository(path).recent()) == 1
