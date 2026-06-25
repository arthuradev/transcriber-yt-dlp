# Windows Packaging

## Development mode
Use `bootstrap.ps1` to:

- check Python,
- install Python via winget if needed,
- create venv,
- install dependencies,
- check FFmpeg,
- check CUDA/GPU,
- run the app.

## User mode
Final distribution:

- portable `Transcriber.exe`,
- installer `Transcriber-Setup.exe`.

## Tools
- PyInstaller first.
- Inno Setup for installer later.

## Runtime preflight
The packaged app must check:

- Windows x64,
- write permissions,
- config exists,
- FFmpeg exists or can be installed,
- GPU/CUDA available for transcription,
- model cache,
- API keys if features enabled.

## Implementation (Phase 18)
- `scripts/bootstrap.ps1` — safe Windows dev setup: checks `uv`, runs `uv sync`,
  checks ffmpeg and GPU/CUDA (via `nvidia-smi`), and creates `.env` from
  `.env.example`. No destructive actions; missing tools print the exact winget
  command rather than installing silently.
- In-app dependency checks: `ports.system_probe.SystemProbe` +
  `adapters.system.LocalSystemProbe` (ffmpeg via PATH, GPU via the transcription
  stack, platform), `application.health.build_health_report`, and
  `ui.health.render_health`. The Settings screen shows a Diagnostics table.
