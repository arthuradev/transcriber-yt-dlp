# ADR — Use GPU-only faster-whisper transcription

## Status
Accepted

## Context
The owner has an NVIDIA GPU and explicitly wants no CPU fallback.

## Decision
Use faster-whisper through a transcription adapter and abort when CUDA/GPU is unavailable.

## Consequences
Performance is good on supported machines; users without GPU cannot use local transcription.

## Notes for AI agents
Do not reverse this decision without creating a new ADR and explicit user approval.
