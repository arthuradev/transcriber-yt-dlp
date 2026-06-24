"""Tests for the download flow execution path (with an injected executor)."""

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
from transcriber.core.media import MediaFormat, MediaMetadata, ProbeResult
from transcriber.core.profiles import DownloadProfile
from transcriber.ui.download_flow import DownloadFlow, DownloadSource
from transcriber.ui.i18n import Translator


class _Engine:
    def __init__(self, probe_result: ProbeResult, download_result: DownloadResult) -> None:
        self._probe = probe_result
        self._download = download_result

    def probe(self, url: str) -> ProbeResult:
        return self._probe

    def download(
        self,
        request: DownloadRequest,
        on_progress: Callable[[DownloadProgress], None],
    ) -> DownloadResult:
        on_progress(DownloadProgress(DownloadStatus.FINISHED, 1, 1, None, None, None))
        return self._download


class _ScriptedPrompts:
    def __init__(self, *, url: str, profile_id: str, output_dir: str, confirm: bool) -> None:
        self._url = url
        self._profile_id = profile_id
        self._output_dir = output_dir
        self._confirm = confirm

    def ask_source(self) -> DownloadSource | None:
        return DownloadSource(is_batch=False, value=self._url)

    def select_profile(self, profiles: Sequence[DownloadProfile]) -> DownloadProfile | None:
        return next((p for p in profiles if p.profile_id == self._profile_id), None)

    def select_format(self, formats: Sequence[MediaFormat]) -> MediaFormat | None:
        return None

    def ask_output_dir(self, default: str) -> str:
        return self._output_dir

    def confirm(self, *, strong: bool) -> bool:
        return self._confirm


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


def _flow(console: Console, engine: _Engine, prompts: _ScriptedPrompts) -> DownloadFlow:
    return DownloadFlow(
        probe_service=MediaProbeService(engine),
        planner=DownloadPlanner(today=lambda: date(2026, 6, 24)),
        console=console,
        translator=Translator(Language.EN_US),
        paths=PathsConfig(download_dir="out"),
        prompts=prompts,
        executor=DownloadExecutor(engine),
    )


def test_flow_executes_and_summarizes(console_buffer: tuple[Console, io.StringIO]) -> None:
    console, buffer = console_buffer
    engine = _Engine(_media(), DownloadResult(True, "out/My Video [abc].mp4", None))
    prompts = _ScriptedPrompts(
        url="https://x/abc", profile_id="video_best", output_dir="out", confirm=True
    )
    _flow(console, engine, prompts).run("video")
    output = buffer.getvalue()
    assert "My Video" in output
    assert "Download complete" in output
    assert "Execution will be available" not in output


def test_flow_reports_failure(console_buffer: tuple[Console, io.StringIO]) -> None:
    console, buffer = console_buffer
    engine = _Engine(_media(), DownloadResult(False, None, "network error"))
    prompts = _ScriptedPrompts(
        url="https://x/abc", profile_id="video_best", output_dir="out", confirm=True
    )
    _flow(console, engine, prompts).run("video")
    output = buffer.getvalue()
    assert "Download failed" in output


def test_flow_transcript_profile_is_not_executed(
    console_buffer: tuple[Console, io.StringIO],
) -> None:
    console, buffer = console_buffer
    engine = _Engine(_media(), DownloadResult(True, "x", None))
    prompts = _ScriptedPrompts(
        url="https://x/abc", profile_id="transcript_only", output_dir="out", confirm=True
    )
    _flow(console, engine, prompts).run("transcript")
    output = buffer.getvalue()
    assert "Execution will be available" in output
    assert "Download complete" not in output
