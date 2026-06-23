# Changelog

All notable changes to Transcriber will be documented in this file.

The project follows phase tags: `v0.1.0`, `v0.2.0`, ...

## [Unreleased]

### Planned
- Phase 3: Themes, ASCII art, and clean-screen success flow.

## [v0.2.0] - 2026-06-23

### Added
- TUI shell (`transcriber.ui`): shared themed Rich console and a default dark
  theme palette.
- Startup banner using Pyfiglet (`bloody` font) with a fallback font, plus the
  `Download • Transcription • Cleanup` subtitle.
- Always-on startup animation that plays only on a real terminal (no-op on
  captured/non-interactive streams).
- Main menu via Questionary (`MenuAction` / `MAIN_MENU`) with the eight initial
  options; non-exit actions render a "Coming soon" placeholder.
- `AppShell` main loop with an injectable action selector for testability;
  `python -m transcriber` now launches the shell.
- UI unit tests (banner, menu, animation, shell) and an architecture test
  asserting the UI layer never imports adapters.

### Changed
- `python -m transcriber` now starts the TUI instead of printing a skeleton
  notice.

### Dependencies
- Added runtime dependencies: `rich`, `questionary`, `pyfiglet` (per ADR 0003).

### Notes
- Menu actions are placeholders; no download/transcription/cleanup behavior yet.
- Theme *selection* and the post-operation success-art clean-screen flow arrive
  in Phase 3.

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
