# Changelog

All notable changes to Transcriber will be documented in this file.

The project follows phase tags: `v0.1.0`, `v0.2.0`, ...

## [Unreleased]

### Planned
- Phase 12: Subtitles/transcripts (download existing subtitles).

## [v0.11.0] - 2026-06-24

### Added
- GPU-only transcription (faster-whisper; no CPU fallback):
  - `core.transcription` domain + `core.transcript_format` serializers
    (txt/md/srt/vtt/json).
  - `ports.transcription.TranscriptionEnginePort` (`gpu_available` + `transcribe`).
  - `adapters.faster_whisper_engine.FasterWhisperEngine` — the only module touching
    faster-whisper/ctranslate2 (lazy, type-suppressed); injectable GPU check and
    transcribe function; reports no GPU gracefully when CUDA/the dependency is
    absent.
  - `application.transcription.TranscriptionService` — enforces GPU-only, aborting
    with a helpful `TranscriptionError` when no GPU is available.
  - `storage.transcript_store.save_transcript` — raw transcript output.
  - `ui.transcribe_flow.TranscribeFlow` — wired to the "Transcribe local file"
    menu action; transcription progress presenter and i18n keys.
- `config.models.TranscriptionConfig` (model `large-v3`, auto language, translate,
  output format, keep-audio) on `UserConfig`.
- `faster-whisper` as an **optional** extra (`transcriber[transcription]`).

### Tests
- Added transcript-format, transcription-service (GPU gate), engine (fakes),
  transcript-store, and transcribe-flow tests; verified the flow end-to-end with
  a fake GPU engine (save + abort paths).

### Notes
- faster-whisper is heavy and GPU-only, so it is not installed by default or in
  CI; real GPU transcription is not exercised by automated tests (injected fakes).
- Audio is decoded by faster-whisper directly (video files work); no separate
  ffmpeg extraction step.

## [v0.10.0] - 2026-06-24

### Added
- Playlist execution: a playlist probe expands into one item per entry,
  organized into a playlist-title subfolder.
- Batch `.txt` input: `core.batch.parse_url_list`, a `TextFileReader` port +
  `adapters.local_files.LocalTextFileReader`, `application.batch.BatchProbeService`
  (probes each URL, collects per-URL errors), and `DownloadPlanner.plan_batch`
  (flattens all items; risk classified on total declared count).
- Folder organization: optional `group` subfolder in `core.paths.plan_output_path`
  (site / date / group / file).
- Duplicate avoidance: `DownloadArchive` port + `storage.FileDownloadArchive`
  (user-local `archive.txt` of `extractor:id` keys). The planner marks
  duplicates; the executor skips archived items and records successes.
  `DownloadResult.skipped` + skipped count in the summary.
- Download flow now asks single-URL vs batch file; source/batch i18n keys
  (pt-BR / en-US).

### Changed
- `PlannedItem` carries `extractor` and `is_duplicate`; `DownloadResult` carries
  `skipped`; the planner/executor accept an optional archive.

### Tests
- Added batch-parsing/service, archive, planner (batch/group/duplicate),
  executor (skip/record), paths (group), and batch-flow tests. Verified the
  batch + archive duplicate-skip pipeline end-to-end across two runs.

### Notes
- Batch limits respected: more than 5 declared items requires strong confirmation.

## [v0.9.0] - 2026-06-24

### Added
- Advanced manual format mode: `core.profiles.manual_profile` builds a one-off
  profile from a chosen `MediaFormat` (its `format_id` becomes the selector, no
  merge/post-processing).
- The download flow offers a "Manual format..." entry (single media with
  available formats); choosing it prompts a format picker. New
  `DownloadFlowPrompts.select_format` and manual-format i18n keys (pt-BR/en-US).

### Tests
- Added `manual_profile` tests and a flow test for manual format selection.

### Notes
- All eight named profiles were already implemented (Phase 7); this phase adds
  manual selection and ensures probed formats are shown and selectable.
- Manual mode applies to single media only (flat playlist probes have no
  per-entry formats).

## [v0.8.0] - 2026-06-24

### Added
- Download execution with progress (single URL):
  - `core.download`: `DownloadStatus`, `DownloadProgress`, `DownloadRequest`,
    `DownloadResult`, `DownloadOutcome`, `DownloadError` (pure domain).
  - `ports.media_engine.DownloadEnginePort`: `download(request, on_progress)`.
  - `adapters.yt_dlp_engine.YtDlpEngine.download`: real yt-dlp download with
    progress hooks and optional audio extraction; injectable downloader.
  - `adapters.yt_dlp_mapping.map_progress` / `output_template` (strictly typed).
  - `application.executor.DownloadExecutor`: runs plan items, aggregates results.
  - `ui.progress.ProgressPresenter`: Rich live progress (terminal only).
  - `ui.download_result.render_download_summary`: success/partial/failure panel.
