# Horizon: End-to-End Demo Scenario

> Status: active
> Created: 2026-07-05
> Previous: `docs/plans/2026-07-05-product-weakness-horizon-candidates.md`

## Goal

Turn the completed product-weakness chain into one public-safe demo scenario that a firm-facing operator can explain from input to review-ready output.

This horizon does not add a new accounting domain first. It proves that the existing parser, source lane, workflow adapter, retriever gate, and operator surface can be walked as one coherent product story.

## Milestones

### E2E1. Demo Asset Inventory And Storyboard

Status: completed

- Deliverable: inventory script, tests, `docs/reports/2026-07-05-e2e1-demo-asset-inventory.md`
- Acceptance: required reports exist, are ordered into one scenario, and expose no protected local payloads.

### E2E2. Scenario Contract

Status: active

- Deliverable: scenario contract script/report.
- Acceptance: demo stages have input, evidence, decision-prep output, review checkpoint, operator command, and failure boundary.

### E2E3. Demo Packet Builder

Status: pending

- Deliverable: ordered demo packet/index under `docs/reports/end-to-end-demo/`.
- Acceptance: operator can open one packet and follow the demo without reading ROADMAP internals.

### E2E4. Demo Smoke And Navigation Gate

Status: pending

- Deliverable: smoke gate script/tests/report.
- Acceptance: every referenced report exists, public-safety checks pass, and the packet is navigable.

### E2E5. Horizon Close Gate

Status: pending

- Deliverable: close report.
- Acceptance: the end-to-end demo scenario is ready for a local run-through and its remaining risks are explicit.

## Decision Log

- Use existing synthetic/public-safe artifacts only. No protected PDFs, DB dumps, embeddings, dogfood, private payloads, or secrets are included.
- The demo is a local toolkit walkthrough, not SaaS packaging.
- No external accountant outreach is part of this horizon.
