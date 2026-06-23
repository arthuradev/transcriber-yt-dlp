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
