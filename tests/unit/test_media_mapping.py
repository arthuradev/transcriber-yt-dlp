"""Tests for mapping yt-dlp info dicts to the media domain."""

from __future__ import annotations

from typing import Any

import pytest

from transcriber.adapters.yt_dlp_mapping import map_info
from transcriber.core.media import MediaError, MediaMetadata, PlaylistMetadata

_VIDEO: dict[str, Any] = {
    "id": "abc123",
    "title": "My Video",
    "extractor_key": "Youtube",
    "webpage_url": "https://youtu.be/abc123",
    "duration": 215.0,
    "uploader": "Chan",
    "subtitles": {"en": [{"ext": "vtt"}], "es": [{"ext": "vtt"}]},
    "automatic_captions": {"fr": [{"ext": "vtt"}]},
    "formats": [
        {
            "format_id": "137",
            "ext": "mp4",
            "height": 1080,
            "filesize": 1000000,
            "vcodec": "avc1",
            "acodec": "none",
            "format_note": "1080p",
        },
        {
            "format_id": "140",
            "ext": "m4a",
            "filesize_approx": 500000,
            "vcodec": "none",
            "acodec": "mp4a",
            "format_note": "audio",
        },
    ],
}

_PLAYLIST: dict[str, Any] = {
    "_type": "playlist",
    "id": "PL1",
    "title": "My List",
    "extractor": "youtube:playlist",
    "webpage_url": "https://yt/playlist?list=PL1",
    "playlist_count": 2,
    "entries": [
        {"id": "v1", "title": "One", "url": "u1"},
        {"id": "v2", "title": "Two", "webpage_url": "u2"},
    ],
}


def test_map_single_video() -> None:
    result = map_info(_VIDEO)
    assert isinstance(result, MediaMetadata)
    assert result.media_id == "abc123"
    assert result.title == "My Video"
    assert result.extractor == "Youtube"
    assert result.duration_seconds == 215.0
    assert result.uploader == "Chan"
    assert len(result.formats) == 2
    assert result.subtitle_languages == ("en", "es")
    assert result.auto_caption_languages == ("fr",)


def test_map_format_fields() -> None:
    result = map_info(_VIDEO)
    assert isinstance(result, MediaMetadata)
    video, audio = result.formats
    assert video.height == 1080
    assert video.filesize == 1000000
    assert video.acodec == "none"
    assert audio.filesize == 500000  # taken from filesize_approx
    assert audio.vcodec == "none"


def test_map_playlist() -> None:
    result = map_info(_PLAYLIST)
    assert isinstance(result, PlaylistMetadata)
    assert result.playlist_id == "PL1"
    assert result.entry_count == 2
    assert len(result.entries) == 2
    assert result.entries[0].title == "One"
    assert result.entries[1].url == "u2"


def test_playlist_count_falls_back_to_len() -> None:
    data: dict[str, Any] = {
        "_type": "playlist",
        "id": "PL",
        "title": "x",
        "entries": [{"id": "a", "title": "A", "url": "u"}],
    }
    result = map_info(data)
    assert isinstance(result, PlaylistMetadata)
    assert result.entry_count == 1


def test_none_entries_are_skipped() -> None:
    data: dict[str, Any] = {
        "_type": "playlist",
        "id": "PL",
        "title": "x",
        "entries": [None, {"id": "a", "title": "A", "url": "u"}],
    }
    result = map_info(data)
    assert isinstance(result, PlaylistMetadata)
    assert len(result.entries) == 1


def test_missing_id_and_title_raises() -> None:
    with pytest.raises(MediaError):
        map_info({"formats": []})
