# History, Logs, and Reports

## Overview
After an operation completes, a secret-free record is persisted three ways:
history (SQLite), a structured log line, and an optional JSON report file.

## Components (Phase 15)
- `core.history.HistoryEntry` / `core.report.OperationReport` — pure records.
  `OperationReport.to_history_entry()` projects a report to a compact entry.
- `application.reporting.build_download_report` — builds a secret-free report
  from a `DownloadPlan` + `DownloadOutcome` (status ok/partial/failed).
- `ports.history.HistoryRepositoryPort` + `storage.history.SqliteHistoryRepository`
  — stdlib SQLite, user-local `history.sqlite` (gitignored), summary fields only.
- `observability.report_format` — `report_to_json` / `report_to_markdown`.
- `observability.logs.FileLogger` — appends timestamped lines, each passed
  through `safety.redaction` (no secrets, no token URLs). User-local
  `transcriber.log` (gitignored).
- `observability.recorder.OperationRecorder` — records one report to history, the
  log, and (optionally) a JSON report file under the download dir's `reports/`.

## Wiring
The download flow records a report via the injected `OperationRecorder` after
execution (alongside the audit event). The DB, logs, and reports are all
user-local and never committed.

## Safety
No private content (transcripts, URLs with tokens, secrets) is written to logs,
history, or reports. Logs are redacted; history/report details are built from
secret-free fields only.
