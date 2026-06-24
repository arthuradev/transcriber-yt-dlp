"""Download execution use case.

Executes a plan's items sequentially through the ``DownloadEnginePort``,
forwarding progress and aggregating results. Items already in the archive are
skipped; successful downloads are recorded in the archive to avoid future
duplicates. No I/O of its own beyond the injected engine/archive.
"""

from __future__ import annotations

from transcriber.core.archive import archive_key
from transcriber.core.download import (
    DownloadOutcome,
    DownloadRequest,
    DownloadResult,
    ProgressCallback,
)
from transcriber.core.plan import DownloadPlan
from transcriber.ports.archive import DownloadArchive
from transcriber.ports.media_engine import DownloadEnginePort


class DownloadExecutor:
    """Runs the download plan, skipping/recording duplicates, and collects results."""

    def __init__(
        self, engine: DownloadEnginePort, *, archive: DownloadArchive | None = None
    ) -> None:
        self._engine = engine
        self._archive = archive

    def execute(self, plan: DownloadPlan, *, on_progress: ProgressCallback) -> DownloadOutcome:
        results: list[DownloadResult] = []
        for item in plan.items:
            key = archive_key(item.extractor, item.media_id)
            if self._archive is not None and item.media_id and self._archive.contains(key):
                results.append(DownloadResult(ok=True, output_path=None, error=None, skipped=True))
                continue

            request = DownloadRequest(
                url=item.url,
                format_selector=plan.format_selector,
                output_path=item.output_path,
                extract_audio=plan.extract_audio,
                audio_format=plan.audio_format,
            )
            result = self._engine.download(request, on_progress)
            if result.ok and self._archive is not None and item.media_id:
                self._archive.add(key)
            results.append(result)
        return DownloadOutcome(results=tuple(results))
