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
No numeric coverage gate initially. Add 70% target later. Make it mandatory by Phase 16.
