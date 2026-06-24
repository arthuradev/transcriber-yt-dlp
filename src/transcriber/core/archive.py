"""Download archive key policy (pure)."""

from __future__ import annotations


def archive_key(extractor: str, media_id: str) -> str:
    """Build the archive key identifying a downloaded item."""
    return f"{extractor}:{media_id}"
