"""Tests for media metadata rendering."""

from __future__ import annotations

import io

from rich.console import Console

from transcriber.config.models import Language
from transcriber.core.media import MediaFormat, MediaMetadata, PlaylistEntry, PlaylistMetadata
from transcriber.ui.i18n import Translator
from transcriber.ui.media import format_duration, format_size, render_metadata


def test_format_duration() -> None:
    assert format_duration(None) == "?"
    assert format_duration(75) == "1:15"
    assert format_duration(3725) == "1:02:05"


def test_format_size() -> None:
    assert format_size(None) == "?"
    assert format_size(512).endswith("B")
    assert "KB" in format_size(2048)


def _media() -> MediaMetadata:
    return MediaMetadata(
        media_id="abc",
        title="My Video",
        extractor="Youtube",
        webpage_url="https://youtu.be/abc",
        duration_seconds=215.0,
        uploader="Chan",
        formats=(MediaFormat("137", "mp4", 1080, 1_000_000, "avc1", "none", "1080p"),),
    )


def test_render_media(console_buffer: tuple[Console, io.StringIO]) -> None:
    console, buffer = console_buffer
    render_metadata(console, _media(), Translator(Language.EN_US))
    output = buffer.getvalue()
    assert "My Video" in output
    assert "Youtube" in output
    assert "3:35" in output
    assert "137" in output


def test_render_playlist(console_buffer: tuple[Console, io.StringIO]) -> None:
    console, buffer = console_buffer
    playlist = PlaylistMetadata(
        playlist_id="PL",
        title="My List",
        extractor="youtube:playlist",
        webpage_url="https://yt/PL",
        entry_count=2,
        entries=(PlaylistEntry("v1", "One", "u1"), PlaylistEntry("v2", "Two", "u2")),
    )
    render_metadata(console, playlist, Translator(Language.EN_US))
    output = buffer.getvalue()
    assert "My List" in output
    assert "One" in output
    assert "Two" in output
