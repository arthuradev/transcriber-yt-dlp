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
