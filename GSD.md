# GSD — Guide for Software Development

## 1. Purpose
This guide explains how humans and AI coding agents must develop Transcriber without losing architectural consistency, breaking safety rules, or producing unreviewable changes.

## 2. Development model
Development is phase-based. Each phase has:

- a branch,
- a scope,
- acceptance criteria,
- tests,
- documentation updates,
- a changelog entry,
- an annotated tag,
- a GitHub Release,
- a user confirmation before the next phase.

## 3. AI workflow
Before implementation:

1. Read `PROJECT_SPEC_LOCK.md`.
2. Read the current phase file.
3. Identify impacted modules.
4. Check ADRs.
5. Plan changes briefly.
6. Implement within scope.
7. Add tests.
8. Run quality gates.
9. Update docs.
10. Commit and tag only when complete.

## 4. Scope discipline
Do not implement future phase features early unless they are necessary infrastructure for the current phase and documented clearly.

Bad:
- Building download engine during UI-only phase.
- Adding plugin system before module contracts exist.
- Adding GUI support during Windows TUI phase.

Good:
- Creating interfaces needed by current phase.
- Creating placeholders documented as non-functional.
- Adding tests for architecture boundaries early.

## 5. Change size
Prefer small commits. A commit should ideally represent one concept:

- `docs(adr): accept modular monolith`
- `feat(ui): add startup banner renderer`
- `test(config): validate first-run language choice`

## 6. Documentation update rules
Update documentation when:

- behavior changes,
- architecture changes,
- commands change,
- config schema changes,
- safety policy changes,
- a new dependency is added,
- a phase completes.

Create or update ADR when:

- an architectural decision is made,
- a technology choice becomes binding,
- a boundary rule changes,
- a safety principle changes.

## 7. Quality gate
Every phase must pass:

```powershell
uv run ruff format --check .
uv run ruff check .
uv run pyright
uv run pytest
uv run python scripts/quality_gate.py
```

## 8. When to stop
Stop and ask the user when:

- phase is complete,
- a quality gate cannot pass,
- a required dependency cannot be installed/tested,
- a decision would change the approved architecture,
- there is a risk of exposing secrets,
- the requested behavior conflicts with safety policy.

## 9. Phase completion checklist
Use `docs/checklists/phase-completion.md`.

## 10. Release checklist
Use `docs/checklists/release.md`.
