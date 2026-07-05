# Plan: Client-Private Parser Runtime

> Objective: `docs/OBJECTIVE.md`
> Horizon: `docs/horizons/client-private-parser-runtime.md`
> Previous gate: `docs/reports/2026-07-05-multi-authority-runtime-hardening-close-report.md`

## Summary

The previous horizon made runtime outputs separate primary, supporting, legal, fact, and client-private evidence. This horizon makes the client-private lane real enough for local operation: private files become structured facts and review questions through a local-only parser contract, then flow into runtime as `client_private_fact` without public body storage.

## Milestone / Step Tree

### CP1 — Private Parser Boundary Audit

- [x] CP1.1 — Inventory existing private-parser surfaces. (verify: audit lists parser/redaction/upload/storage/deletion/runtime files)
- [x] CP1.2 — Compare existing scaffolds to `client_private_fact` authority boundary. (verify: audit maps fields and gaps)
- [x] CP1.3 — Classify CP2~CP5 implementation gaps. (verify: gap table exists)
- [x] CP1.4 — Write CP1 report. (verify: `docs/reports/2026-07-05-cp1-private-parser-boundary-audit.md`)

### CP2 — Local Parser Runtime Contract

- [x] CP2.1 — Define parser runtime output shape. (verify: focused parser contract tests)
- [x] CP2.2 — Reject protected body-like fields. (verify: negative tests)
- [x] CP2.3 — Preserve structured-facts-only public fixture. (verify: synthetic fixture only)
- [x] CP2.4 — Write CP2 report.

### CP3 — Client-Private Evidence Adapter

- [x] CP3.1 — Convert parser output to client-private authority references.
- [x] CP3.2 — Attach references to review/statement surfaces as local-only facts.
- [x] CP3.3 — Prove no primary promotion.
- [x] CP3.4 — Write CP3 report.

### CP4 — Deletion And Retention Gate

- [x] CP4.1 — Add retention/deletion attestation object.
- [x] CP4.2 — Gate close on attestation state.
- [x] CP4.3 — Write operator runbook/report.

### CP5 — Private Runtime Close Demo

- [x] CP5.1 — Build local-only private runtime demo fixture.
- [x] CP5.2 — Implement close gate.
- [x] CP5.3 — Run carried multi-authority/RAG regressions.
- [x] CP5.4 — Close horizon.

## Stop Conditions

- Stop if real private source body must be committed.
- Stop if parser output requires raw private text in report or test fixtures.
- Stop if client-private facts are promoted into K-IFRS primary evidence.
