# Horizon: Client-Private Parser Runtime

> Status: active
> Created: 2026-07-05
> Previous: `docs/horizons/multi-authority-runtime-hardening.md`

## Goal

Contracts, trial balances, accounting policies, and workpaper-like private files should enter the runtime only through a local-only parser boundary.

This horizon does not commit real client material. It defines and verifies the runtime path where private inputs become structured facts, review questions, deletion attestations, and local-only evidence references without entering the public repo.

## Why Now

`multi-authority-runtime-hardening` added the `client_private_fact` placeholder lane. The next missing product capability is turning local private files into that lane safely.

- Real private source bodies must stay local.
- Public artifacts may store schemas, fixtures, placeholder metadata, reports, and tests only.
- Parser output must be structured facts and review questions, not copied private text.
- Runtime output must show client-private facts separately from K-IFRS primary evidence.
- Deletion/retention state must be operator-attested before any firm-facing product surface.

## Milestones

### CP1. Private Parser Boundary Audit

Status: active

Deliverable:

- `docs/reports/2026-07-05-cp1-private-parser-boundary-audit.md`

Acceptance:

- Existing local parser, dry-run fixture, redaction, upload/storage, and adapter scaffolds are inventoried.
- Gaps to CP2~CP5 are classified.
- No real private material is required.

### CP2. Local Parser Runtime Contract

Deliverable:

- runtime parser contract object
- tests for structured-facts-only output
- `docs/reports/2026-07-05-cp2-local-parser-runtime-contract.md`

Acceptance:

- Parser outputs structured facts, source labels, review questions, and deletion policy only.
- Protected body-like fields are rejected.
- Public fixtures remain synthetic/placeholders.

### CP3. Client-Private Evidence Adapter

Deliverable:

- adapter from parser output to `client_private_fact` runtime authority references
- statement/review-pack linkage tests
- `docs/reports/2026-07-05-cp3-client-private-evidence-adapter.md`

Acceptance:

- Client-private facts stay in `client_private_fact`.
- They never become K-IFRS primary evidence or public fact evidence.

### CP4. Deletion And Retention Gate

Deliverable:

- deletion attestation gate
- local-only runbook report
- `docs/reports/2026-07-05-cp4-private-runtime-deletion-gate.md`

Acceptance:

- Runtime refuses to close without retention/deletion state.
- Gate output does not expose private content.

### CP5. Private Runtime Close Demo

Deliverable:

- `scripts/client_private_parser_runtime_gate.py`
- `tests/test_client_private_parser_runtime_gate.py`
- `docs/reports/2026-07-05-client-private-parser-runtime-close-report.md`

Acceptance:

- Demo shows local private fact placeholder flowing through parser contract, authority boundary, review output, and deletion gate.
- Multi-authority runtime gate remains passing.

## Decision Log

- This horizon does not parse or store real client files in the public repo.
- Parser work uses synthetic fixtures and placeholder metadata unless the user explicitly provides local private material for local-only testing.
- K-IFRS primary evidence remains separate from client-private facts.
