# Scripts Placeholder

Expected scripts:

- `quality_gate.py`
- `bootstrap.ps1`
- `build_exe.ps1`
- `build_installer.ps1`

`quality_gate.py` (Phase 1) and `bootstrap.ps1` (Phase 18) exist. The packaging
scripts (`build_exe.ps1`, `build_installer.ps1`) come in Phase 19.

## bootstrap.ps1
Sets up Transcriber for development on Windows: checks `uv`, runs `uv sync`,
checks ffmpeg and GPU/CUDA, and creates `.env` from `.env.example`. It is safe —
no destructive actions and no silent installs (it prints the winget command for
anything missing). Run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/bootstrap.ps1
```

Pass `-Run` to launch the app afterwards.
