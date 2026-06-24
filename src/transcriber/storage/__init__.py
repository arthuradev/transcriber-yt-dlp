"""Storage layer.

Local persistence: user config, history, archive, non-sensitive logs, and
reports.

Phase 4 adds ``ConfigStore`` (YAML user-config persistence); Phase 10 adds
``FileDownloadArchive`` (duplicate-avoidance archive); Phase 11/13 add
``transcript_store`` / ``text_store``; Phase 15 adds ``SqliteHistoryRepository``.
Secrets are never stored here.
"""
