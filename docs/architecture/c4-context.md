# C4 Context — Transcriber

## System context
```text
User
 └─ uses → Transcriber Windows TUI

Transcriber
 ├─ reads/writes → Local filesystem
 ├─ calls → yt-dlp supported sites
 ├─ calls → WeatherAPI, if configured
 ├─ calls → DeepSeek/OpenAI-compatible LLM, if enabled
 ├─ uses → FFmpeg, if required
 └─ uses → NVIDIA CUDA/faster-whisper for transcription
```

## External systems
- Media websites supported by yt-dlp.
- WeatherAPI.
- DeepSeek or OpenAI-compatible provider.
- Local filesystem.
- Windows shell/bootstrap tools.
- FFmpeg.
- NVIDIA GPU/CUDA runtime.

## Trust boundaries
- User local machine is trusted.
- Public media URLs are untrusted input.
- Cookies are sensitive.
- API keys are sensitive.
- LLM provider receives transcript text only after confirmation.
