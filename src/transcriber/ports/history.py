"""Port for the operation-history repository."""

from __future__ import annotations

from typing import Protocol

from transcriber.core.history import HistoryEntry


class HistoryRepositoryPort(Protocol):
    """Stores and retrieves operation history."""

    def add(self, entry: HistoryEntry) -> None:
        """Append a history entry."""
        ...

    def recent(self, limit: int = 20) -> list[HistoryEntry]:
        """Return the most recent entries, newest first."""
        ...
