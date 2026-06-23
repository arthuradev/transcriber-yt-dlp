# ADR — Keep secrets in the environment, not in the persisted config

## Status
Accepted

## Context
First-run setup collects user preferences (language, theme, weather city,
output folder, LLM/cookies preferences) and also relates to API keys
(WeatherAPI, DeepSeek/OpenAI-compatible). The persisted user configuration is a
local YAML file. Storing API keys in that file risks accidental exposure if a
user shares their config, and blurs the line between preferences and secrets.
This refines ADR 0008 ([[0008-public-repo-local-config]]).

## Decision
The persisted user configuration (`UserConfig`, saved as YAML) holds only
non-secret preferences. API keys and other secrets live exclusively in the
environment / `.env` (see `.env.example`). The Pydantic config models contain no
key/secret fields, and the first-run wizard never writes secrets into the config
file.

## Consequences
- Sharing or committing a config file cannot leak credentials.
- Reading a secret is a separate, explicit step (environment lookup) added when
  the consuming feature (weather, LLM) is implemented.
- The first-run wizard guides users toward `.env` for keys rather than storing
  them itself.

## Notes for AI agents
Do not add API-key or secret fields to the config models or write secrets to the
config file. Keep secrets in environment variables. Do not reverse this decision
without a new ADR and explicit user approval.
