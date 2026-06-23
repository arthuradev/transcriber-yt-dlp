# ADR — Use Rich, Questionary, and Pyfiglet for the TUI

## Status
Accepted

## Context
The user wants a beautiful terminal interface with keyboard menus, progress bars, and startup logo.

## Decision
Use Rich for rendering/progress, Questionary for menus, and Pyfiglet with `bloody` font for the logo.

## Consequences
Excellent terminal UX while staying in terminal; must test terminal width and Windows behavior.

## Notes for AI agents
Do not reverse this decision without creating a new ADR and explicit user approval.
