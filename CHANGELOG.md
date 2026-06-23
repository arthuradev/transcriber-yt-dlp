# Changelog

All notable changes to Transcriber will be documented in this file.

The project follows phase tags: `v0.1.0`, `v0.2.0`, ...

## [Unreleased]

### Planned
- Phase 2: UI base (Rich/Questionary/Pyfiglet startup and menu).

## [v0.1.0] - 2026-06-23

### Added
- Public repository skeleton and documentation pack.
- Modular-monolith `src/transcriber` package layout (core, application, ports,
  adapters, ui, safety, storage, observability, config, assets).
- Pure core domain content: structured `AppError`/`ErrorSeverity` and the
  `OperationType`/`RiskLevel` enumerations.
- Non-functional `python -m transcriber` entry point.
- `scripts/quality_gate.py` validator (secret-file, package-structure, and
  core import-boundary checks).
- Architecture boundary tests and core unit tests.
- uv-based build (hatchling) with a `dev` dependency group; GitHub Actions CI.

### Notes
- No functional download/transcription/cleanup features yet.
