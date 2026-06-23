# Security Policy

## Sensitive data
The repository must never contain:

- API keys,
- `.env`,
- cookies,
- tokens,
- user configs,
- downloaded media,
- generated transcripts,
- private logs,
- browser credentials,
- local model caches.

## Responsible use
Transcriber is intended for legitimate media processing. Users must respect copyright, platform terms, privacy, and local laws.

## Cookies
Cookies are sensitive. The app may support browser cookies as an advanced feature, but must:

- warn the user,
- require confirmation,
- avoid logging cookie data,
- avoid committing cookie files,
- avoid sending cookies to LLM providers.

## LLM cleanup
When transcript cleanup is enabled:

- only transcript text may be sent,
- never send audio/video files,
- never log transcript content by default,
- warn the user before sending text to a provider.

## Reporting issues
For public security issues, open a GitHub issue without secrets. For sensitive issues, use private contact once configured.
