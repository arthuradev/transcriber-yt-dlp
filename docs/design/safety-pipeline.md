# Safety Pipeline

Every operation follows this pipeline:

```text
UserIntent
→ StructuredCommand
→ RiskClassification
→ DryRunPlan
→ PreValidation
→ Confirmation
→ Execution
→ PostValidation
→ AuditLog
→ FinalReport
→ Cleanup/Rollback if possible
```

## Risk levels
- Low: metadata read, settings read.
- Medium: public download, conversion, transcript generation.
- High: cookies, batch download, overwrite, private URL, LLM cleanup.
- Critical: arbitrary shell, deleting in bulk, saving secrets, bypass attempts.

## Critical actions
Blocked by default unless a future ADR explicitly allows them.
