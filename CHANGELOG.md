# Changelog

All notable changes to Transcriber will be documented in this file.

The project follows phase tags: `v0.1.0`, `v0.2.0`, ...

## [Unreleased]

### Planned
- Phase 4: Config, language, and first-run setup.

## [v0.3.0] - 2026-06-23

### Added
- Dark theme registry with six themes (default, purple, red, blue, monochrome,
  anime); `build_console(theme_name)` selects one, all sharing the same style
  keys.
- ASCII art renderer (`transcriber.ui.ascii_art`): UTF-8 loading, cell-accurate
  width measurement (correct for Unicode/braille art), terminal-fit checks,
  random selection, and no-wrap centered rendering that preserves raw lines.
- Clean-screen success flow (`transcriber.ui.screens`): `clear_screen` and
  `show_success_screen` (summary panel + optional success art + minimum display
  time + Press-Enter-to-return), with injectable sleep for testability.
- Welcome art at startup: the shell renders a fitting welcome art under the
  banner; `python -m transcriber` discovers `assets/ascii/welcome` and picks one.
- `.gitattributes` normalizing line endings to LF.

### Changed
- `build_console` now takes an optional theme name (defaults to `default`).
- `AppShell` accepts `theme_name` and `welcome_art`.
- CI actions bumped (checkout v7, setup-python v6, setup-uv v8) to run on
  Node 24 and clear the Node 20 deprecation warning.

### Tests
- Added theme, ASCII art, and success-screen tests.

### Notes
- Theme *selection from settings/first-run* and YAML-driven ASCII config are
  Phase 4; the renderer/registry contracts are in place now.
- No download/transcription/cleanup behavior yet.

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
