"""Map a yt-dlp ``info`` dict into the media domain model.

Kept separate from the engine adapter (and free of any yt-dlp import) so it can
be type-checked strictly and unit-tested with plain dicts. Inputs are treated as
``dict[str, Any]`` (the shape yt-dlp returns after ``sanitize_info``).
"""

from __future__ import annotations

from typing import Any, cast

from transcriber.core.media import (
    MediaError,
    MediaFormat,
    MediaMetadata,
    PlaylistEntry,
    PlaylistMetadata,
    ProbeResult,
)


def _str(value: Any) -> str:
    return "" if value is None else str(value)


def _opt_str(value: Any) -> str | None:
    return None if value is None else str(value)


def _opt_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    return None


def _opt_float(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _map_format(fmt: dict[str, Any]) -> MediaFormat:
    filesize = fmt.get("filesize")
    if filesize is None:
        filesize = fmt.get("filesize_approx")
    return MediaFormat(
        format_id=_str(fmt.get("format_id")),
        ext=_str(fmt.get("ext")),
        height=_opt_int(fmt.get("height")),
        filesize=_opt_int(filesize),
        vcodec=_opt_str(fmt.get("vcodec")),
        acodec=_opt_str(fmt.get("acodec")),
        note=_opt_str(fmt.get("format_note")),
    )


def _map_media(info: dict[str, Any]) -> MediaMetadata:
    media_id = _str(info.get("id"))
    title = _str(info.get("title"))
    if not media_id and not title:
        raise MediaError("Unexpected metadata: missing id and title")
    raw_formats = cast("list[dict[str, Any]]", info.get("formats") or [])
    return MediaMetadata(
        media_id=media_id,
        title=title,
        extractor=_str(info.get("extractor_key") or info.get("extractor")),
        webpage_url=_str(info.get("webpage_url") or info.get("original_url")),
        duration_seconds=_opt_float(info.get("duration")),
        uploader=_opt_str(info.get("uploader")),
        formats=tuple(_map_format(fmt) for fmt in raw_formats if fmt),
    )


def _map_playlist(info: dict[str, Any]) -> PlaylistMetadata:
    raw_entries = cast("list[dict[str, Any]]", info.get("entries") or [])
    entries = tuple(
        PlaylistEntry(
            media_id=_str(entry.get("id")),
            title=_str(entry.get("title")),
            url=_str(entry.get("url") or entry.get("webpage_url")),
        )
        for entry in raw_entries
        if entry
    )
    count = _opt_int(info.get("playlist_count"))
    return PlaylistMetadata(
        playlist_id=_str(info.get("id")),
        title=_str(info.get("title")),
        extractor=_str(info.get("extractor_key") or info.get("extractor")),
        webpage_url=_str(info.get("webpage_url") or info.get("original_url")),
        entry_count=count if count is not None else len(entries),
        entries=entries,
    )


def map_info(info: dict[str, Any]) -> ProbeResult:
    """Map a yt-dlp info dict to a single-media or playlist result."""
    if info.get("_type") == "playlist" or info.get("entries") is not None:
        return _map_playlist(info)
    return _map_media(info)
