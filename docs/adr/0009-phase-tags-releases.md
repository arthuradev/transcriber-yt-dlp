# ADR — Use phase branches, annotated tags, and releases

## Status
Accepted

## Context
The owner wants controlled phase progress and tags for each phase.

## Decision
Each phase uses a branch, merges to main, gets annotated tag `v0.x.0`, GitHub Release, and user approval before next phase.

## Consequences
Clear history and rollback points; extra release discipline.

## Notes for AI agents
Do not reverse this decision without creating a new ADR and explicit user approval.
