# Horizon: RAG Quality Fresh Validation

> Status: closed
> Created: 2026-07-05
> Previous: `docs/horizons/end-to-end-demo-scenario.md`

## Goal

Revalidate K-IFRS RAG quality with a fresh, public-safe acceptance contract before any default retriever promotion or deeper accounting workflow expansion.

This horizon does not change the default retriever at the start. It creates stronger evidence first, then decides whether the opt-in repair retriever remains deferred or can be promoted later under explicit authorization.

## Milestones

### RQF1. Validation Corpus And Acceptance Contract

Status: completed

- Deliverable: validation contract script, tests, `docs/reports/2026-07-05-rqf1-validation-contract.md`
- Acceptance: RAG quality commands, dataset boundaries, metrics, promotion blockers, and public-safety rules are explicit.

### RQF2. Current Retriever Baseline Snapshot

Status: completed

- Deliverable: baseline snapshot script/report.
- Acceptance: current default retriever quality is measured against available public-safe eval metadata or documented as blocked by missing local private assets.

### RQF3. Opt-In Retriever Regression Matrix

Status: completed

- Deliverable: regression matrix script/report.
- Acceptance: opt-in repair retriever is compared against the baseline with pass/fail and rollback evidence.

### RQF4. Promotion Decision Gate

Status: completed

- Deliverable: promote/defer/rollback report.
- Acceptance: result is explicit, reversible, and does not promote defaults without stronger evidence and authorization.

### RQF5. Horizon Close And Next Gap Handoff

Status: completed

- Deliverable: close report.
- Acceptance: RAG quality status is closed as promote/defer/blocked and the next objective-gap horizon is named.

## Decision Log

- Default retriever remains unchanged until this horizon produces stronger evidence.
- No protected K-IFRS source text, DB dump, embeddings, dogfood, private payloads, or secrets are included in public reports.
- Packaging and external accountant feedback are outside this horizon.

## Close Result

- Result: `defer`
- Evidence: `docs/reports/2026-07-05-rag-quality-fresh-validation-close-report.md`
- Default retriever change: forbidden
- Next horizon: `private-parser-realism-hardening`
