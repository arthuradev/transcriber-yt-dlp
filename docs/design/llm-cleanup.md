# LLM Transcript Cleanup

## Purpose
LLM cleanup improves formatting, punctuation, paragraphing, and readability.

## Providers
- DeepSeek recommended in examples.
- OpenAI-compatible providers supported.
- Provider details must be configurable.

## Safety
- Always ask before cleanup.
- Send transcript text only.
- Do not send video/audio.
- Do not log transcript content when cleanup is enabled.
- Do not allow the LLM to invent facts or change meaning.

## Prompt contract
The cleanup instruction must say:

- correct punctuation,
- improve paragraph breaks,
- preserve meaning,
- do not add information,
- do not remove important content,
- preserve order.

## Implementation (Phase 13)
- `core.cleanup` — five cleanup profiles (`readable`, `study_notes`, `article`,
  `subtitle_cleanup`, `verbatim_clean`), the fixed `PROMPT_CONTRACT`,
  `system_prompt(profile)`, `chunk_text`, and `LLMError`.
- `ports.llm_provider.LLMProviderPort` — `complete(system, user, model)`.
- `adapters.openai_compatible.OpenAICompatibleProvider` — `POST
  {base_url}/chat/completions` via stdlib `urllib` (injectable transport). The
  API key is a Bearer header, never logged, redacted from error detail; the
  transcript text is never logged.
- `application.cleanup.CleanupService` — chunks the transcript and cleans each
  chunk; never logs transcript content.
- `storage.text_store.save_text` — writes the cleaned transcript (the raw one is
  saved separately by transcription).
- `ui.cleanup_flow.CleanupFlow` — wired to "Clean transcript with AI": warns what
  is sent, **always asks before cleanup**, requires the API key, picks a style,
  then cleans and saves.

The API key comes from `.env` (`DEEPSEEK_API_KEY` or `OPENAI_COMPATIBLE_API_KEY`,
via `config.secrets.llm_api_key`). The real network call is isolated/injectable
and not network-tested (no key in CI).