- `DownloadFlow` now executes after confirmation for downloadable (video/audio)
  profiles, shows progress, renders the summary, and shows success art.
- Download i18n keys (pt-BR / en-US).

### Changed
- `DownloadPlan` carries `extract_audio`, `audio_format`, and `is_downloadable`.

### Tests
- Added progress-mapping, executor, summary-renderer, and flow-execution tests.
  Verified the real yt-dlp download path end-to-end against a local HTTP server.

### Notes
- Single URL focus; playlist/batch execution and history/reports come later.
- Transcript/metadata profiles are not executed yet (transcript = Phase 12).

## [v0.7.0] - 2026-06-24

### Added
- Download planning and dry-run (no execution):
  - `core.profiles`: the eight download profiles + category filtering.
  - `core.paths`: pure output-path planning (sanitization, site/date/media-id
    organization; date injected for determinism).
  - `core.plan.DownloadPlan` / `PlannedItem`: the structured, inspectable plan.
  - `safety.risk.classify_download`: risk classification (metadata = low,
    download = medium/confirm, batch > 5 / overwrite / cookies = high / strong
    confirm).
  - `application.planner.DownloadPlanner`: builds plans from probe results.
  - `ui.plan.render_plan`: risk-colored dry-run renderer (escapes bracketed
    format selectors).
  - `ui.download_flow.DownloadFlow`: interactive URL -> probe -> profile ->
    output -> dry-run -> confirmation, wired to the download menu actions.
- `AppShell` action handler routing download actions to the flow.
- Plan/risk i18n keys (pt-BR / en-US).

### Tests
- Added profiles, paths, risk, planner, plan-renderer, download-flow, and
  shell-routing tests.

### Notes
- Nothing downloads or writes files in this phase; the flow stops at the dry-run
  and confirmation. Execution lands in Phase 8.

## [v0.6.0] - 2026-06-23

### Added
- yt-dlp metadata probe (probe only; no downloads):
  - `core.media`: `MediaFormat`, `MediaMetadata`, `PlaylistEntry`,
    `PlaylistMetadata`, `ProbeResult`, and `MediaError` (pure domain).
  - `ports.media_engine.MediaEnginePort` — `probe(url) -> ProbeResult`.
  - `adapters.yt_dlp_engine.YtDlpEngine` — the only module importing yt-dlp;
    probes with `download=False` and `extract_flat`; injectable extractor for
    offline tests.
  - `adapters.yt_dlp_mapping.map_info` — strictly-typed dict -> domain mapping.
  - `application.probe.MediaProbeService` — input validation + delegation.
  - `ui.media.render_metadata` — title/site/duration/url, formats table, or
    playlist item count + entry titles. Added media i18n keys (pt-BR / en-US).

### Changed
- Added runtime dependency `yt-dlp`.

### Tests
- Added mapping, probe-service, engine (injected extractor), and renderer tests.

### Notes
- yt-dlp ships only partial private inline types; they are suppressed solely in
  the engine adapter and isolated from the rest of the codebase.
- Interactive URL input is wired with the download flow in Phase 7.

## [v0.5.0] - 2026-06-23

### Added
- Optional weather/time display behind a `WeatherPort`:
  - `core.weather.WeatherSnapshot` / `WeatherError` (pure domain).
  - `adapters.weatherapi.WeatherApiAdapter` (WeatherAPI.com `current.json`) with
    an injectable HTTP transport; the API key is read from `WEATHERAPI_KEY`,
    never logged, and redacted from error detail.
  - `application.weather.WeatherService` with a TTL cache (`cache_minutes`) and
    graceful degradation (failures become `None`).
  - `ui.weather` formatting and a discreet "unavailable" warning; the shell shows
    the weather line at the top of the header.
- `config.secrets.weather_api_key()` to read the key from the environment.
- i18n key `weather.unavailable` (pt-BR / en-US).

### Changed
- `AppShell` accepts an optional `weather_line_provider`.
- Startup wires weather only when `enabled` and `show_on_startup`; with no key it
  shows the discreet warning. Weather never blocks startup.

### Tests
- Added weather adapter (incl. key redaction), service (caching/degradation), and
  UI/shell-integration tests.

### Notes
- No new third-party dependency: the adapter uses stdlib `urllib`.
- API keys remain in `.env` only (ADR 0013).

## [v0.4.0] - 2026-06-23

