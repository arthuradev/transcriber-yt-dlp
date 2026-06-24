"""SQLite-backed operation history (implements HistoryRepositoryPort).

User-local SQLite database; never committed (``*.sqlite`` is gitignored). Stores
only secret-free summary fields.
"""

from __future__ import annotations

import os
import sqlite3
from collections.abc import Callable
from datetime import datetime
from pathlib import Path

from transcriber.core.history import HistoryEntry

_SCHEMA = """
CREATE TABLE IF NOT EXISTS history (
    timestamp TEXT NOT NULL,
    kind TEXT NOT NULL,
    status TEXT NOT NULL,
    item_count INTEGER NOT NULL,
    succeeded INTEGER NOT NULL,
    skipped INTEGER NOT NULL,
    failed INTEGER NOT NULL,
    detail TEXT NOT NULL
)
"""

_COLUMNS = "timestamp, kind, status, item_count, succeeded, skipped, failed, detail"


def default_history_path() -> Path:
    """Return the default user-local history database path."""
    appdata = os.environ.get("APPDATA")
    root = Path(appdata) if appdata else Path.home() / ".config"
    return root / "Transcriber" / "history.sqlite"


class SqliteHistoryRepository:
    """SQLite operation-history store."""

    def __init__(self, path: Path) -> None:
        self._path = path
        path.parent.mkdir(parents=True, exist_ok=True)
        self._run(lambda conn: conn.execute(_SCHEMA))

    def _run(self, action: Callable[[sqlite3.Connection], object]) -> None:
        conn = sqlite3.connect(self._path)
        try:
            action(conn)
            conn.commit()
        finally:
            conn.close()

    def add(self, entry: HistoryEntry) -> None:
        self._run(
            lambda conn: conn.execute(
                f"INSERT INTO history ({_COLUMNS}) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    entry.timestamp.isoformat(),
                    entry.kind,
                    entry.status,
                    entry.item_count,
                    entry.succeeded,
                    entry.skipped,
                    entry.failed,
                    entry.detail,
                ),
            )
        )

    def recent(self, limit: int = 20) -> list[HistoryEntry]:
        conn = sqlite3.connect(self._path)
        try:
            rows = conn.execute(
                f"SELECT {_COLUMNS} FROM history ORDER BY timestamp DESC LIMIT ?",
                (limit,),
            ).fetchall()
        finally:
            conn.close()
        return [
            HistoryEntry(
                timestamp=datetime.fromisoformat(row[0]),
                kind=row[1],
                status=row[2],
                item_count=row[3],
                succeeded=row[4],
                skipped=row[5],
                failed=row[6],
                detail=row[7],
            )
            for row in rows
        ]
