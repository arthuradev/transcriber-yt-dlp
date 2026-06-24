"""Test that the download flow records history via the recorder."""

from __future__ import annotations

import io
from collections.abc import Callable, Sequence
from datetime import date

from rich.console import Console

from transcriber.application.executor import DownloadExecutor
from transcriber.application.planner import DownloadPlanner
from transcriber.application.probe import MediaProbeService
from transcriber.config.models import Language, PathsConfig
from transcriber.core.download import (
    DownloadProgress,
    DownloadRequest,
    DownloadResult,
    DownloadStatus,
)
from transcriber.core.history import HistoryEntry
from transcriber.core.media import MediaFormat, MediaMetadata, ProbeResult
from transcriber.core.profiles import DownloadProfile
from transcriber.observability.recorder import OperationRecorder
from transcriber.ui.download_flow import DownloadFlow, DownloadSource
from transcriber.ui.i18n import Translator


class _Engine:
    def probe(self, url: str) -> ProbeResult:
        return MediaMetadata("abc", "V", "Yt", "https://x/abc", 10.0, None, ())

    def download(
        self,
        request: DownloadRequest,
        on_progress: Callable[[DownloadProgress], None],
    ) -> DownloadResult:
        on_progress(DownloadProgress(DownloadStatus.FINISHED, 1, 1, None, None, None))
        return DownloadResult(True, request.output_path, None)


class _Prompts:
    def ask_source(self) -> DownloadSource | None:
        return DownloadSource(is_batch=False, value="https://x/abc")

    def select_profile(self, profiles: Sequence[DownloadProfile]) -> DownloadProfile | None:
        return next((p for p in profiles if p.profile_id == "video_best"), None)

    def select_format(self, formats: Sequence[MediaFormat]) -> MediaFormat | None:
        return None

    def ask_output_dir(self, default: str) -> str:
        return "out"

    def confirm(self, *, strong: bool) -> bool:
        return True

    def confirm_cookies(self) -> bool:
        return False


class _History:
    def __init__(self) -> None:
        self.entries: list[HistoryEntry] = []

    def add(self, entry: HistoryEntry) -> None:
        self.entries.append(entry)

    def recent(self, limit: int = 20) -> list[HistoryEntry]:
        return list(self.entries)


def test_flow_records_history(console_buffer: tuple[Console, io.StringIO]) -> None:
    console, _ = console_buffer
    engine = _Engine()
    history = _History()
    DownloadFlow(
        probe_service=MediaProbeService(engine),
        planner=DownloadPlanner(today=lambda: date(2026, 6, 24)),
        console=console,
        translator=Translator(Language.EN_US),
        paths=PathsConfig(download_dir="out"),
        prompts=_Prompts(),
        executor=DownloadExecutor(engine),
        recorder=OperationRecorder(history=history),
    ).run("video")
    assert len(history.entries) == 1
    assert history.entries[0].kind == "download"
    assert history.entries[0].status == "ok"
