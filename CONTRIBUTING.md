# Contributing

Transcriber is developed phase-by-phase. Contributions must respect the architecture, safety rules, and quality gates.

## Requirements
- Windows environment for app behavior.
- Python 3.12+.
- uv.
- Git.

## Setup
```powershell
uv sync
uv run pytest
```

## Before submitting changes
```powershell
uv run ruff format --check .
uv run ruff check .
uv run pyright
uv run pytest
uv run python scripts/quality_gate.py
```

## Commit style
Use Conventional Commits:

```text
feat(ui): add startup banner
fix(config): handle missing language setting
docs(adr): record packaging decision
test(safety): cover high-risk confirmation
```

## Architecture
Read `ARCHITECTURE.md` and `ARCHITECTURE_CONSTITUTION.md` before changing module boundaries.

## Security
Never commit secrets, cookies, private configs, logs, transcripts, or downloaded media.
