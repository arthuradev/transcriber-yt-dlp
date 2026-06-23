# ADR — Package as Windows exe after core stability

## Status
Accepted

## Context
Final users may not have Python installed and need easy startup.

## Decision
Use PyInstaller later for portable exe and Inno Setup for installer after core features are stable.

## Consequences
Better UX for non-technical users; packaging complexity deferred.

## Notes for AI agents
Do not reverse this decision without creating a new ADR and explicit user approval.
