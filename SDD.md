# SDD — System Design Document

## 1. Overview
Transcriber is a Windows-only terminal TUI application that helps users download media from yt-dlp-supported URLs, transcribe audio/video locally using GPU-only faster-whisper, optionally format transcript text through an LLM provider, and organize results into user-selected folders.

The product must feel like software, not a throwaway script: beautiful startup, keyboard menus, progress bars, dry-run plans, clean screen mode, success ASCII art, history, reports, and safe handling of sensitive operations.

## 2. Problem
Users often need to download videos, extract audio, obtain subtitles, transcribe local files, or clean transcripts. Existing scripts usually require long commands, technical knowledge, manual dependency setup, and unsafe handling of cookies/API keys. They also leave terminal output messy and are hard for non-technical users.

## 3. Goals
- Provide a beautiful Windows terminal TUI.
- Allow the user to paste a URL or provide a `.txt` file of URLs.
- Detect media metadata before download.
- Let the user choose quality, format, output folder, and operation type.
- Support playlists and batch URLs with safety limits.
- Support GPU-only transcription.
- Support transcript download when subtitles exist.
- Support optional transcript formatting with DeepSeek/OpenAI-compatible providers.
- Always show dry-run plans before operations.
- Keep logs, history, and final reports.
- Package as portable `.exe` and installer later.

## 4. Non-goals
- No piracy/bypass focus.
- No CPU fallback for transcription.
- No cross-platform support in the current roadmap.
- No GUI desktop app in current roadmap.
- No hidden background automation.
- No automatic cookie usage.
- No hardcoded personal city, API key, or local path.

## 5. Users
- Primary: Windows users who want a clean media download/transcription workflow.
- Secondary: non-technical users who can run an `.exe` and follow a menu.
- Developer: project owner and AI coding agents.

## 6. Functional requirements
### Startup
- Show Pyfiglet logo using `bloody` font.
- Show animation.
- Show configured weather and local time if enabled.
- Ask language on first run: Portuguese or English.
- Ask setup questions on first run.

### UI
- Keyboard menu navigation.
- Dark theme.
- Clean screen mode.
- Progress bars with ETA when reliable.
- Success summary + ASCII art.

### Media operations
- Probe metadata before download.
- Show site, title, duration, type, available formats when possible.
- Download video/audio/metadata/transcript.
- Support playlists.
- Support batch `.txt` input.
- Support quality profiles and manual format mode.
- Organize by site/date/operation.
- Avoid duplicate downloads.

### Transcription
- Extract audio when needed.
- Check CUDA/GPU availability.
- Abort if GPU is unavailable.
- Use faster-whisper with `large-v3` by default.
- Support auto language detection and translation.
- Save raw transcript.

### LLM cleanup
- Ask before sending transcript text.
- Use configurable provider.
- Default recommendation: DeepSeek in example config.
- Cleanup must format only, not invent facts.
- Save cleaned transcript separately.

### Safety
- Dry-run before every operation.
- Risk classification.
- Confirmation for high-risk operations.
- Redacted logs.
- Cookie warnings.

## 7. Non-functional requirements
- Maintainable modular monolith.
- Testable core logic.
- Explicit architecture boundaries.
- Observable execution.
- Safe by default.
- Configurable by user.
- Beautiful but not fragile.
- Phase-based development.

## 8. Architecture summary
Transcriber uses a modular monolith with these areas:

- `core`: domain models, policies, errors, pure logic.
- `application`: use cases and orchestration.
- `ports`: contracts for external systems.
- `adapters`: yt-dlp, WeatherAPI, DeepSeek, filesystem, shell, packaging.
- `ui`: Rich/Questionary/Pyfiglet TUI.
- `safety`: risk, dry-run, confirmation, audit, rollback modeling.
- `storage`: history, archive, config persistence.
- `observability`: events, logs, reports.
- `assets`: ASCII art and UI resources.

## 9. Major workflows
### URL download workflow
```text
URL received
→ metadata probe
→ user selects operation/profile/output
→ plan created
→ dry-run shown
→ safety validation
→ confirmation
→ execution
→ progress events
→ post-validation
→ history/report
→ success art
→ return to clean menu
```

### Transcription workflow
```text
source selected
→ audio extraction or local audio accepted
→ GPU check
→ transcription plan
→ dry-run
→ execution
→ raw transcript saved
→ optional LLM cleanup
→ final transcript saved
→ report
```

## 10. Risks
- yt-dlp site breakage.
- Cookies exposing accounts.
- API keys leaked by logs.
- GPU dependency setup complexity.
- Terminal width breaking ASCII art.
- AI cleanup changing meaning.
- Overengineering before MVP.
- Architecture drift caused by agentic coding.

## 11. Success criteria
The project is successful when a non-technical Windows user can open the app, choose language, configure folder, paste a link, see a dry-run, download/transcribe safely, and receive clean output with a clear final report.
