"""Port for the download archive (duplicate avoidance)."""

from __future__ import annotations

from typing import Protocol


class DownloadArchive(Protocol):
    """Records which items have been downloaded, to skip duplicates."""

    def contains(self, key: str) -> bool:
        """Whether ``key`` has already been downloaded."""
        ...

    def add(self, key: str) -> None:
        """Record ``key`` as downloaded."""
        ...
