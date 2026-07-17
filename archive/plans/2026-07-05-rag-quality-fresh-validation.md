# Plan: RAG Quality Fresh Validation

> Objective: `docs/OBJECTIVE.md`
> Horizon: `docs/horizons/rag-quality-fresh-validation.md`

## Summary

This horizon answers the next objective gap: whether current RAG quality is strong enough to trust in the product path. It starts by fixing the validation contract, then captures baseline and opt-in retriever evidence, then closes with a promotion/defer decision.

## Milestone / Step Tree

### RQF1 — Validation Corpus And Acceptance Contract

- [x] RQF1.1 — Inventory trustworthy RAG quality commands and reports.
- [x] RQF1.2 — Define metric thresholds and protected-data boundaries.
- [x] RQF1.3 — Write RQF1 validation contract report.

### RQF2 — Current Retriever Baseline Snapshot

- [x] RQF2.1 — Capture current default retriever baseline.
- [x] RQF2.2 — Record missing local data blockers if any.
- [x] RQF2.3 — Write baseline snapshot report.

### RQF3 — Opt-In Retriever Regression Matrix

- [x] RQF3.1 — Compare opt-in retriever against baseline.
- [x] RQF3.2 — Record regressions, latency, and rollback evidence.
- [x] RQF3.3 — Write regression matrix report.

### RQF4 — Promotion Decision Gate

- [x] RQF4.1 — Evaluate promote/defer/rollback criteria.
- [x] RQF4.2 — Confirm explicit authorization requirement for default changes.
- [x] RQF4.3 — Write promotion decision report.

### RQF5 — Horizon Close And Next Gap Handoff

- [x] RQF5.1 — Combine RQF1~RQF4 evidence.
- [x] RQF5.2 — Close horizon and name next objective-gap horizon.
- [x] RQF5.3 — Sync ROADMAP/OBJECTIVE/progress map.

## Decision Log

- Start with public-safe validation contract because current gap evidence says default retriever promotion is deferred.
- Do not promote any retriever default in this horizon without stronger evidence and explicit authorization.
- Packaging and external accountant feedback are excluded.
