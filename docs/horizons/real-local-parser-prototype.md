# Horizon: Real Local Parser Prototype

> Status: active
> Created: 2026-07-05
> Previous: `docs/horizons/product-trust-and-quality-evidence.md`

## Goal

Move from parser contracts and synthetic dry-runs toward a realistic local parser prototype while preserving the no-public-private-payload boundary.

## Milestones

### RLP1. Parser Prototype Asset Inventory

Status: active

- Deliverable: `docs/reports/2026-07-05-rlp1-parser-prototype-asset-inventory.md`
- Acceptance: existing parser contracts, adapter scaffolds, deletion gates, and dry-run fixtures are mapped.

### RLP2. Local Fixture Parser Adapter

- Deliverable: parser adapter code, tests, `docs/reports/2026-07-05-rlp2-local-fixture-parser-adapter.md`
- Acceptance: a local fixture-like input becomes structured facts and review questions without copying raw private text.

### RLP3. Deletion Automation Simulation

- Deliverable: deletion simulation gate, tests, `docs/reports/2026-07-05-rlp3-deletion-automation-simulation.md`
- Acceptance: parser output cannot close until retention/deletion state is attested.

### RLP4. Private Payload Leak Tests

- Deliverable: leak-test script, tests, `docs/reports/2026-07-05-rlp4-private-payload-leak-tests.md`
- Acceptance: body-like, identifier-like, OCR-like, and embedding-like fields are rejected from public artifacts.

### RLP5. Local Parser Prototype Close Gate

- Deliverable: close gate script, tests, `docs/reports/2026-07-05-real-local-parser-prototype-close-report.md`
- Acceptance: prototype path is demonstrable with synthetic/local-safe fixtures and no public private payload.

## Decision Log

- Real client files are not introduced unless the user explicitly provides local-only material later.
- Public repo artifacts remain schema, synthetic fixture, tests, and reports only.
