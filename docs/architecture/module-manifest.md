# Module Manifest

Module manifests are optional at first, but useful when modules become plug-like or risk-bearing.

Example:

```toml
id = "media_download"
name = "Media Download"
version = "0.1.0"
status = "active"

[capabilities]
provides = ["media.metadata", "media.download", "media.subtitles"]

[contracts]
implements = ["MediaEnginePort"]

[dependencies]
packages = ["yt-dlp"]
external = ["ffmpeg"]

[permissions]
network = true
filesystem = true
shell = false
secrets = ["browser_cookies_optional"]

[risk]
default = "medium"
sensitive_actions = ["cookies_from_browser", "batch_download"]

[dry_run]
supported = true

[rollback]
supported = "partial"

[health_checks]
checks = ["yt_dlp_available", "ffmpeg_available"]
```

Do not create manifests for trivial modules unless they provide capabilities, permissions, or optional behavior.
