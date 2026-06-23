# Tasks

## Current phase
Phase 3 — Themes, ASCII art, clean screen.

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
- [ ] Ask user permission to proceed to Phase 4.

## Backlog notes
- No functional media download yet.
- No weather implementation yet.
- No transcription implementation yet.
- Theme selection from settings/first-run and YAML ASCII config are Phase 4.
- Do not skip ahead.
