# Architecture Constitution

These rules are permanent unless changed through an ADR.

## 1. Core stays small and stable
The core contains essential domain rules and pure models. It must not depend on external systems, UI, shell, network, filesystem mutation, database, or APIs.

## 2. Edges depend on the center
Adapters depend on ports/application/core. Core never depends on adapters.

## 3. UI is not business logic
The TUI collects user choices and displays state. It must not decide download rules, safety risk, transcript rules, or file policies.

## 4. Every operation has dry-run
Download, transcription, cleanup, file write, batch processing, cookie use, installation, and packaging operations must have a dry-run or preflight plan.

## 5. Sensitive actions are governed
Sensitive actions must pass through risk classification, pre-validation, confirmation, execution, post-validation, logging, and report generation.

## 6. Secrets are never committed
No API key, token, cookie, local config, transcript, download, or private log enters the public repository.

## 7. GPU-only transcription
The project intentionally does not fall back to CPU. If CUDA/GPU is unavailable, transcription aborts with a helpful message.

## 8. User configuration is local
Weather city, API providers, keys, output folders, theme, language, and cookie choices are user-local settings.

## 9. Errors are classified
Errors must become structured app errors with severity, code, user message, technical detail, and recovery suggestion where possible.

## 10. Tests protect architecture
Tests must protect behavior and boundaries. Architecture tests are required.

## 11. Decisions are recorded
Architectural decisions must be recorded in ADRs.

## 12. Phase discipline is mandatory
Do not skip phase boundaries. Do not create `v1.0.0` without explicit user approval.
