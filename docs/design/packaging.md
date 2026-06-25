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

## Build (Phase 19)
- `Transcriber.spec` — PyInstaller spec for a portable console exe. Collects the
  whole `transcriber` package (lazy imports) + `yt_dlp`, bundles `assets/ascii`,
  and excludes the heavy transcription stack. Bundles no secrets or user data.
- `scripts/pyi_entry.py` — the frozen entry point (`transcriber.__main__:main`).
- `scripts/build_exe.ps1` — `uv sync --extra build` then
  `uv run pyinstaller Transcriber.spec` → `dist\Transcriber.exe`.
- `scripts/installer.iss` + `scripts/build_installer.ps1` — Inno Setup installer
  (`Transcriber-Setup-<version>.exe`); installs only the exe, with Start Menu
  shortcuts and an uninstaller. Requires ISCC (winget command printed if missing).
- PyInstaller is an optional `build` extra (`transcriber[build]`), not installed
  by default or in CI.
- Frozen builds resolve `assets/ascii` from `sys._MEIPASS` (see
  `ui.ascii_art.locate_ascii_dir`).

**Not verified here:** the actual exe/installer build is not run in CI or this
environment (PyInstaller/ISCC not present). Scripts and the spec are
syntax-validated; the real build must be run on a Windows host.