### Added
- Pydantic user-configuration models (`transcriber.config.models`): `UserConfig`
  with `ui`, `weather`, `llm`, `cookies`, `paths`, `gpu`, and a `Language` enum
  (pt-BR / en-US). No secrets are modelled — API keys stay in `.env`.
- YAML config persistence (`ConfigStore`) implementing a `ConfigRepository`
  port; default location `%APPDATA%\Transcriber\config.yaml`.
- First-run setup: `FirstRunService` (application) drives a wizard via the
  `FirstRunPrompts` port and persists the config; `QuestionaryFirstRunPrompts`
  (ui) provides the localized prompts with a bilingual language question.
- Internationalization: `Translator` with a pt-BR / en-US message catalog;
  the menu, placeholders, and goodbye are now localized.
- `python -m transcriber` runs first-run setup when needed, otherwise loads the
  saved config and applies the chosen theme and language.
- ADR 0013 (secrets in env, not config) and a configuration design doc.

### Changed
- Menu API is translator-driven (`MENU_ORDER`, `build_menu_items`,
  `label_for(action, translator)`, `prompt_main_menu(translator)`).
- `AppShell` accepts a `Translator`.
- Added runtime dependencies `pydantic` and `pyyaml` (dev: `types-PyYAML`).

### Tests
- Added config-model, config-store, i18n, and first-run tests, plus an
  architecture test that the application layer imports no ui/adapters.

### Notes
- No weather/LLM API calls yet; first run collects preferences only.

## [v0.3.0] - 2026-06-23

### Added
- Dark theme registry with six themes (default, purple, red, blue, monochrome,
  anime); `build_console(theme_name)` selects one, all sharing the same style
  keys.
- ASCII art renderer (`transcriber.ui.ascii_art`): UTF-8 loading, cell-accurate
  width measurement (correct for Unicode/braille art), terminal-fit checks,
  random selection, and no-wrap centered rendering that preserves raw lines.
- Clean-screen success flow (`transcriber.ui.screens`): `clear_screen` and
  `show_success_screen` (summary panel + optional success art + minimum display
  time + Press-Enter-to-return), with injectable sleep for testability.
- Welcome art at startup: the shell renders a fitting welcome art under the
  banner; `python -m transcriber` discovers `assets/ascii/welcome` and picks one.
- `.gitattributes` normalizing line endings to LF.

### Changed
- `build_console` now takes an optional theme name (defaults to `default`).
- `AppShell` accepts `theme_name` and `welcome_art`.
- CI actions bumped (checkout v7, setup-python v6, setup-uv v8.2.0) to run on
  Node 24 and clear the Node 20 deprecation warning.

### Tests
- Added theme, ASCII art, and success-screen tests.

### Notes
- Theme *selection from settings/first-run* and YAML-driven ASCII config are
  Phase 4; the renderer/registry contracts are in place now.
- No download/transcription/cleanup behavior yet.

## [v0.2.0] - 2026-06-23

### Added
- TUI shell (`transcriber.ui`): shared themed Rich console and a default dark
  theme palette.
- Startup banner using Pyfiglet (`bloody` font) with a fallback font, plus the
  `Download • Transcription • Cleanup` subtitle.
- Always-on startup animation that plays only on a real terminal (no-op on
  captured/non-interactive streams).
- Main menu via Questionary (`MenuAction` / `MAIN_MENU`) with the eight initial
  options; non-exit actions render a "Coming soon" placeholder.
- `AppShell` main loop with an injectable action selector for testability;
  `python -m transcriber` now launches the shell.
- UI unit tests (banner, menu, animation, shell) and an architecture test
  asserting the UI layer never imports adapters.

### Changed
- `python -m transcriber` now starts the TUI instead of printing a skeleton
  notice.

### Dependencies
- Added runtime dependencies: `rich`, `questionary`, `pyfiglet` (per ADR 0003).

### Notes
- Menu actions are placeholders; no download/transcription/cleanup behavior yet.
- Theme *selection* and the post-operation success-art clean-screen flow arrive
  in Phase 3.

## [v0.1.0] - 2026-06-23

### Added
- Public repository skeleton and documentation pack.
- Modular-monolith `src/transcriber` package layout (core, application, ports,
  adapters, ui, safety, storage, observability, config, assets).
- Pure core domain content: structured `AppError`/`ErrorSeverity` and the
  `OperationType`/`RiskLevel` enumerations.
- Non-functional `python -m transcriber` entry point.
- `scripts/quality_gate.py` validator (secret-file, package-structure, and
  core import-boundary checks).
- Architecture boundary tests and core unit tests.
- uv-based build (hatchling) with a `dev` dependency group; GitHub Actions CI.

### Notes
- No functional download/transcription/cleanup features yet.
