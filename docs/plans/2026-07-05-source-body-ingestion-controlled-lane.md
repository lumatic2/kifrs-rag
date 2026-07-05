# Plan: Source Body Ingestion Controlled Lane

> Objective: `docs/OBJECTIVE.md`
> Horizon: `docs/horizons/source-body-ingestion-controlled-lane.md`

## Summary

This horizon adds one controlled non-IFRS source-body ingestion lane with authorization and public-safe gates.

## Milestone / Step Tree

### SBI1 — Source Class Selection And Authorization Boundary

- [x] SBI1.1 — Compare candidate source classes.
- [x] SBI1.2 — Select one lane and document authorization boundary.
- [x] SBI1.3 — Write SBI1 report.

### SBI2 — Source Body Policy Record

- [ ] SBI2.1 — Define machine-readable policy record.
- [ ] SBI2.2 — Add validator and tests.
- [ ] SBI2.3 — Write SBI2 report.

### SBI3 — Synthetic Body Parser And Chunker

- [ ] SBI3.1 — Build synthetic body fixture.
- [ ] SBI3.2 — Implement parser/chunker dry-run.
- [ ] SBI3.3 — Add tests and report.

### SBI4 — Retrieval Gate For Controlled Lane

- [ ] SBI4.1 — Define controlled-lane retrieval expectation.
- [ ] SBI4.2 — Add retrieval gate without changing primary K-IFRS authority.
- [ ] SBI4.3 — Write report.

### SBI5 — Controlled Lane Close Gate

- [ ] SBI5.1 — Implement close gate.
- [ ] SBI5.2 — Run public-safe and RAG regressions.
- [ ] SBI5.3 — Close horizon.

## Decision Log

- If authorization is absent, implementation stays synthetic-body only.
- Protected source body is not committed.
