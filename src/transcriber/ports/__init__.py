"""Ports layer.

Interfaces (Protocols) describing the external systems the application depends
on, e.g. media engine, weather, LLM provider, transcription engine, filesystem,
shell, history repository, and report writer.

Phase 4 adds ``ConfigRepository`` / ``FirstRunPrompts``; Phase 5 ``WeatherPort``;
Phase 6/8 ``MediaEnginePort`` / ``DownloadEnginePort``; Phase 10 ``TextFileReader``
and ``DownloadArchive``; Phase 11 ``TranscriptionEnginePort``; Phase 12
``SubtitleEnginePort``.
"""
