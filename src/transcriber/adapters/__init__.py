"""Adapters layer.

Concrete implementations of ports that talk to external systems (yt-dlp,
WeatherAPI, DeepSeek/OpenAI-compatible providers, faster-whisper, local
filesystem, Windows shell, SQLite).

Phase 5 adds ``WeatherApiAdapter``; Phase 6/8 add ``YtDlpEngine`` (probe +
download); Phase 10 adds ``LocalTextFileReader``; Phase 11 adds
``FasterWhisperEngine`` (GPU-only, optional dependency); Phase 13 adds
``OpenAICompatibleProvider`` (DeepSeek/OpenAI-compatible LLM).
"""
