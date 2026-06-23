# Architecture — Transcriber

## 1. Style
Transcriber uses a **modular monolith with ports and adapters**.

The project is not microservices. It is not a single-file script. It is a local Windows app with strong internal boundaries.

## 2. High-level structure
```text
src/transcriber/
  core/
  application/
  ports/
  adapters/
  ui/
  safety/
  storage/
  observability/
  config/
  assets/
```

## 3. Dependency direction
```text
ui ───────────────┐
adapters ────────┤
storage ─────────┤
observability ───┤
                 ▼
            application
                 ▼
              core
```

`core` does not depend on the outside world. External systems depend inward through ports.

## 4. Layer responsibilities
### core
Pure domain concepts:

- operation types,
- risk levels,
- media profile models,
- transcript models,
- path policies,
- app errors,
- result states.

Forbidden in `core`:

- UI imports,
- adapter imports,
- subprocess,
- network clients,
- filesystem mutation,
- API clients.

### application
Use cases and workflow coordination:

- first-run setup,
- metadata probe orchestration,
- download planning,
- transcription planning,
- LLM cleanup orchestration,
- dry-run creation,
- execution handoff,
- result reporting.

### ports
Interfaces for external systems:

- `MediaEnginePort`,
- `WeatherPort`,
- `LLMProviderPort`,
- `TranscriptionEnginePort`,
- `FileSystemPort`,
- `ShellPort`,
- `HistoryRepositoryPort`,
- `ReportWriterPort`.

### adapters
Implement ports:

- yt-dlp adapter,
- WeatherAPI adapter,
- DeepSeek/OpenAI-compatible adapter,
- faster-whisper adapter,
- local filesystem adapter,
- Windows shell/bootstrap adapter,
- SQLite adapter.

### ui
Presentation only:

- Rich layouts,
- Questionary menus,
- Pyfiglet banners,
- progress rendering,
- clean screen mode,
- ASCII art rendering.

UI must not contain business rules.

### safety
Safety pipeline:

- risk classifier,
- dry-run builder,
- confirmation gate,
- cookie guard,
- secrets guard,
- path guard,
- audit events,
- rollback model.

### storage
Local persistence:

- user config,
- history,
- archive,
- non-sensitive logs,
- reports.

### observability
Events and reporting:

- event bus,
- structured logs,
- final reports,
- phase/debug diagnostics.

## 5. Event model
Use events to decouple UI/progress/logging:

```text
UrlReceived
InfoExtractStarted
InfoExtracted
PlanCreated
DryRunRendered
SafetyCheckPassed
DownloadStarted
ProgressUpdated
PostProcessingStarted
TranscriptionStarted
LLMCleanupStarted
OperationSucceeded
OperationFailed
ReportCreated
```

## 6. Safety pipeline
Every operation follows:

```text
intent
→ structured command
→ risk classification
→ dry-run plan
→ pre-validation
→ confirmation if needed
→ execution
→ post-validation
→ audit/report
→ cleanup/rollback when possible
```

## 7. Architecture tests
Architecture boundaries must be tested. At minimum:

- core must not import adapters,
- core must not import UI,
- core must not import subprocess/network clients,
- application must not call APIs directly,
- UI must not execute operations directly,
- sensitive operations must use safety pipeline.
