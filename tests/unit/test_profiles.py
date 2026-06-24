"""Tests for download profiles."""

from __future__ import annotations

from transcriber.core.media import MediaFormat
from transcriber.core.profiles import (
    DOWNLOAD_PROFILES,
    get_profile,
    manual_profile,
    profiles_for_category,
)


def _fmt(*, vcodec: str | None, acodec: str | None, ext: str = "mp4") -> MediaFormat:
    return MediaFormat("137", ext, 1080, 1000, vcodec, acodec, "note")


def test_manual_profile_video() -> None:
    profile = manual_profile(_fmt(vcodec="avc1", acodec="none"))
    assert profile.kind == "video"
    assert profile.format_selector == "137"
    assert profile.default_ext == "mp4"
    assert profile.profile_id == "manual:137"


def test_manual_profile_audio() -> None:
    profile = manual_profile(_fmt(vcodec="none", acodec="mp4a", ext="m4a"))
    assert profile.kind == "audio"
    assert profile.format_selector == "137"
    assert profile.default_ext == "m4a"


def test_all_profiles_present() -> None:
    assert set(DOWNLOAD_PROFILES) == {
        "video_best",
        "video_1080p",
        "video_720p",
        "audio_best",
        "audio_mp3",
        "audio_m4a",
        "metadata_only",
        "transcript_only",
    }


def test_get_profile() -> None:
    assert get_profile("audio_mp3") is not None
    assert get_profile("nope") is None


def test_profiles_for_category() -> None:
    video = {p.profile_id for p in profiles_for_category("video")}
    assert video == {"video_best", "video_1080p", "video_720p"}
    audio = {p.profile_id for p in profiles_for_category("audio")}
    assert audio == {"audio_best", "audio_mp3", "audio_m4a"}
    transcript = {p.profile_id for p in profiles_for_category("transcript")}
    assert transcript == {"transcript_only", "metadata_only"}
    assert profiles_for_category("unknown") == ()
