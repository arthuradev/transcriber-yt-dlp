# Tasks

## Current phase
Phase 20 — Public release candidate (final phase).

## Phase 1 checklist
- [x] Create public GitHub repository `transcriber-yt-dlp`.
- [x] Add Apache-2.0 license.
- [x] Add documentation pack.
- [x] Add `src/` layout skeleton.
- [x] Add `pyproject.toml` with uv, ruff, pytest, pyright.
- [x] Add `.gitignore` and `.env.example`.
- [x] Add GitHub Actions quality gate.
- [x] Add `scripts/quality_gate.py` placeholder/initial validator.
- [x] Add architecture boundary test skeleton.
- [x] Update CHANGELOG.
- [x] Commit using Conventional Commits.
- [x] Merge to `main`.
- [x] Create annotated tag `v0.1.0`.
- [x] Create GitHub Release for `v0.1.0`.
- [x] Ask user permission to proceed to Phase 2.

## Phase 2 checklist
- [x] Add `rich`, `questionary`, `pyfiglet` runtime dependencies.
- [x] Add shared themed console and default dark theme palette.
- [x] Add Pyfiglet startup banner (`bloody` font) and subtitle.
- [x] Add always-on startup animation (terminal-only).
- [x] Add Questionary main menu with the eight initial options.
- [x] Add `AppShell` main loop with placeholder actions.
- [x] Wire `python -m transcriber` to launch the TUI.
- [x] Add UI tests and a UI->adapters architecture boundary test.
- [x] Update CHANGELOG and TASKS.
- [x] Run quality gates.
- [x] Commit, merge to `main`, tag `v0.2.0`, GitHub Release.
- [x] Ask user permission to proceed to Phase 3.

## Phase 3 checklist
- [x] Add dark theme registry (default, purple, red, blue, monochrome, anime).
- [x] Make `build_console`/`AppShell` theme-aware.
- [x] Add ASCII art renderer with cell-accurate width and fit checks.
- [x] Add no-wrap centered rendering with compact fallback.
- [x] Add clean-screen success flow (`show_success_screen`).
- [x] Wire welcome art at startup.
- [x] Add theme/ascii/screen tests.
- [x] Housekeeping: add `.gitattributes`; bump CI action versions.
- [x] Update CHANGELOG and TASKS.
- [x] Run quality gates.
- [x] Commit, merge to `main`, tag `v0.3.0`, GitHub Release.
- [x] Ask user permission to proceed to Phase 4.

## Phase 4 checklist
- [x] Add Pydantic user-config models and `Language` enum.
- [x] Add YAML config persistence (`ConfigStore`) + `ConfigRepository` port.
- [x] Add i18n `Translator` with pt-BR / en-US catalog.
- [x] Localize menu/shell strings.
- [x] Add first-run wizard (`FirstRunService` + `FirstRunPrompts` port + UI impl).
- [x] Wire first-run/config load into startup.
- [x] Keep secrets in `.env` (ADR 0013); none in persisted config.
- [x] Add config/i18n/first-run tests + application boundary test.
- [x] Update CHANGELOG and TASKS; add configuration design doc.
- [x] Run quality gates.
- [x] Commit, merge to `main`, tag `v0.4.0`, GitHub Release.
- [x] Ask user permission to proceed to Phase 5.

## Phase 5 checklist
- [x] Add `WeatherSnapshot`/`WeatherError` domain + `WeatherPort`.
- [x] Add `WeatherApiAdapter` (injectable transport, key redaction).
- [x] Add `WeatherService` with TTL cache and graceful degradation.
- [x] Add weather display + discreet unavailable warning; wire into header.
- [x] Read key from `.env` via `config.secrets`; never log it.
- [x] Ensure weather never blocks startup.
- [x] Add weather adapter/service/ui tests.
- [x] Update CHANGELOG, TASKS, weather design doc.
- [x] Run quality gates.
- [x] Commit, merge to `main`, tag `v0.5.0`, GitHub Release.
- [x] Ask user permission to proceed to Phase 6.

## Phase 6 checklist
- [x] Add media domain (`core.media`) + `MediaEnginePort`.
- [x] Add `YtDlpEngine` (probe only, injectable extractor, yt-dlp isolated).
- [x] Add strictly-typed `map_info` dict -> domain mapping.
- [x] Add `MediaProbeService` (application).
- [x] Add `render_metadata` UI + media i18n keys.
- [x] Add mapping/service/engine/renderer tests.
- [x] Update CHANGELOG, TASKS, media-download design doc.
- [x] Run quality gates.
- [x] Commit, merge to `main`, tag `v0.6.0`, GitHub Release.
- [x] Ask user permission to proceed to Phase 7.

