"""Download profiles.

Pure domain definitions of the supported download profiles (mirrors
``configs/profiles.example.yaml``). No I/O.
"""

from __future__ import annotations

from dataclasses import dataclass

from transcriber.core.media import MediaFormat

MANUAL_PROFILE_ID = "__manual__"


@dataclass(frozen=True)
class DownloadProfile:
    """A named download profile and its yt-dlp format selector."""

    profile_id: str
    kind: str  # "video" | "audio" | "metadata" | "transcript"
    format_selector: str
    default_ext: str
    extract_audio: bool
    audio_format: str | None
    requires_ffmpeg: bool


_PROFILES: tuple[DownloadProfile, ...] = (
    DownloadProfile("video_best", "video", "bv*+ba/b", "mp4", False, None, True),
    DownloadProfile(
        "video_1080p", "video", "bv*[height<=1080]+ba/b[height<=1080]", "mp4", False, None, True
    ),
    DownloadProfile(
        "video_720p", "video", "bv*[height<=720]+ba/b[height<=720]", "mp4", False, None, True
    ),
    DownloadProfile("audio_best", "audio", "ba/b", "m4a", False, None, False),
    DownloadProfile("audio_mp3", "audio", "ba/b", "mp3", True, "mp3", True),
    DownloadProfile("audio_m4a", "audio", "m4a/ba/b", "m4a", True, "m4a", True),
    DownloadProfile("metadata_only", "metadata", "", "json", False, None, False),
    DownloadProfile("transcript_only", "transcript", "", "srt", False, None, False),
)

DOWNLOAD_PROFILES: dict[str, DownloadProfile] = {
    profile.profile_id: profile for profile in _PROFILES
}

# Which profile kinds a menu category offers.
_CATEGORY_KINDS: dict[str, tuple[str, ...]] = {
    "video": ("video",),
    "audio": ("audio",),
    "transcript": ("transcript", "metadata"),
}


def get_profile(profile_id: str) -> DownloadProfile | None:
    """Return the profile with ``profile_id``, or ``None``."""
    return DOWNLOAD_PROFILES.get(profile_id)


def profiles_for_category(category: str) -> tuple[DownloadProfile, ...]:
    """Return the profiles offered for a menu ``category`` (video/audio/transcript)."""
    kinds = _CATEGORY_KINDS.get(category, ())
    return tuple(profile for profile in _PROFILES if profile.kind in kinds)


def manual_profile(fmt: MediaFormat) -> DownloadProfile:
    """Build a one-off profile that downloads exactly the chosen format.

    Advanced manual mode: no merging or post-processing, so whatever the user
    picks (video-only, audio-only, or progressive) is what gets downloaded.
    """
    has_video = bool(fmt.vcodec) and fmt.vcodec != "none"
    kind = "video" if has_video else "audio"
    default_ext = fmt.ext or ("mp4" if has_video else "m4a")
    return DownloadProfile(
        profile_id=f"manual:{fmt.format_id}",
        kind=kind,
        format_selector=fmt.format_id,
        default_ext=default_ext,
        extract_audio=False,
        audio_format=None,
        requires_ffmpeg=False,
    )
