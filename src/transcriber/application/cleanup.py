"""Transcript cleanup use case.

Chunks the transcript, sends each chunk to the LLM provider with the
formatting-only system prompt, and joins the cleaned chunks. Never logs the
transcript content (a project safety rule). Errors propagate as ``LLMError``.
"""

from __future__ import annotations

from transcriber.core.cleanup import CleanupProfile, chunk_text, system_prompt
from transcriber.ports.llm_provider import LLMProviderPort


class CleanupService:
    """Cleans transcript text via an LLM provider."""

    def __init__(self, provider: LLMProviderPort, *, max_chars: int = 6000) -> None:
        self._provider = provider
        self._max_chars = max_chars

    def clean(self, text: str, profile: CleanupProfile, model: str) -> str:
        chunks = chunk_text(text, self._max_chars)
        if not chunks:
            return ""
        prompt = system_prompt(profile)
        cleaned = [self._provider.complete(prompt, chunk, model).strip() for chunk in chunks]
        return "\n\n".join(part for part in cleaned if part)
