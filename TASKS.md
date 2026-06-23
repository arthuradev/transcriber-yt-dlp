# Tasks

## Current phase
Phase 2 — UI base (Rich/Questionary/Pyfiglet startup and menu).

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
- [ ] Ask user permission to proceed to Phase 3.

## Backlog notes
- No functional media download yet.
- No weather implementation yet.
- No transcription implementation yet.
- Theme selection and success-art clean-screen flow are Phase 3.
- Do not skip ahead.
