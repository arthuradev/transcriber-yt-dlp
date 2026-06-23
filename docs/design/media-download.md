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
