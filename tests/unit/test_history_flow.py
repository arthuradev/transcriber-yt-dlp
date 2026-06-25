"""Tests for the history view flow."""

from __future__ import annotations

import io
from datetime import UTC, datetime

from rich.console import Console

from transcriber.config.models import Language
from transcriber.core.history import HistoryEntry
from transcriber.ui.history_flow import HistoryFlow
from transcriber.ui.i18n import Translator


class _History:
    def __init__(self, entries: list[HistoryEntry]) -> None:
        self._entries = entries

    def add(self, entry: HistoryEntry) -> None:
        self._entries.append(entry)

    def recent(self, limit: int = 20) -> list[HistoryEntry]:
        return self._entries[:limit]


def _entry(kind: str = "download", status: str = "ok") -> HistoryEntry:
    return HistoryEntry(datetime(2026, 6, 24, 14, 30, tzinfo=UTC), kind, status, 1, 1, 0, 0, "d")


def test_history_renders_entries(console_buffer: tuple[Console, io.StringIO]) -> None:
    console, buffer = console_buffer
    history = _History([_entry("download", "ok"), _entry("transcribe", "failed")])
    HistoryFlow(history=history, console=console, translator=Translator(Language.EN_US)).run()
    output = buffer.getvalue()
    assert "Recent operations" in output
    assert "download" in output
    assert "transcribe" in output
    assert "2026-06-24 14:30" in output


def test_history_empty(console_buffer: tuple[Console, io.StringIO]) -> None:
    console, buffer = console_buffer
    HistoryFlow(history=_History([]), console=console, translator=Translator(Language.EN_US)).run()
    assert "No history yet" in buffer.getvalue()
