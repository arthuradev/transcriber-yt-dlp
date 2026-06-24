# Media Download Design

## Engine
yt-dlp is used behind a `MediaEnginePort` adapter.

## Inputs
- Single URL.
- `.txt` file with multiple URLs.
- Playlist URL.

## Safety limits
- Up to 5 URLs: normal confirmation.
- More than 5: strong confirmation.
- Very large batches/playlists: high risk.

## Required flow
```text
input
→ metadata probe
→ profile selection
→ output selection
→ dry-run
→ confirmation
→ execution
→ validation
→ history/report
```

## Cookies
Cookies are advanced and protected. Browser cookies may be used only with explicit confirmation.

## Profiles
See `configs/profiles.example.yaml`.

## Probe implementation (Phase 6)
Metadata probing (no downloads yet):
- `core.media` — pure domain: `MediaFormat`, `MediaMetadata`, `PlaylistEntry`,
  `PlaylistMetadata`, `ProbeResult` (= single | playlist), and `MediaError`.
- `ports.media_engine.MediaEnginePort` — `probe(url) -> ProbeResult`.
- `adapters.yt_dlp_engine.YtDlpEngine` — the only module importing yt-dlp;
  probes with `download=False` and `extract_flat="in_playlist"`. The info
  extractor is injectable for offline tests. yt-dlp's partial private types are
  suppressed only in this file.
- `adapters.yt_dlp_mapping.map_info` — strictly-typed dict -> domain mapping
  (no yt-dlp import), unit-tested with plain dicts.
- `application.probe.MediaProbeService` — validates input and delegates to the
  port (the UI never calls the engine directly).
- `ui.media.render_metadata` — shows title/site/duration/url and a formats table
  (single) or item count + entry titles (playlist).

Interactive URL input is wired into the menu with the download planner/dry-run
flow in Phase 7.

## Execution implementation (Phase 8 — single URL)
- `core.download` — pure domain: `DownloadStatus`, `DownloadProgress`,
  `DownloadRequest`, `DownloadResult`, `DownloadOutcome`, `DownloadError`.
- `ports.media_engine.DownloadEnginePort` — `download(request, on_progress)`
  (kept separate from `MediaEnginePort` so probe-only fakes still satisfy it).
- `adapters.yt_dlp_engine.YtDlpEngine.download` — real yt-dlp download with
  progress hooks and optional audio extraction; the downloader is injectable.
  `yt_dlp_mapping.map_progress` / `output_template` are strictly typed and tested.
- `application.executor.DownloadExecutor` — runs the plan's items and aggregates
  results.
- `ui.progress.ProgressPresenter` — Rich live progress (terminal only).
- `ui.download_result.render_download_summary` — success/partial/failure panel.
- The `DownloadFlow` now executes after confirmation (for downloadable
  video/audio profiles), shows progress, renders the summary, and shows success
  art. Transcript/metadata profiles remain non-executing for now.

## Profiles & manual format mode (Phase 9)
- All eight named profiles are implemented (`core.profiles`).
- Advanced manual mode: the probe's reported formats are shown
  (`render_metadata`), and for a single media item the profile list includes a
  "Manual format..." entry. Choosing it prompts a format picker; the selected
  format becomes a one-off profile via `core.profiles.manual_profile` whose
  `format_selector` is the exact `format_id` (no merge/post-processing).
- Manual mode is offered only when formats are available (single media); flat
  playlist probes have no per-entry formats.

## Playlists, batch, folders, duplicates (Phase 10)
- **Playlists** execute via the planner/executor: a playlist probe expands into
  one `PlannedItem` per entry, organized into a playlist-title subfolder.
- **Batch `.txt`**: `core.batch.parse_url_list` parses the file; `TextFileReader`
  port (`adapters.local_files.LocalTextFileReader`) reads it; `BatchProbeService`
  probes each URL (collecting per-URL errors); `DownloadPlanner.plan_batch`
  flattens all items into one plan. Risk is classified on the total declared
  count (>5 → strong confirmation).
- **Folder organization**: `core.paths.plan_output_path` adds an optional
  `group` subfolder (site / date / group / file).
- **Duplicates/archive**: `DownloadArchive` port + `storage.FileDownloadArchive`
  (a user-local `archive.txt` of `extractor:id` keys). The planner marks
  duplicates for the dry-run; the executor skips archived items and records
  successful downloads. `DownloadResult.skipped` and the summary's skipped count
  surface this.