## Phase 7 checklist
- [x] Add download profiles (`core.profiles`) + category filtering.
- [x] Add pure output-path planning (`core.paths`).
- [x] Add `DownloadPlan`/`PlannedItem` (`core.plan`).
- [x] Add risk classification (`safety.risk`).
- [x] Add `DownloadPlanner` (application).
- [x] Add dry-run renderer (`ui.plan`) with markup escaping.
- [x] Add interactive `DownloadFlow` wired to download menu actions.
- [x] Add plan/risk i18n keys; shell action-handler routing.
- [x] Add profiles/paths/risk/planner/renderer/flow/shell tests.
- [x] Update CHANGELOG, TASKS, safety-pipeline design doc.
- [x] Run quality gates.
- [x] Commit, merge to `main`, tag `v0.7.0`, GitHub Release.
- [x] Ask user permission to proceed to Phase 8.

## Phase 8 checklist
- [x] Add download domain (`core.download`).
- [x] Add `DownloadEnginePort.download`.
- [x] Add real yt-dlp download + progress hook + result extraction.
- [x] Add `map_progress` / `output_template` (strictly typed).
- [x] Add `DownloadExecutor` (application).
- [x] Add `ProgressPresenter` and `render_download_summary` (ui).
- [x] Wire execution into `DownloadFlow` after confirmation.
- [x] Add download i18n keys.
- [x] Add mapping/executor/summary/flow tests; verify real download locally.
- [x] Update CHANGELOG, TASKS, media-download design doc.
- [x] Run quality gates.
- [x] Commit, merge to `main`, tag `v0.8.0`, GitHub Release.
- [x] Ask user permission to proceed to Phase 9.

## Phase 9 checklist
- [x] Confirm all eight named profiles are implemented.
- [x] Add `manual_profile` (one-off profile from a chosen format).
- [x] Offer "Manual format..." in the flow (single media with formats).
- [x] Add `select_format` prompt + manual-format i18n keys.
- [x] Ensure probed formats are shown and selectable.
- [x] Add manual-profile and manual-flow tests.
- [x] Update CHANGELOG, TASKS, media-download design doc.
- [x] Run quality gates.
- [x] Commit, merge to `main`, tag `v0.9.0`, GitHub Release.
- [x] Ask user permission to proceed to Phase 10.

## Phase 10 checklist
- [x] Playlist execution with playlist-title subfolder.
- [x] Batch `.txt` input (parser + reader port/adapter + batch service).
- [x] `DownloadPlanner.plan_batch` flattening + risk on total count.
- [x] Folder organization `group` subfolder.
- [x] Duplicate archive (port + file storage); planner marks, executor skips/records.
- [x] Flow source selection (single/batch); source/batch i18n keys.
- [x] Add batch/archive/planner/executor/paths/flow tests; verify end-to-end.
- [x] Update CHANGELOG, TASKS, media-download design doc.
- [x] Run quality gates.
- [x] Commit, merge to `main`, tag `v0.10.0`, GitHub Release.
- [x] Ask user permission to proceed to Phase 11.

## Phase 11 checklist
- [x] Add transcription domain + serializers (txt/md/srt/vtt/json).
- [x] Add `TranscriptionEnginePort` + `FasterWhisperEngine` (GPU-only, injectable).
- [x] Add `TranscriptionService` enforcing GPU-only (no CPU fallback).
- [x] Add raw transcript output (`save_transcript`).
- [x] Add `TranscribeFlow` wired to "Transcribe local file".
- [x] Add `TranscriptionConfig`; faster-whisper as optional extra.
- [x] Add format/service/engine/store/flow tests; verify flow end-to-end (fakes).
- [x] Update CHANGELOG, TASKS, transcription design doc.
- [x] Run quality gates.
- [x] Commit, merge to `main`, tag `v0.11.0`, GitHub Release.
- [x] Ask user permission to proceed to Phase 12.

## Phase 12 checklist
- [x] Probe reports subtitle/auto-caption languages; shown in metadata.
- [x] Add `core.subtitles` + `SubtitleEnginePort` + `YtDlpEngine.download_subtitles`.
- [x] Add `SubtitleService` + `SubtitleFlow` (prefer existing subtitles).
- [x] Wire "Download transcript / subtitles" to the subtitle flow.
- [x] Add `SubtitlesConfig`; subtitle i18n keys; no-subs fallback hint.
- [x] Add subtitle/mapping/engine/flow/media tests; verify flow end-to-end.
- [x] Update CHANGELOG, TASKS, media-download design doc.
- [x] Run quality gates.
- [x] Commit, merge to `main`, tag `v0.12.0`, GitHub Release.
- [x] Ask user permission to proceed to Phase 13.

## Phase 13 checklist
- [x] Add cleanup profiles + format-only prompt contract + chunking.
- [x] Add `LLMProviderPort` + `OpenAICompatibleProvider` (key redaction, no logging).
- [x] Add `CleanupService` (chunk → clean → join).
- [x] Add cleaned-transcript writer (`save_text`).
- [x] Add `CleanupFlow` (always ask before cleanup; key required) wired to menu.
- [x] Read key from `.env`; cleanup i18n keys.
- [x] Add cleanup/provider/service/store/flow tests; verify end-to-end.
- [x] Update CHANGELOG, TASKS, llm-cleanup design doc.
- [x] Run quality gates.
- [x] Commit, merge to `main`, tag `v0.13.0`, GitHub Release.
- [x] Ask user permission to proceed to Phase 14.

