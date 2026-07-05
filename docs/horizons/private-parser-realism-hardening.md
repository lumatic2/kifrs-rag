# Horizon: Private Parser Realism Hardening

> Status: active
> Created: 2026-07-05
> Previous: `docs/horizons/rag-quality-fresh-validation.md`

## Goal

Move private/local parser evidence from fixture-heavy proof toward realistic local-file handling while preserving authorization, deletion, and public-safe reporting boundaries.

This horizon does not ingest real protected files by default. It first makes the authorization-safe adapter proof explicit, then hardens dry-run, deletion, leak, and close gates.

## Milestones

### PPR1. Authorization-Safe Adapter Proof Plan

Status: completed

- Deliverable: proof plan script, tests, `docs/reports/2026-07-05-ppr1-authorization-safe-adapter-proof.md`
- Acceptance: actual protected payload handling is gated, local-only, deletion-aware, and public-safe before any real adapter work.

### PPR2. Realistic Local Fixture Adapter Contract

Status: active

- Deliverable: adapter contract script/report.
- Acceptance: supported file classes, parser outputs, redaction fields, and failure modes are explicit.

### PPR3. Deletion And Retention Rehearsal

Status: pending

- Deliverable: deletion rehearsal script/report.
- Acceptance: local artifact lifecycle is simulated with clear retained/deleted evidence states.

### PPR4. Parser Leak And Public Report Gate

Status: pending

- Deliverable: leak gate script/tests/report.
- Acceptance: public reports contain structured facts and statuses only, not protected payload contents.

### PPR5. Horizon Close And Source Connector Handoff

Status: pending

- Deliverable: close report.
- Acceptance: private parser realism status is closed and next objective-gap horizon is named.

## Decision Log

- No real protected file ingestion without explicit user authorization.
- Public reports may mention file classes and structured-facts-only schemas, not raw private content.
- Packaging and external accountant feedback are outside this horizon.
