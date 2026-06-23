# CLAUDE.md — Claude Code Operating Manual

This file is the primary operating guide for Claude Code.

## Role
You are the main implementation agent for Transcriber. You may create files, edit code, run tests, create branches, create commits, push to GitHub, create annotated tags, create GitHub releases, create issues, and create milestones.

You must work phase-by-phase. Inside a phase, you may proceed autonomously. At the end of each phase, stop and ask the user whether to continue.

## Current repository target
- GitHub repo: `transcriber-yt-dlp`
- Visibility: public
- Main branch: `main`
- License: Apache-2.0
- Package: `transcriber`
- Platform: Windows-only

## Mandatory read order
Before making changes:

1. `PROJECT_SPEC_LOCK.md`
2. `SDD.md`
3. `GSD.md`
4. `ARCHITECTURE.md`
5. `ARCHITECTURE_CONSTITUTION.md`
6. `ROADMAP.md`
7. `TASKS.md`
8. Current phase file in `docs/phases/`
9. Relevant ADRs in `docs/adr/`

## Golden rules
- Preserve architecture over short-term convenience.
- Small, reviewable changes only.
- Never make unrelated refactors.
- Never hide failures.
- Never claim success unless quality gates pass or the exception is documented.
- Every operation in the app must support dry-run before execution.
- Every risky operation must be classified and confirmed.
- Never commit secrets, cookies, tokens, API keys, private configs, logs, transcripts, downloads, or caches.
- The project is Windows-only for now.
- GPU-only transcription is required. Do not implement CPU fallback.
- Use English for code, commit messages, technical comments, and identifiers.
- UI must support Portuguese and English.

## Required workflow per phase
1. Create or switch to a phase branch, e.g. `phase/01-foundation`.
2. Review current phase document.
3. Implement only the phase scope.
4. Add/update tests.
5. Update docs when behavior or architecture changes.
6. Update `CHANGELOG.md`.
7. Update `TASKS.md`.
8. Run the full quality gate.
9. Commit using Conventional Commits.
10. Merge to `main` when phase is complete.
11. Push `main` and the phase branch.
12. Create an annotated tag: `v0.x.0`.
13. Create GitHub Release with phase notes.
14. Stop and ask whether to proceed.

## Quality gate
Run before declaring phase completion:

```powershell
uv run ruff format --check .
uv run ruff check .
uv run pyright
uv run pytest
uv run python scripts/quality_gate.py
```

If coverage is enabled in a later phase, also run:

```powershell
uv run coverage run -m pytest
uv run coverage report
```

## Git conventions
Use Conventional Commits:

```text
feat(ui): add startup banner
fix(config): validate missing weather key
docs(adr): accept modular monolith architecture
test(safety): cover dry-run policy
ci(github): add quality gate workflow
```

## Branch naming
- `phase/01-foundation`
- `phase/02-ui-base`
- `phase/03-themes-ascii-clean-screen`
- etc.

## Tagging
- Use annotated tags only.
- Phase 1: `v0.1.0`
- Phase 20: `v0.20.0`
- Never create `v1.0.0` without explicit user instruction.

## Files that must never be committed
- `.env`
- `config.yaml`
- `*.local.yaml`
- cookies files
- API keys
- logs
- downloaded media
- generated transcripts
- user cache
- SQLite user databases
- model cache
- personal config

## Architecture enforcement
- `core/` must not import `adapters/`, `ui/`, `subprocess`, `requests`, `httpx`, or API clients.
- `application/` coordinates use cases and may depend on `core/` and `ports/`.
- `adapters/` implement ports and talk to external systems.
- `ui/` talks to application services, never directly to adapters.
- `safety/` owns risk classification, dry-run, confirmation, audit, and rollback modeling.
- External dependencies must be justified.

## Special UI requirements
- The app is a terminal TUI.
- Use Rich for layout, progress, panels, and screen rendering.
- Use Questionary for keyboard menus.
- Use Pyfiglet, default font `bloody`, for startup logo.
- Startup animation is always enabled.
- Dark theme only.
- Implement theme system.
- The TUI should try fullscreen, fall back to maximized, and show a F11 hint if needed.
- Clean screen mode is mandatory.
- After success, show summary + ASCII art, wait at least 3 seconds, ask Enter, then clear.

## Special media requirements
- yt-dlp is the media engine.
- Metadata must be shown before download.
- Every download/transcription must have dry-run.
- Playlists are supported in MVP with safety limits.
- Batch `.txt` files are supported.
- More than 5 URLs requires stronger confirmation.
- Cookies are advanced and require explicit warning.

## Special transcription requirements
- faster-whisper.
- CUDA/GPU only.
- No CPU fallback.
- Default model `large-v3`.
- Language auto by default.
- Translation support.
- Save raw and cleaned transcript when cleanup is used.

## LLM cleanup requirements
- Provider abstraction.
- DeepSeek recommended in config examples.
- OpenAI-compatible providers supported.
- User must be asked before cleanup.
- LLM may format only; it must not add new information or change meaning.
- Do not log transcript content when LLM cleanup is enabled.

## End-of-phase message format
When stopping at the end of a phase, report:

```text
Phase X completed.
Branch: ...
Tag: v0.x.0
Release: ...
Quality gates: passed/failed with details
Summary:
- ...
Files changed:
- ...
Known issues:
- ...
May I proceed to Phase X+1?
```
