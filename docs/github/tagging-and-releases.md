# Tagging and Releases

## Tags
Use annotated tags:

```powershell
git tag -a v0.1.0 -m "Phase 1 — Foundation, docs, repo, CI, architecture"
git push origin v0.1.0
```

## Releases
Every phase tag gets a GitHub Release.

## Versioning rule
- Phase X = `v0.X.0`.
- Never create `v1.0.0` without explicit user instruction.
