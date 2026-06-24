"""Download planning use case.

Turns probe result(s) + chosen profile + path settings into a structured,
classified, dry-run-able ``DownloadPlan``. Supports single items, playlists, and
batches, and marks already-downloaded items as duplicates via the archive. No
side effects: planning never touches the network or filesystem. The current date
is injected for determinism.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from datetime import date

from transcriber.config.models import PathsConfig
from transcriber.core.archive import archive_key
from transcriber.core.media import MediaMetadata, PlaylistMetadata, ProbeResult
from transcriber.core.paths import plan_output_path
from transcriber.core.plan import DownloadPlan, PlannedItem
from transcriber.core.profiles import DownloadProfile
from transcriber.ports.archive import DownloadArchive
from transcriber.safety.risk import classify_download


class DownloadPlanner:
    """Builds download plans from probe results."""

    def __init__(
        self,
        *,
        today: Callable[[], date] = date.today,
        archive: DownloadArchive | None = None,
    ) -> None:
        self._today = today
        self._archive = archive

    def plan(
        self, probe: ProbeResult, profile: DownloadProfile, paths: PathsConfig
    ) -> DownloadPlan:
        """Plan a single probe result."""
        return self.plan_batch([probe], profile, paths)

    def plan_batch(
        self,
        probes: Sequence[ProbeResult],
        profile: DownloadProfile,
        paths: PathsConfig,
    ) -> DownloadPlan:
        """Plan one or more probe results as a single operation."""
        today = self._today()
        items: list[PlannedItem] = []
        declared = 0
        multi = len(probes) > 1
        for probe in probes:
            probe_items, probe_declared, is_playlist = self._items_for(probe, profile, paths, today)
            items.extend(probe_items)
            declared += probe_declared
            multi = multi or is_playlist

        assessment = classify_download(
            item_count=declared,
            profile_kind=profile.kind,
            overwrite=paths.overwrite_policy == "overwrite",
        )

        warnings = list(assessment.reasons)
        if profile.requires_ffmpeg:
            warnings.append("Requires ffmpeg to be installed.")
        if not items:
            warnings.append("No downloadable items were found.")
        duplicates = sum(1 for item in items if item.is_duplicate)
        if duplicates:
            warnings.append(f"{duplicates} item(s) already downloaded (will be skipped).")

        return DownloadPlan(
            profile_id=profile.profile_id,
            format_selector=profile.format_selector,
            output_dir=paths.download_dir,
            is_playlist=multi,
            items=tuple(items),
            risk=assessment.level,
            requires_confirmation=assessment.requires_confirmation,
            requires_strong_confirmation=assessment.requires_strong_confirmation,
            requires_ffmpeg=profile.requires_ffmpeg,
            warnings=tuple(warnings),
            extract_audio=profile.extract_audio,
            audio_format=profile.audio_format,
            is_downloadable=profile.kind in ("video", "audio"),
        )

    def _items_for(
        self,
        probe: ProbeResult,
        profile: DownloadProfile,
        paths: PathsConfig,
        today: date,
    ) -> tuple[tuple[PlannedItem, ...], int, bool]:
        if isinstance(probe, PlaylistMetadata):
            items = tuple(
                self._plan_item(
                    title=entry.title,
                    media_id=entry.media_id,
                    url=entry.url,
                    extractor=probe.extractor,
                    profile=profile,
                    paths=paths,
                    today=today,
                    group=probe.title,
                )
                for entry in probe.entries
            )
            return items, probe.entry_count or len(items), True

        media: MediaMetadata = probe
        item = self._plan_item(
            title=media.title,
            media_id=media.media_id,
            url=media.webpage_url,
            extractor=media.extractor,
            profile=profile,
            paths=paths,
            today=today,
            group="",
        )
        return (item,), 1, False

    def _plan_item(
        self,
        *,
        title: str,
        media_id: str,
        url: str,
        extractor: str,
        profile: DownloadProfile,
        paths: PathsConfig,
        today: date,
        group: str,
    ) -> PlannedItem:
        output_path = plan_output_path(
            output_dir=paths.download_dir,
            extractor=extractor,
            media_id=media_id,
            title=title,
            ext=profile.default_ext,
            organize_by_site=paths.organize_by_site,
            organize_by_date=paths.organize_by_date,
            include_media_id=paths.include_media_id_in_filename,
            today=today,
            group=group,
        )
        is_duplicate = bool(
            self._archive is not None
            and media_id
            and self._archive.contains(archive_key(extractor, media_id))
        )
        return PlannedItem(
            title=title,
            media_id=media_id,
            url=url,
            output_path=output_path,
            extractor=extractor,
            is_duplicate=is_duplicate,
        )
