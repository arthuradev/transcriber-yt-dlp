# Configuration & First-Run Setup

## Model
User settings are typed Pydantic models in `transcriber.config.models`:

- `UserConfig` (root): `version`, `language`, `ui`, `weather`, `llm`, `cookies`,
  `paths`, `gpu`.
- Secrets are **not** modelled here — API keys live in `.env`
  (see ADR 0013). The persisted config holds preferences only.

## Persistence
`transcriber.storage.config_store.ConfigStore` reads/writes the config as YAML.

- Default location: `%APPDATA%\Transcriber\config.yaml` on Windows
  (`~/.config/Transcriber/config.yaml` elsewhere), via `default_config_path()`.
- The file is user-local and never committed (`config.yaml` is gitignored).
- `ConfigStore` implements the `ConfigRepository` port.

## First run
`transcriber.application.first_run.FirstRunService` detects first run
(`is_first_run()` = no saved config) and runs the wizard via the
`FirstRunPrompts` port, then persists the result.

Order of questions: language → theme → weather (and city if enabled) → output
folder → LLM cleanup preference → GPU-only acknowledgement.

The UI implementation `QuestionaryFirstRunPrompts` owns the localized prompt
text; the language question is shown bilingually before a language is known.

## Internationalization
`transcriber.ui.i18n.Translator` resolves message keys to `pt-BR` / `en-US`
strings, falling back to English then to the key. User-facing strings are looked
up by key; code identifiers stay English.

## Architecture
```text
__main__ (composition root)
  → ConfigStore (storage, implements ConfigRepository)
  → FirstRunService (application) → FirstRunPrompts + ConfigRepository ports
  → QuestionaryFirstRunPrompts (ui, implements FirstRunPrompts)
  → AppShell (ui) configured with theme + Translator from UserConfig
```
The application layer depends only on ports and config models — never on `ui`,
`storage` internals, or external clients.
