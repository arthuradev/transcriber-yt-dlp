"""Tests for the download executor."""

from __future__ import annotations

from collections.abc import Callable

from transcriber.application.executor import DownloadExecutor
from transcriber.core.download import (
    DownloadProgress,
    DownloadRequest,
    DownloadResult,
    DownloadStatus,
)
from transcriber.core.operations import RiskLevel
from transcriber.core.plan import DownloadPlan, PlannedItem


def _plan(
    items: tuple[PlannedItem, ...],
    *,
    profile_id: str = "video_best",
    format_selector: str = "bv*+ba/b",
    extract_audio: bool = False,
    audio_format: str | None = None,
) -> DownloadPlan:
    return DownloadPlan(
        profile_id=profile_id,
        format_selector=format_selector,
        output_dir="out",
        is_playlist=False,
        items=items,
        risk=RiskLevel.MEDIUM,
        requires_confirmation=True,
        requires_strong_confirmation=False,
        requires_ffmpeg=True,
        warnings=(),
        extract_audio=extract_audio,
        audio_format=audio_format,
        is_downloadable=True,
    )


class _Engine:
    def __init__(self, result_for: Callable[[DownloadRequest], DownloadResult]) -> None:
        self._result_for = result_for
        self.requests: list[DownloadRequest] = []

    def download(
        self,
        request: DownloadRequest,
        on_progress: Callable[[DownloadProgress], None],
    ) -> DownloadResult:
        self.requests.append(request)
        on_progress(DownloadProgress(DownloadStatus.DOWNLOADING, 50, 100, None, None, None))
        on_progress(DownloadProgress(DownloadStatus.FINISHED, 100, 100, None, None, None))
        return self._result_for(request)


class _Archive:
    def __init__(self, existing: set[str] | None = None) -> None:
        self._keys: set[str] = set(existing) if existing else set()
        self.added: list[str] = []

    def contains(self, key: str) -> bool:
        return key in self._keys

    def add(self, key: str) -> None:
        self._keys.add(key)
        self.added.append(key)


def test_executor_success() -> None:
    item = PlannedItem("T", "id", "https://x", "out/T.mp4")
    engine = _Engine(lambda r: DownloadResult(True, r.output_path, None))
    calls: list[DownloadProgress] = []
    outcome = DownloadExecutor(engine).execute(_plan((item,)), on_progress=calls.append)
    assert outcome.ok
    assert outcome.succeeded == 1
    assert outcome.failed == 0
    assert outcome.output_paths == ("out/T.mp4",)
    assert engine.requests[0].url == "https://x"
    assert engine.requests[0].format_selector == "bv*+ba/b"
    assert len(calls) == 2


def test_executor_failure() -> None:
    item = PlannedItem("T", "id", "https://x", "out/T.mp4")
    engine = _Engine(lambda r: DownloadResult(False, None, "boom"))
    outcome = DownloadExecutor(engine).execute(_plan((item,)), on_progress=lambda p: None)
    assert not outcome.ok
    assert outcome.failed == 1
    assert outcome.output_paths == ()


def test_executor_passes_audio_options() -> None:
    item = PlannedItem("T", "id", "https://x", "out/T.mp3")
    plan = _plan(
        (item,),
        profile_id="audio_mp3",
        format_selector="ba/b",
        extract_audio=True,
        audio_format="mp3",
    )
    engine = _Engine(lambda r: DownloadResult(True, r.output_path, None))
    DownloadExecutor(engine).execute(plan, on_progress=lambda p: None)
    assert engine.requests[0].extract_audio is True
    assert engine.requests[0].audio_format == "mp3"


def test_executor_skips_archived_items() -> None:
    item = PlannedItem("T", "id", "https://x", "out/T.mp4", extractor="Yt")
    engine = _Engine(lambda r: DownloadResult(True, r.output_path, None))
    archive = _Archive({"Yt:id"})
    outcome = DownloadExecutor(engine, archive=archive).execute(
        _plan((item,)), on_progress=lambda p: None
    )
    assert outcome.skipped == 1
    assert outcome.succeeded == 0
    assert engine.requests == []


def test_executor_records_success_in_archive() -> None:
    item = PlannedItem("T", "id", "https://x", "out/T.mp4", extractor="Yt")
    engine = _Engine(lambda r: DownloadResult(True, r.output_path, None))
    archive = _Archive()
    DownloadExecutor(engine, archive=archive).execute(_plan((item,)), on_progress=lambda p: None)
    assert "Yt:id" in archive.added
