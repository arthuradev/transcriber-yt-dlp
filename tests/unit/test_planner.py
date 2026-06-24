"""Tests for the download planner."""

from __future__ import annotations

from datetime import date

from transcriber.application.planner import DownloadPlanner
from transcriber.config.models import PathsConfig
from transcriber.core.media import MediaMetadata, PlaylistEntry, PlaylistMetadata
from transcriber.core.operations import RiskLevel
from transcriber.core.profiles import DOWNLOAD_PROFILES


def _planner() -> DownloadPlanner:
    return DownloadPlanner(today=lambda: date(2026, 6, 24))


def _media() -> MediaMetadata:
    return MediaMetadata(
        media_id="abc",
        title="My Video",
        extractor="Youtube",
        webpage_url="https://x/abc",
        duration_seconds=100.0,
        uploader=None,
        formats=(),
    )


def test_plan_single_video() -> None:
    plan = _planner().plan(
        _media(), DOWNLOAD_PROFILES["video_best"], PathsConfig(download_dir="out")
    )
    assert plan.item_count == 1
    assert plan.risk is RiskLevel.MEDIUM
    assert plan.requires_confirmation
    assert not plan.requires_strong_confirmation
    item = plan.items[0]
    assert item.output_path.startswith("out/")
    assert "Youtube" in item.output_path
    assert "2026-06-24" in item.output_path
    assert item.output_path.endswith(".mp4")
    assert "[abc]" in item.output_path


def test_plan_metadata_profile_is_low() -> None:
    plan = _planner().plan(_media(), DOWNLOAD_PROFILES["metadata_only"], PathsConfig())
    assert plan.risk is RiskLevel.LOW
    assert not plan.requires_confirmation


def test_plan_large_playlist_is_high() -> None:
    entries = tuple(PlaylistEntry(f"id{i}", f"T{i}", f"u{i}") for i in range(7))
    playlist = PlaylistMetadata("PL", "List", "Youtube", "https://x/PL", 7, entries)
    plan = _planner().plan(playlist, DOWNLOAD_PROFILES["video_best"], PathsConfig())
    assert plan.is_playlist
    assert plan.item_count == 7
    assert plan.risk is RiskLevel.HIGH
    assert plan.requires_strong_confirmation


def test_plan_respects_organize_flags() -> None:
    paths = PathsConfig(
        download_dir="d",
        organize_by_site=False,
        organize_by_date=False,
        include_media_id_in_filename=False,
    )
    plan = _planner().plan(_media(), DOWNLOAD_PROFILES["audio_mp3"], paths)
    assert plan.items[0].output_path == "d/My Video.mp3"
    assert plan.requires_ffmpeg


def test_plan_playlist_uses_group_subfolder() -> None:
    entries = (PlaylistEntry("v1", "Clip 1", "u1"),)
    playlist = PlaylistMetadata("PL", "My List", "Youtube", "https://x/PL", 1, entries)
    plan = _planner().plan(
        playlist, DOWNLOAD_PROFILES["video_best"], PathsConfig(download_dir="out")
    )
    assert plan.items[0].output_path == "out/Youtube/2026-06-24/My List/Clip 1 [v1].mp4"


def test_plan_batch_flattens_and_classifies() -> None:
    m1 = MediaMetadata("a", "A", "Yt", "https://x/a", None, None, ())
    m2 = MediaMetadata("b", "B", "Yt", "https://x/b", None, None, ())
    entries = tuple(PlaylistEntry(f"id{i}", f"T{i}", f"u{i}") for i in range(5))
    playlist = PlaylistMetadata("PL", "L", "Yt", "https://x/PL", 5, entries)
    plan = _planner().plan_batch([m1, m2, playlist], DOWNLOAD_PROFILES["video_best"], PathsConfig())
    assert plan.item_count == 7
    assert plan.is_playlist
    assert plan.risk is RiskLevel.HIGH


def test_plan_marks_duplicates() -> None:
    class _Archive:
        def contains(self, key: str) -> bool:
            return key == "Yt:a"

        def add(self, key: str) -> None:
            pass

    planner = DownloadPlanner(today=lambda: date(2026, 6, 24), archive=_Archive())
    media = MediaMetadata("a", "A", "Yt", "https://x/a", None, None, ())
    plan = planner.plan(media, DOWNLOAD_PROFILES["video_best"], PathsConfig())
    assert plan.items[0].is_duplicate
    assert any("already downloaded" in warning for warning in plan.warnings)
