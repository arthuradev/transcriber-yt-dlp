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
