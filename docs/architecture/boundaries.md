# Architecture Boundaries

## Forbidden imports
- `core` must not import `adapters`, `ui`, `subprocess`, `requests`, `httpx`, API clients, or filesystem-mutating code.
- `application` must not import concrete external clients directly.
- `ui` must not implement business rules or perform side effects directly.

## Required tests
Add architecture tests under `tests/architecture/`.

Minimum checks:

- core has no adapter imports,
- core has no UI imports,
- core has no subprocess/network imports,
- application does not import concrete API adapters,
- all sensitive operations reference safety pipeline.
