"""faster-whisper transcription adapter (GPU-only; no CPU fallback).

This is the only module that touches faster-whisper / ctranslate2 (an optional,
heavy, GPU-only dependency), so its imports are lazy (inside the default
functions) and type-suppressed here. The GPU check and the transcribe function
are injectable, so the engine is fully testable without a GPU or the optional
dependency installed.
"""
# faster-whisper / ctranslate2 are optional and untyped; isolate them here.
# pyright: reportMissingImports=false, reportMissingModuleSource=false
# pyright: reportMissingTypeStubs=false, reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false, reportUnknownArgumentType=false

from __future__ import annotations

from collections.abc import Callable

from transcriber.core.transcription import (
    Transcript,
    TranscriptionProgress,
    TranscriptionProgressCallback,
    TranscriptionRequest,
    TranscriptSegment,
)

GpuCheck = Callable[[], bool]
TranscribeFn = Callable[[TranscriptionRequest, TranscriptionProgressCallback], Transcript]


def _default_gpu_available() -> bool:
    try:
        import ctranslate2

        return ctranslate2.get_cuda_device_count() > 0
    except Exception:
        return False


def _default_transcribe(
    request: TranscriptionRequest, on_progress: TranscriptionProgressCallback
) -> Transcript:
    from faster_whisper import WhisperModel

    model = WhisperModel(request.model, device="cuda", compute_type="float16")
    segment_iter, info = model.transcribe(
        request.audio_path,
        language=request.language or None,
        task="translate" if request.translate else "transcribe",
    )
    total = float(getattr(info, "duration", 0.0) or 0.0)
    language = str(getattr(info, "language", "") or "")

    segments: list[TranscriptSegment] = []
    for segment in segment_iter:
        start = float(segment.start)
        end = float(segment.end)
        segments.append(TranscriptSegment(start=start, end=end, text=str(segment.text).strip()))
        on_progress(TranscriptionProgress(processed_seconds=end, total_seconds=total))

    return Transcript(language=language, segments=tuple(segments))


class FasterWhisperEngine:
    """Transcribes media via faster-whisper on CUDA."""

    def __init__(
        self,
        *,
        gpu_check: GpuCheck | None = None,
        transcribe_fn: TranscribeFn | None = None,
    ) -> None:
        self._gpu_check = gpu_check if gpu_check is not None else _default_gpu_available
        self._transcribe = transcribe_fn if transcribe_fn is not None else _default_transcribe

    def gpu_available(self) -> bool:
        return self._gpu_check()

    def transcribe(
        self,
        request: TranscriptionRequest,
        on_progress: TranscriptionProgressCallback,
    ) -> Transcript:
        return self._transcribe(request, on_progress)
