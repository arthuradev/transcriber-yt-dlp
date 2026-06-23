# Project Spec Lock — Transcriber

This file records the current agreed decisions. Claude Code must treat this file as the source of truth unless the user explicitly changes a decision.

## Identity
- Display name: `Transcriber`.
- Package name: `transcriber`.
- GitHub repository: `transcriber-yt-dlp`.
- License: Apache-2.0.
- Public repository.
- README and GitHub description: bilingual Portuguese/English.
- Code, identifiers, comments, commits, and technical names: English.
- User-facing UI: Portuguese or English selected on first run; changeable in settings.

## Platform
- Windows-only for now.
- Ignore Linux/macOS support for the current roadmap.
- Runs in terminal as a TUI application.
- Final distribution: both portable `.exe` and installer `.exe`.
- Initial packaging: PyInstaller.
- Installer later: Inno Setup.

## UI/UX
- Style: Monkeytype clean + cute/waifu accents.
- Dark theme only.
- Theme system allowed: default, purple, red, blue, monochrome, anime.
- Startup animation always enabled.
- Pyfiglet with `bloody` font is default.
- Other figlet fonts may be supported as optional/random.
- Startup subtitle allowed: `Download • Transcription • Cleanup`.
- TUI must clear the screen between operations.
- After success: show summary + ASCII art together, wait at least 3 seconds, then show “Press Enter to return to menu”.
- ASCII art should be raw/preserved by default; optional color overlay only if safe.
- If terminal is too small, do not show the art; show compact success fallback.
- Center art only when it fits safely.
- Try fullscreen; if unavailable, maximize; if unavailable, show a F11 hint.

## ASCII Art
- Four uploaded ASCII arts may be included in the public repository.
- They are used for welcome/success states.
- User can add new arts by dropping `.txt` files into asset folders.
- `ascii.yaml` controls enable/disable, min terminal width, wait behavior, and selection.

## Weather and personalization
- Weather provider: WeatherAPI.
- Weather is optional by default.
- First run asks for language, weather preference, city, API key, output folder, LLM preference, and GPU policy confirmation.
- Public repo must not hardcode São Bernardo do Campo.
- Local user config may set any city.
- Weather display: city, temperature, condition, local time.
- If API key/internet is missing: show a discreet warning.
- Cache weather responses to avoid unnecessary API calls.

## Download engine
- yt-dlp is the media engine.
- Accept any site supported by yt-dlp, with no guarantee that every site works.
- Support single URL and `.txt` batch URL input.
- Batch downloads are limited: up to 5 URLs without strong confirmation.
- Playlists are part of MVP.
- Cookies are part of MVP as an advanced protected feature.
- Allow `cookies-from-browser` with explicit warning and confirmation.
- Never auto-enable cookies.
- Never commit or log cookies.
- Show metadata before download.
- Download profiles: `video_best`, `video_1080p`, `video_720p`, `audio_best`, `audio_mp3`, `audio_m4a`, `metadata_only`, `transcript_only`.
- Advanced manual format selection is allowed.

## Output organization
- On first run, ask user to choose or create output folder.
- Default fallback folder name is `downloads`.
- Persist output folder in config.
- Use subfolders by site and date/operation.
- Include media ID in filenames to avoid duplicates.
- Ask before overwriting.
- Use history/archive to avoid duplicates.

## Transcription
- Engine: faster-whisper.
- GPU-only globally.
- No CPU fallback.
- Default model: `large-v3`.
- Language: auto by default.
- Translation support should exist.
- Save raw transcript and cleaned transcript when cleanup is used.
- Output formats: `.txt`, `.md`, `.srt`, `.vtt`, `.json`.
- `.docx` and `.pdf` later.
- Local file transcription supported.
- Temporary audio is deleted by default.
- User may choose to keep intermediates.

## LLM cleanup
- DeepSeek is recommended but configurable.
- Support OpenAI-compatible providers.
- `config.example.yaml` may suggest a DeepSeek model, but the core must be provider-agnostic.
- Cleanup is optional and must always ask before using.
- Cleanup profiles: `readable`, `study_notes`, `article`, `subtitle_cleanup`, `verbatim_clean`.
- LLM may format only. It must not add facts or change meaning.
- Warn that only transcript text is sent, not the video/audio.
- Hide transcript content from logs when LLM cleanup is enabled.
- No cost/token limit required initially.

## Safety
- README must include responsible use and copyright warning.
- App warns rather than blocks sites/content by default.
- Download mass behavior is restricted.
- High-risk operations require confirmation.
- Dry-run before every operation.
- URLs with private tokens are redacted from logs.

## GitHub process
- Main branch: `main`.
- Each phase uses a dedicated branch.
- At phase completion: tests, docs, changelog, commit, merge to main, push, annotated tag, GitHub Release, release notes, ask to proceed.
- Use Conventional Commits.
- GitHub Actions from Phase 1.
- Claude may create issues and milestones.
- Releases at every phase.

## Testing
- Tools: ruff, pytest, pyright, pydantic, uv.
- Use `src/` layout.
- No numeric coverage gate initially.
- Add 70% coverage target later, mandatory gate by Phase 16.
- Architecture tests are mandatory early.
- Core must not import adapters, UI, subprocess, network clients, or external APIs.

## Phase order
See `ROADMAP.md` and `docs/phases/`.
