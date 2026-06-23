# AGENTS.md — Agent Instructions

This file is compatible with Claude Code, Codex, Aider, GitHub Copilot coding agents, Cursor, and similar AI coding tools.

## Project summary
Transcriber is a Windows-only terminal TUI app for media downloads, GPU-only transcription, transcript cleanup, and organized output. It uses a modular monolith architecture with explicit boundaries, safety pipeline, dry-run-first execution, and rich terminal UX.

## Required context files
Read before modifying the project:

1. `PROJECT_SPEC_LOCK.md`
2. `SDD.md`
3. `GSD.md`
4. `ARCHITECTURE.md`
5. `ARCHITECTURE_CONSTITUTION.md`
6. `docs/adr/`
7. `ROADMAP.md`
8. `TASKS.md`

## Work rules
- Keep changes small and scoped.
- Do not rewrite unrelated code.
- Do not add dependencies without justification.
- Do not change architecture without ADR.
- Do not modify safety behavior without tests.
- Do not commit secrets or user data.
- Do not implement CPU fallback for transcription.
- Do not add cross-platform support yet.

## Architecture rules
- Core/domain code must be independent from UI, adapters, shell, filesystem side effects, network clients, and APIs.
- Application/use-case layer coordinates workflows.
- Ports define external contracts.
- Adapters implement ports.
- UI is only presentation and user interaction.
- Safety pipeline governs sensitive actions.
- Observability receives events and writes logs/reports safely.

## Quality gate
Before considering work complete:

```powershell
uv run ruff format --check .
uv run ruff check .
uv run pyright
uv run pytest
uv run python scripts/quality_gate.py
```

## Safety
Never expose, print, store, or commit:

- `.env`
- API keys
- WeatherAPI keys
- DeepSeek keys
- cookies
- tokens
- browser credentials
- private URLs with tokens
- logs with private data
- downloaded media
- generated transcripts

## UI requirements
- Rich + Questionary + Pyfiglet.
- Font `bloody` by default.
- Dark theme only.
- Language system: Portuguese and English.
- Startup animation always enabled.
- Clean screen mode.
- Success ASCII art if terminal is wide enough.

## Phase discipline
Do not skip phases. Do not proceed to the next phase until the current one is completed, tagged, released, and approved by the user.
