"""Download plan domain model.

The structured, dry-run-able plan produced before any download. Pure data.
"""

from __future__ import annotations

from dataclasses import dataclass

from transcriber.core.operations import RiskLevel


@dataclass(frozen=True)
class PlannedItem:
    """One item that would be downloaded, with its planned output path."""

    title: str
    media_id: str
    url: str
    output_path: str
    extractor: str = ""
    is_duplicate: bool = False


@dataclass(frozen=True)
class DownloadPlan:
    """A safe, inspectable plan for a download operation (no side effects)."""

    profile_id: str
    format_selector: str
    output_dir: str
    is_playlist: bool
    items: tuple[PlannedItem, ...]
    risk: RiskLevel
    requires_confirmation: bool
    requires_strong_confirmation: bool
    requires_ffmpeg: bool
    warnings: tuple[str, ...]
    extract_audio: bool = False
    audio_format: str | None = None
    is_downloadable: bool = True
    cookies_from_browser: str | None = None

    @property
    def item_count(self) -> int:
        return len(self.items)

    @property
    def has_items(self) -> bool:
        return bool(self.items)
