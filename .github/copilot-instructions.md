# GitHub Copilot Instructions — Transcriber

Read `AGENTS.md`, `PROJECT_SPEC_LOCK.md`, `ARCHITECTURE.md`, and `ARCHITECTURE_CONSTITUTION.md` before making suggestions.

Do not suggest code that:

- commits secrets,
- adds CPU fallback to transcription,
- bypasses dry-run,
- places business logic in UI,
- imports adapters from core,
- uses shell commands unsafely,
- logs transcript content or cookies,
- adds cross-platform work before approved.

Prefer:

- typed Python,
- Pydantic config models,
- small functions,
- tests around safety and boundaries,
- explicit error classes,
- Rich/Questionary for TUI,
- ports/adapters for external systems.
