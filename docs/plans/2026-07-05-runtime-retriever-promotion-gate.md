# Plan: Runtime Retriever Promotion Gate

> Objective: `docs/OBJECTIVE.md`
> Horizon: `docs/horizons/runtime-retriever-promotion-gate.md`

## Summary

This horizon turns the opt-in retriever repair stack into a promotion decision with regression, latency,
failure-boundary, operator-command, and rollback evidence.

## Milestone / Step Tree

### RPG1 — Promotion Evidence Inventory

- [x] RPG1.1 — Inventory current retriever eval, default guard, and product trust evidence.
- [x] RPG1.2 — Classify evidence as promotion-supporting, promotion-blocking, or advisory.
- [x] RPG1.3 — Write RPG1 report.

### RPG2 — Regression And Latency Gate

- [x] RPG2.1 — Define minimum recall/citation and runtime cost checks.
- [x] RPG2.2 — Implement promotion regression/latency gate.
- [x] RPG2.3 — Add tests and report.

### RPG3 — Failure And Rollback Policy

- [x] RPG3.1 — Define rollback states and failure cases.
- [x] RPG3.2 — Validate fallback to current default retriever.
- [x] RPG3.3 — Add tests and report.

### RPG4 — Operator Promotion Command

- [ ] RPG4.1 — Define operator-facing promote/defer command output.
- [ ] RPG4.2 — Implement dry-run command without changing runtime default by accident.
- [ ] RPG4.3 — Add tests and report.

### RPG5 — Promotion Gate Close Report

- [ ] RPG5.1 — Implement close gate.
- [ ] RPG5.2 — Run carried RAG/product trust regressions.
- [ ] RPG5.3 — Close horizon with promote/defer/block result.

## Decision Log

- Promotion requires evidence; it is not the default outcome.
- No runtime default is changed without an explicit gate result and rollback path.
- No protected K-IFRS body, private payload, embedding dump, dogfood material, or secret is committed.
