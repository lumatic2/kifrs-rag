# Horizon: Source Body Ingestion Controlled Lane

> Status: closed
> Created: 2026-07-05
> Previous: `docs/horizons/real-local-parser-prototype.md`

## Goal

Implement one controlled non-IFRS source-body ingestion lane with explicit authorization, parser/chunker policy, retrieval gate, and public-safe reporting.

## Milestones

### SBI1. Source Class Selection And Authorization Boundary

Status: completed

- Deliverable: `docs/reports/2026-07-05-sbi1-source-class-selection.md`
- Acceptance: one source class is selected with authorization status, allowed fields, forbidden fields, and fallback plan.

### SBI2. Source Body Policy Record

Status: completed

- Deliverable: policy record, validator, tests, `docs/reports/2026-07-05-sbi2-source-body-policy-record.md`
- Acceptance: storage, citation role, chunking, and retention policy are machine-validated.

### SBI3. Synthetic Body Parser And Chunker

Status: completed

- Deliverable: parser/chunker dry-run, tests, `docs/reports/2026-07-05-sbi3-synthetic-body-parser-chunker.md`
- Acceptance: synthetic body becomes public-safe chunks with no protected source text committed.

### SBI4. Retrieval Gate For Controlled Lane

Status: completed

- Deliverable: retrieval gate, tests, `docs/reports/2026-07-05-sbi4-controlled-lane-retrieval-gate.md`
- Acceptance: controlled chunks can be discovered as supporting interpretation or legal boundary evidence without changing K-IFRS primary evidence.

### SBI5. Controlled Lane Close Gate

Status: completed

- Deliverable: close gate script, tests, `docs/reports/2026-07-05-source-body-ingestion-controlled-lane-close-report.md`
- Acceptance: authorization, parser/chunker, retrieval, public-safe, and RAG regression gates pass.

## Decision Log

- This horizon must not scrape or store protected body text without explicit authorization.
- If authorization is absent, synthetic-body dry-run remains the maximum allowed implementation.
