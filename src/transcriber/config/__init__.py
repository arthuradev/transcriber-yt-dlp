"""Config layer.

User-local configuration models, defaults, and loading. Configuration values
(weather city, API providers, keys, output folders, theme, language, cookie
choices) are always local and never committed. API keys are never modelled
here; they live in the environment / ``.env``.

Phase 4 adds the Pydantic user-configuration models (see ``models``).
"""
