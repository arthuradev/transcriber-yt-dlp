"""Port for an LLM chat-completion provider."""

from __future__ import annotations

from typing import Protocol


class LLMProviderPort(Protocol):
    """Contract for an OpenAI-compatible chat provider."""

    def complete(self, system: str, user: str, model: str) -> str:
        """Return the model's reply for the system+user messages. Raises ``LLMError``."""
        ...
