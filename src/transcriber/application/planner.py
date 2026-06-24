"""Download planning use case.

Turns a probe result + chosen profile + path settings into a structured,
classified, dry-run-able ``DownloadPlan``. No side effects: planning never
touches the network or filesystem. The current date is injected for determinism.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import date

from transcriber.config.models import PathsConfig
from transcriber.core.media import MediaMetadata, PlaylistMetadata, ProbeResult
from transcriber.core.paths import plan_output_path
from transcriber.core.plan import DownloadPlan, PlannedItem
from transcriber.core.profiles import DownloadProfile
from transcriber.safety.risk import classify_download


class DownloadPlanner:
    """Builds download plans from probe results."""

    def __init__(self, *, today: Callable[[], date] = date.today) -> None:
        self._today = today

    def plan(
        self,
        probe: ProbeResult,
        profile: DownloadProfile,
        paths: PathsConfig,
    ) -> DownloadPlan:
        today = self._today()
        overwrite = paths.overwrite_policy == "overwrite"

        if isinstance(probe, PlaylistMetadata):
            is_playlist = True
            extractor = probe.extractor
            items = tuple(
                self._plan_item(
                    title=entry.title,
                    media_id=entry.media_id,
                    url=entry.url,
                    extractor=extractor,
                    profile=profile,
                    paths=paths,
                    today=today,
                )
                for entry in probe.entries
            )
            item_count = probe.entry_count or len(items)
        else:
            media: MediaMetadata = probe
            is_playlist = False
            items = (
                self._plan_item(
                    title=media.title,
                    media_id=media.media_id,
                    url=media.webpage_url,
                    extractor=media.extractor,
                    profile=profile,
                    paths=paths,
                    today=today,
                ),
            )
            item_count = 1

        assessment = classify_download(
            item_count=item_count,
            profile_kind=profile.kind,
            overwrite=overwrite,
        )

        warnings = list(assessment.reasons)
        if profile.requires_ffmpeg:
            warnings.append("Requires ffmpeg to be installed.")
        if not items:
            warnings.append("No downloadable items were found.")

        return DownloadPlan(
            profile_id=profile.profile_id,
            format_selector=profile.format_selector,
            output_dir=paths.download_dir,
            is_playlist=is_playlist,
            items=items,
            risk=assessment.level,
            requires_confirmation=assessment.requires_confirmation,
            requires_strong_confirmation=assessment.requires_strong_confirmation,
            requires_ffmpeg=profile.requires_ffmpeg,
            warnings=tuple(warnings),
        )

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
        )
        return PlannedItem(title=title, media_id=media_id, url=url, output_path=output_path)
