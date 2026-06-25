# UI/UX Design

## Style
- Monkeytype clean.
- Dark only.
- Cute/waifu accents used sparingly.
- Terminal-first, not GUI.
- Clear panels, minimal clutter.

## Startup
- Clear screen.
- Show animation.
- Render Pyfiglet `Transcriber` with default `bloody` font.
- Show subtitle.
- Show weather/time if configured.
- Show random startup message.

## Main menu
Use Questionary keyboard selection.

Initial options:
- Download video
- Download audio
- Download transcript/subtitles
- Transcribe local file
- Clean transcript with AI
- History
- Settings
- Exit

## Clean screen mode
After every operation:
- show final summary,
- show success ASCII art if possible,
- wait at least 3 seconds,
- show “Press Enter to return to menu”,
- clear screen,
- render fresh header/menu.

## Terminal width
Never wrap ASCII art. If too small, use compact fallback.

## Implementation (Phase 17 — polish)
- `ui.history_flow.HistoryFlow` — the History menu action shows recent operations
  (from the Phase 15 SQLite history) as a status-colored table.
- `ui.settings_flow.SettingsFlow` — the Settings menu action shows current
  settings and lets the user change theme/language, persisted via the config
  repository (theme/language apply on next launch).
- Both flows are themed and localized (pt-BR / en-US) and use the established
  prompt-protocol pattern. No architecture change.
