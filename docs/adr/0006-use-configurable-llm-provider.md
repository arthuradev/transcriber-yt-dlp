# ADR — Use configurable LLM provider with DeepSeek recommendation

## Status
Accepted

## Context
Transcript cleanup should use DeepSeek by default for the owner but remain configurable for public users.

## Decision
Define an LLM provider port and provide an OpenAI-compatible adapter. Use DeepSeek in examples, not hardcoded core logic.

## Consequences
Provider flexibility; requires careful logging and user consent.

## Notes for AI agents
Do not reverse this decision without creating a new ADR and explicit user approval.
