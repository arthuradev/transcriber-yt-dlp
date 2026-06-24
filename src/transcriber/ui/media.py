"""Render probed media metadata before any download."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from transcriber.core.media import MediaMetadata, PlaylistMetadata, ProbeResult
from transcriber.ui.i18n import Translator

_MAX_FORMATS = 20
_MAX_ENTRIES = 15


def format_duration(seconds: float | None) -> str:
    """Format a duration in seconds as ``H:MM:SS`` (or ``M:SS``)."""
    if seconds is None:
        return "?"
    total = int(seconds)
    hours, remainder = divmod(total, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def format_size(num: int | None) -> str:
    """Format a byte count as a human-readable size."""
    if num is None:
        return "?"
    size = float(num)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024:
            return f"{size:.0f} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} PB"


def render_metadata(console: Console, result: ProbeResult, translator: Translator) -> None:
    """Render probed metadata (single item or playlist) to the console."""
    if isinstance(result, PlaylistMetadata):
        _render_playlist(console, result, translator)
    else:
        _render_media(console, result, translator)


def _render_media(console: Console, media: MediaMetadata, t: Translator) -> None:
    table = Table(show_header=False, box=None)
    table.add_column(style="muted")
    table.add_column(style="info")
    table.add_row(t("media.title"), media.title or "?")
    table.add_row(t("media.site"), media.extractor or "?")
    table.add_row(t("media.duration"), format_duration(media.duration_seconds))
    if media.uploader:
        table.add_row(t("media.uploader"), media.uploader)
    subtitle_langs = media.subtitle_languages or media.auto_caption_languages
    if subtitle_langs:
        table.add_row(t("media.subtitles"), ", ".join(subtitle_langs))
    table.add_row(t("media.url"), media.webpage_url or "?")
    console.print(Panel(table, title=t("media.metadata_title"), border_style="accent"))
    if media.formats:
        _render_formats(console, media, t)


def _render_formats(console: Console, media: MediaMetadata, t: Translator) -> None:
    table = Table(title=t("media.formats"), title_style="menu.title")
    table.add_column("id", style="muted")
    table.add_column("ext")
    table.add_column("res")
    table.add_column("size")
    table.add_column("vcodec")
    table.add_column("acodec")
    for fmt in media.formats[:_MAX_FORMATS]:
        resolution = f"{fmt.height}p" if fmt.height else (fmt.note or "")
        table.add_row(
            fmt.format_id,
            fmt.ext,
            resolution,
            format_size(fmt.filesize),
            fmt.vcodec or "",
            fmt.acodec or "",
        )
    console.print(table)
    extra = len(media.formats) - _MAX_FORMATS
    if extra > 0:
        console.print(f"[muted]{t('media.more_formats', count=extra)}[/muted]")


def _render_playlist(console: Console, playlist: PlaylistMetadata, t: Translator) -> None:
    table = Table(show_header=False, box=None)
    table.add_column(style="muted")
    table.add_column(style="info")
    table.add_row(t("media.playlist"), playlist.title or "?")
    table.add_row(t("media.site"), playlist.extractor or "?")
    table.add_row(t("media.items"), str(playlist.entry_count))
    table.add_row(t("media.url"), playlist.webpage_url or "?")
    console.print(Panel(table, title=t("media.metadata_title"), border_style="accent"))
    for entry in playlist.entries[:_MAX_ENTRIES]:
        console.print(f"[muted]-[/muted] {entry.title or entry.media_id or '?'}")
    extra = len(playlist.entries) - _MAX_ENTRIES
    if extra > 0:
        console.print(f"[muted]{t('media.more_items', count=extra)}[/muted]")
