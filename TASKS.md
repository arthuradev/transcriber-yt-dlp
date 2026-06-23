# Tasks

## Current phase
Phase 5 — WeatherAPI and personalization.

## Phase 1 checklist
- [x] Create public GitHub repository `transcriber-yt-dlp`.
- [x] Add Apache-2.0 license.
- [x] Add documentation pack.
- [x] Add `src/` layout skeleton.
- [x] Add `pyproject.toml` with uv, ruff, pytest, pyright.
- [x] Add `.gitignore` and `.env.example`.
- [x] Add GitHub Actions quality gate.
- [x] Add `scripts/quality_gate.py` placeholder/initial validator.
- [x] Add architecture boundary test skeleton.
- [x] Update CHANGELOG.
- [x] Commit using Conventional Commits.
- [x] Merge to `main`.
- [x] Create annotated tag `v0.1.0`.
- [x] Create GitHub Release for `v0.1.0`.
- [x] Ask user permission to proceed to Phase 2.

## Phase 2 checklist
- [x] Add `rich`, `questionary`, `pyfiglet` runtime dependencies.
- [x] Add shared themed console and default dark theme palette.
- [x] Add Pyfiglet startup banner (`bloody` font) and subtitle.
- [x] Add always-on startup animation (terminal-only).
- [x] Add Questionary main menu with the eight initial options.
- [x] Add `AppShell` main loop with placeholder actions.
- [x] Wire `python -m transcriber` to launch the TUI.
- [x] Add UI tests and a UI->adapters architecture boundary test.
- [x] Update CHANGELOG and TASKS.
- [x] Run quality gates.
- [x] Commit, merge to `main`, tag `v0.2.0`, GitHub Release.
- [x] Ask user permission to proceed to Phase 3.

## Phase 3 checklist
- [x] Add dark theme registry (default, purple, red, blue, monochrome, anime).
- [x] Make `build_console`/`AppShell` theme-aware.
- [x] Add ASCII art renderer with cell-accurate width and fit checks.
- [x] Add no-wrap centered rendering with compact fallback.
- [x] Add clean-screen success flow (`show_success_screen`).
- [x] Wire welcome art at startup.
- [x] Add theme/ascii/screen tests.
- [x] Housekeeping: add `.gitattributes`; bump CI action versions.
- [x] Update CHANGELOG and TASKS.
- [x] Run quality gates.
- [x] Commit, merge to `main`, tag `v0.3.0`, GitHub Release.
- [x] Ask user permission to proceed to Phase 4.

## Phase 4 checklist
- [x] Add Pydantic user-config models and `Language` enum.
- [x] Add YAML config persistence (`ConfigStore`) + `ConfigRepository` port.
- [x] Add i18n `Translator` with pt-BR / en-US catalog.
- [x] Localize menu/shell strings.
- [x] Add first-run wizard (`FirstRunService` + `FirstRunPrompts` port + UI impl).
- [x] Wire first-run/config load into startup.
- [x] Keep secrets in `.env` (ADR 0013); none in persisted config.
- [x] Add config/i18n/first-run tests + application boundary test.
- [x] Update CHANGELOG and TASKS; add configuration design doc.
- [x] Run quality gates.
- [x] Commit, merge to `main`, tag `v0.4.0`, GitHub Release.
- [x] Ask user permission to proceed to Phase 5.

## Phase 5 checklist
- [x] Add `WeatherSnapshot`/`WeatherError` domain + `WeatherPort`.
- [x] Add `WeatherApiAdapter` (injectable transport, key redaction).
- [x] Add `WeatherService` with TTL cache and graceful degradation.
- [x] Add weather display + discreet unavailable warning; wire into header.
- [x] Read key from `.env` via `config.secrets`; never log it.
- [x] Ensure weather never blocks startup.
- [x] Add weather adapter/service/ui tests.
- [x] Update CHANGELOG, TASKS, weather design doc.
- [x] Run quality gates.
- [x] Commit, merge to `main`, tag `v0.5.0`, GitHub Release.
- [ ] Ask user permission to proceed to Phase 6.

## Backlog notes
- No functional media download yet (Phase 6 adds yt-dlp metadata probe).
- No transcription implementation yet.
- API keys live in `.env`, never in config.yaml.
- Do not skip ahead.
