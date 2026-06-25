# Testing Strategy

## Tools
- pytest
- ruff
- pyright
- pydantic validation
- coverage later

## Early tests
- config schema,
- language selection,
- theme loading,
- ASCII renderer width fallback,
- path guard,
- risk classifier,
- dry-run builder,
- architecture boundaries.

## Later tests
- yt-dlp adapter with mocks,
- progress events,
- transcription adapter with fakes,
- LLM cleanup chunking,
- history/archive,
- packaging scripts.

## Coverage
A 70% line-coverage gate is **mandatory** from Phase 16 (`[tool.coverage.report]
fail_under = 70`). `__main__.py` (the composition root) is omitted. Run locally:

```powershell
uv run coverage run -m pytest
uv run coverage report
```

(If `uv run coverage` is blocked by Windows App Control locally, use
`uv run python -m coverage ...`.) CI runs the coverage gate on every push.

## Architecture tests
`tests/architecture/test_boundaries.py` enforces the layered dependency rules
data-driven: each layer is scanned with `ast` for forbidden imports. Core stays
pure; ports/safety depend only inward; application avoids ui/adapters/storage/
observability; ui never imports adapters; etc.

## Integration tests
`tests/integration/` exercises multiple real components together (e.g.
plan -> execute -> archive -> history -> report) with fakes only at the external
boundary.
