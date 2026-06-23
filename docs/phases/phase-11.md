# Phase 11 — GPU-only transcription

## Tag
`v0.11.0`

## Branch
`phase/11-gpu-only-transcription`

## Goal
Implement faster-whisper adapter, GPU checks, audio extraction, raw transcript output.

## Explicit non-scope
No CPU fallback.

## Required work
- Follow architecture rules.
- Add or update tests.
- Update documentation if behavior/config/architecture changes.
- Update `CHANGELOG.md`.
- Update `TASKS.md`.
- Run quality gates.

## Acceptance criteria
- Phase goal is implemented.
- No out-of-scope work is included.
- Quality gates pass.
- No secrets/private files are committed.
- Phase branch is merged into `main`.
- Annotated tag `v0.11.0` is created.
- GitHub Release for `v0.11.0` is created.
- Claude asks the user whether to proceed to Phase 12.

## Release note template
```md
## v0.11.0 — Phase 11: GPU-only transcription

### Added
- ...

### Changed
- ...

### Fixed
- ...

### Tests
- ...

### Known limitations
- ...
```
