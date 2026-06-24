# Safety Pipeline

Every operation follows this pipeline:

```text
UserIntent
→ StructuredCommand
→ RiskClassification
→ DryRunPlan
→ PreValidation
→ Confirmation
→ Execution
→ PostValidation
→ AuditLog
→ FinalReport
→ Cleanup/Rollback if possible
```

## Risk levels
- Low: metadata read, settings read.
- Medium: public download, conversion, transcript generation.
- High: cookies, batch download, overwrite, private URL, LLM cleanup.
- Critical: arbitrary shell, deleting in bulk, saving secrets, bypass attempts.

## Critical actions
Blocked by default unless a future ADR explicitly allows them.

## Implementation (Phase 7 — planning + dry-run)
The first stages of the pipeline (intent -> structured command -> risk ->
dry-run -> pre-validation) are implemented for downloads:
- `core.profiles` — the eight download profiles and category filtering.
- `core.paths` — pure output-path planning (sanitization, site/date/media-id
  organization), with the date injected for determinism.
- `core.plan.DownloadPlan` / `PlannedItem` — the structured, inspectable plan.
- `safety.risk.classify_download` — risk classification: metadata = low; a normal
  download = medium (confirm); batch over 5, forced overwrite, or cookies = high
  (strong confirm).
- `application.planner.DownloadPlanner` — builds the plan from a probe result +
  profile + path settings.
- `ui.plan.render_plan` — the dry-run renderer (risk-colored, escapes dynamic
  content such as bracketed format selectors).
- `ui.download_flow.DownloadFlow` — the interactive URL -> probe -> profile ->
  output -> dry-run -> confirmation sequence, wired to the download menu actions.

Execution, post-validation, audit, and reporting arrive in later phases. Nothing
in Phase 7 downloads or writes files.

## Cookies, redaction, audit (Phase 14)
- `safety.cookies.evaluate_cookies` — the cookie guard: cookies are advanced and
  opt-in (never auto-enabled), allowed only when enabled + browser-cookies
  allowed + a supported browser is configured, and confirmed before use. The
  download flow shows a warning, requires confirmation, and only then passes
  `cookiesfrombrowser` to yt-dlp. Cookies make the operation high risk (strong
  confirmation) and are never logged.
- `safety.redaction` — `redact_secrets` / `redact_url_tokens` / `redact` strip
  secrets and token-bearing URL parameters from any string before logging.
- `safety.audit.AuditLog` — records sensitive actions (action, risk, secret-free
  detail, timestamp); the download flow records a `download` event. Persistence
  and reporting arrive in Phase 15.
