"""Operation history domain (pure)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class HistoryEntry:
    """A durable record of one completed operation (no secrets, no content)."""

    timestamp: datetime
    kind: str  # download | transcribe | cleanup | subtitles
    status: str  # ok | partial | failed
    item_count: int
    succeeded: int
    skipped: int
    failed: int
    detail: str
