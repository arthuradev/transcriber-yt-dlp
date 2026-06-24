# Transcription Design

## Engine
Use faster-whisper through `TranscriptionEnginePort`.

## GPU-only policy
- Device: CUDA.
- CPU fallback: forbidden.
- If CUDA is unavailable, abort with helpful instructions.

## Default
- Model: `large-v3`.
- Language: auto.
- Translation: supported.

## Outputs
- raw transcript,
- cleaned transcript if LLM cleanup is used,
- `.txt`, `.md`, `.srt`, `.vtt`, `.json`,
- `.docx` and `.pdf` later.

## Temporary files
Delete extracted audio by default. Allow user to keep intermediates.

## Implementation (Phase 11)
- `core.transcription` — pure domain: `TranscriptionRequest`,
  `TranscriptionProgress`, `TranscriptSegment`, `Transcript`, `TranscriptionError`.
- `core.transcript_format` — pure serializers: `to_txt`/`to_md`/`to_srt`/`to_vtt`/
  `to_json`.
- `ports.transcription.TranscriptionEnginePort` — `gpu_available()` +
  `transcribe(request, on_progress)`.
- `adapters.faster_whisper_engine.FasterWhisperEngine` — the only module touching
  faster-whisper/ctranslate2 (lazy, type-suppressed imports). GPU check and the
  transcribe function are injectable; without CUDA/the dependency, `gpu_available`
  returns `False`. Audio is decoded by faster-whisper directly (video files work).
- `application.transcription.TranscriptionService` — enforces GPU-only: aborts
  with `TranscriptionError` if no GPU (no CPU fallback) before doing any work.
- `storage.transcript_store.save_transcript` — writes the raw transcript.
- `ui.transcribe_flow.TranscribeFlow` — local-file → transcribe → save, wired to
  the "Transcribe local file" menu action.

faster-whisper is an **optional** extra (`pip install transcriber[transcription]`)
because it is a heavy GPU-only stack; it is not installed by default or in CI.
Real GPU transcription is therefore not exercised by the automated tests (which
use injected fakes).
