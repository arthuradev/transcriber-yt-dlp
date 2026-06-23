# ADR — Use modular monolith architecture

## Status
Accepted

## Context
The project is a solo/public Windows app that needs strong internal boundaries without distributed-system overhead.

## Decision
Use a modular monolith with core, application, ports, adapters, ui, safety, storage, and observability.

## Consequences
Simpler local development, easier packaging, fewer operational risks, but requires architecture tests to avoid boundary drift.

## Notes for AI agents
Do not reverse this decision without creating a new ADR and explicit user approval.
