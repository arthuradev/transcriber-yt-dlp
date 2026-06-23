# ADR — Require dry-run and safety pipeline

## Status
Accepted

## Context
Downloads, cookies, file writes, transcription, and cleanup can have side effects.

## Decision
Every operation creates a dry-run plan before execution and passes through risk classification and confirmation rules.

## Consequences
Safer UX and easier auditing; more implementation work.

## Notes for AI agents
Do not reverse this decision without creating a new ADR and explicit user approval.
