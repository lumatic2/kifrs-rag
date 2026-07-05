# Horizon: External Source Body Connector Expansion

> Status: active
> Created: 2026-07-05
> Previous: `docs/horizons/private-parser-realism-hardening.md`

## Goal

Move external source evidence beyond metadata/demo notes into a controlled source-body connector expansion plan with authorization, policy, parsing, chunking, retrieval, and public-safe reporting gates.

This horizon does not scrape or redistribute protected third-party content by default. It first selects a source class and policy boundary, then implements only authorized/synthetic-safe body handling evidence.

## Milestones

### ESB1. Source-Body Connector Selection And Policy Gate

Status: completed

- Deliverable: selection/policy script, tests, `docs/reports/2026-07-05-esb1-source-body-connector-selection.md`
- Acceptance: source class, authorization boundary, allowed metadata/body fields, and public-safe report rules are explicit.

### ESB2. Synthetic Source-Body Fixture Contract

Status: completed

- Deliverable: fixture contract script/report.
- Acceptance: parser input/output schema and forbidden raw-body publication rules are explicit.

### ESB3. Chunking And Retrieval Dry Run

Status: completed

- Deliverable: chunk/retrieval dry-run script/report.
- Acceptance: chunks are synthetic/authorized and retrieval evidence stays public-safe.

### ESB4. Connector Leak And Policy Gate

Status: active

- Deliverable: leak/policy gate script/tests/report.
- Acceptance: connector reports do not expose protected body text or secrets.

### ESB5. Horizon Close And Workflow Coverage Handoff

Status: pending

- Deliverable: close report.
- Acceptance: external source-body connector expansion status is closed and next objective-gap horizon is named.

## Decision Log

- No protected source-body ingestion without explicit authorization.
- Public reports may include source class, policy, schema, status, metrics, and synthetic snippets only.
- Packaging and external accountant feedback are outside this horizon.
