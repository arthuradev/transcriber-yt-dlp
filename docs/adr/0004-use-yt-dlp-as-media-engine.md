# ADR — Use yt-dlp as media engine

## Status
Accepted

## Context
The project needs to support many media sites without reimplementing extractors.

## Decision
Use yt-dlp through an adapter for metadata probing, downloads, formats, playlists, and subtitles.

## Consequences
Powerful support for many sites; sites may break and cookies/rate limits need safety handling.

## Notes for AI agents
Do not reverse this decision without creating a new ADR and explicit user approval.
