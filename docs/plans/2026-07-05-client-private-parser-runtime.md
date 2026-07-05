# Plan: Client-Private Parser Runtime

> Objective: `docs/OBJECTIVE.md`
> Horizon: `docs/horizons/client-private-parser-runtime.md`
> Previous gate: `docs/reports/2026-07-05-multi-authority-runtime-hardening-close-report.md`

## Summary

The previous horizon made runtime outputs separate primary, supporting, legal, fact, and client-private evidence. This horizon makes the client-private lane real enough for local operation: private files become structured facts and review questions through a local-only parser contract, then flow into runtime as `client_private_fact` without public body storage.

## Milestone / Step Tree

### CP1 — Private Parser Boundary Audit

- [ ] CP1.1 — Inventory existing private-parser surfaces. (verify: audit lists parser/redaction/upload/storage/deletion/runtime files)
- [ ] CP1.2 — Compare existing scaffolds to `client_private_fact` authority boundary. (verify: audit maps fields and gaps)
- [ ] CP1.3 — Classify CP2~CP5 implementation gaps. (verify: gap table exists)
- [ ] CP1.4 — Write CP1 report. (verify: `docs/reports/2026-07-05-cp1-private-parser-boundary-audit.md`)

### CP2 — Local Parser Runtime Contract

- [ ] CP2.1 — Define parser runtime output shape. (verify: focused parser contract tests)
- [ ] CP2.2 — Reject protected body-like fields. (verify: negative tests)
- [ ] CP2.3 — Preserve structured-facts-only public fixture. (verify: synthetic fixture only)
- [ ] CP2.4 — Write CP2 report.

### CP3 — Client-Private Evidence Adapter

- [ ] CP3.1 — Convert parser output to client-private authority references.
- [ ] CP3.2 — Attach references to review/statement surfaces as local-only facts.
- [ ] CP3.3 — Prove no primary promotion.
- [ ] CP3.4 — Write CP3 report.

### CP4 — Deletion And Retention Gate

- [ ] CP4.1 — Add retention/deletion attestation object.
- [ ] CP4.2 — Gate close on attestation state.
- [ ] CP4.3 — Write operator runbook/report.

### CP5 — Private Runtime Close Demo

- [ ] CP5.1 — Build local-only private runtime demo fixture.
- [ ] CP5.2 — Implement close gate.
- [ ] CP5.3 — Run carried multi-authority/RAG regressions.
- [ ] CP5.4 — Close horizon.

## Stop Conditions

- Stop if real private source body must be committed.
- Stop if parser output requires raw private text in report or test fixtures.
- Stop if client-private facts are promoted into K-IFRS primary evidence.
