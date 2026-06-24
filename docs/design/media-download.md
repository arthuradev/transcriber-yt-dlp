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
