# ADR — Use ASCII art as configurable assets

## Status
Accepted

## Context
The user wants waifu-style ASCII art after successful operations.

## Decision
Store ASCII art as UTF-8 text assets, render only when terminal width is sufficient, and allow custom local art.

## Consequences
Delightful UX; must avoid formatting breakage and allow disabling.

## Notes for AI agents
Do not reverse this decision without creating a new ADR and explicit user approval.