## Phase 14 checklist
- [x] Add cookie guard (`safety.cookies`), opt-in/confirmed/never auto-enabled.
- [x] Add redaction helpers (`safety.redaction`).
- [x] Add audit events (`safety.audit.AuditLog`); record download events.
- [x] Thread `cookies_from_browser` through request/plan/planner/executor/adapter.
- [x] Classify cookie use as high risk; add `confirm_cookies` + cookie warning.
- [x] Add cookie/redaction/audit/planner/executor/flow tests; verify end-to-end.
- [x] Update CHANGELOG, TASKS, safety-pipeline design doc.
- [x] Run quality gates.
- [x] Commit, merge to `main`, tag `v0.14.0`, GitHub Release.
- [x] Ask user permission to proceed to Phase 15.

## Phase 15 checklist
- [x] Add history domain + `HistoryRepositoryPort` + SQLite repository.
- [x] Add operation report domain + JSON/Markdown formatters.
- [x] Add redacted `FileLogger` (no private content).
- [x] Add `OperationRecorder` (history + log + report file).
- [x] Add `build_download_report`; wire recorder into the download flow.
- [x] Add history/report/log/recorder/reporting/flow tests; verify end-to-end.
- [x] Update CHANGELOG, TASKS; add history-and-reports design doc.
- [x] Run quality gates.
- [x] Commit, merge to `main`, tag `v0.15.0`, GitHub Release.
- [x] Ask user permission to proceed to Phase 16.

## Phase 16 checklist
- [x] Add `coverage`; configure `fail_under = 70` (omit `__main__`).
- [x] Wire coverage gate into CI.
- [x] Strict data-driven architecture boundary tests (per-layer rules).
- [x] Add integration test (plan -> execute -> archive -> history -> report).
- [x] Update CHANGELOG, TASKS, testing design doc.
- [x] Run quality gates (incl. coverage 88% >= 70%).
- [x] Commit, merge to `main`, tag `v0.16.0`, GitHub Release.
- [x] Ask user permission to proceed to Phase 17.

## Phase 17 checklist
- [x] Add History view flow (recent operations from SQLite history).
- [x] Add Settings flow (view + edit theme/language, persisted).
- [x] Wire History/Settings menu actions; add i18n keys.
- [x] Add history-flow and settings-flow tests; verify end-to-end.
- [x] Update CHANGELOG, TASKS, ui-ux design doc.
- [x] Run quality gates (coverage 88% >= 70%).
- [x] Commit, merge to `main`, tag `v0.17.0`, GitHub Release.
- [x] Ask user permission to proceed to Phase 18.

## Phase 18 checklist
- [x] Add safe `scripts/bootstrap.ps1` (uv/ffmpeg/GPU checks, .env creation).
- [x] Add health domain + `SystemProbe` port + `LocalSystemProbe` adapter.
- [x] Add `build_health_report` + `render_health`; show Diagnostics in Settings.
- [x] Add health/probe/renderer/settings tests; validate ps1 syntax.
- [x] Update CHANGELOG, TASKS, packaging + scripts docs.
- [x] Run quality gates (coverage 88% >= 70%).
- [x] Commit, merge to `main`, tag `v0.18.0`, GitHub Release.
- [x] Ask user permission to proceed to Phase 19.

## Phase 19 checklist
- [x] Add PyInstaller spec (`Transcriber.spec`) + entry (`scripts/pyi_entry.py`).
- [x] Add `scripts/build_exe.ps1` (portable exe).
- [x] Add Inno Setup `scripts/installer.iss` + `scripts/build_installer.ps1`.
- [x] Add `build` optional extra (PyInstaller); locate assets from `_MEIPASS`.
- [x] Add `_MEIPASS` test; validate ps1 + spec syntax.
- [x] Update CHANGELOG, TASKS, packaging design doc.
- [x] Run quality gates (coverage 88% >= 70%).
- [x] Commit, merge to `main`, tag `v0.19.0`, GitHub Release.
- [x] Ask user permission to proceed to Phase 20.

## Phase 20 checklist
- [x] Polish public README (bilingual: features, quickstart, usage, build).
- [x] Align package version to 0.20.0 (pyproject, __version__, installer).
- [x] Add release-consistency test.
- [x] Update CHANGELOG and TASKS.
- [x] Run quality gates (coverage >= 70%).
- [x] Commit, merge to `main`, tag `v0.20.0`, GitHub Release.
- [x] Ask user whether to proceed past v0.20.0.

## Project status
All 20 phases complete (v0.1.0 ... v0.20.0), tagged and released with green CI.
`v1.0.0` is intentionally NOT created — it requires explicit owner approval.

## Backlog notes
- Real exe/installer build must run on a Windows host (PyInstaller/ISCC).
- Transcription requires the optional extra + CUDA; not exercised by tests.
- API keys live in `.env`, never in config.yaml.
