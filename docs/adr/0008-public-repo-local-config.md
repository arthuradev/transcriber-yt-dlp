# ADR — Use public repository with local user configuration

## Status
Accepted

## Context
The project is public but user preferences and secrets are personal.

## Decision
Commit examples only. Keep real config, secrets, logs, downloads, cookies, and transcripts out of git.

## Consequences
Safe public development; requires clear first-run setup.

## Notes for AI agents
Do not reverse this decision without creating a new ADR and explicit user approval.
