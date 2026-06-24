"""Operation report domain (pure)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from transcriber.core.history import HistoryEntry


@dataclass(frozen=True)
class OperationReport:
    """A full, secret-free report of one operation."""

    kind: str
    status: str  # ok | partial | failed
    item_count: int
    succeeded: int
    skipped: int
    failed: int
    outputs: tuple[str, ...]
    warnings: tuple[str, ...]
    timestamp: datetime
    detail: str = ""

    def to_history_entry(self) -> HistoryEntry:
        """Project this report into a compact history entry."""
        return HistoryEntry(
            timestamp=self.timestamp,
            kind=self.kind,
            status=self.status,
            item_count=self.item_count,
            succeeded=self.succeeded,
            skipped=self.skipped,
            failed=self.failed,
            detail=self.detail,
        )
