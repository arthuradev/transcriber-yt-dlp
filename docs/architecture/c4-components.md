# C4 Components — Transcriber

## Main components
```text
ui/
  banner, menu, progress, clean screen, ascii renderer

application/
  first_run, media_probe, download_planner, transcript_workflow, cleanup_workflow

core/
  models, policies, errors, result states

ports/
  media_engine, weather, llm, transcription, filesystem, history, reports

adapters/
  ytdlp, weatherapi, deepseek, faster_whisper, local_filesystem, sqlite

safety/
  risk_classifier, dry_run, confirmation, secrets_guard, cookie_guard, path_guard

observability/
  events, logger, report_writer
```
