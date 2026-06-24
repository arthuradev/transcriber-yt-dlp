"""Storage layer.

Local persistence: user config, history, archive, non-sensitive logs, and
reports.

Phase 4 adds ``ConfigStore`` (YAML user-config persistence); Phase 10 adds
``FileDownloadArchive`` (duplicate-avoidance archive). Secrets are never stored
here.
"""
