# Horizon: Workflow Coverage Expansion

> Status: closed
> Created: 2026-07-05
> Previous: `docs/horizons/source-body-ingestion-controlled-lane.md`

## Goal

Expand accountant-work automation coverage beyond the existing 1109/1115/1116 review-pack surface using the firm-service map and objective coverage axes.

## Milestones

### WCE1. Coverage Gap Ranking

Status: completed

- Deliverable: `docs/reports/2026-07-05-wce1-coverage-gap-ranking.md`
- Acceptance: candidate domains are ranked by firm-service value, data availability, determinism, and verification cost.

### WCE2. First New Workflow Candidate Contract

Status: completed

- Deliverable: workflow contract, tests, `docs/reports/2026-07-05-wce2-first-workflow-contract.md`
- Acceptance: one domain is selected and scoped to decision-prep draft output.

### WCE3. Minimal Review-Pack Adapter

Status: completed

- Deliverable: adapter code, tests, `docs/reports/2026-07-05-wce3-minimal-review-pack-adapter.md`
- Acceptance: selected workflow can produce at least a structured summary and human-review checklist.

### WCE4. Coverage Metric Update

Status: completed

- Deliverable: coverage metric script/report, tests, `docs/reports/2026-07-05-wce4-coverage-metric-update.md`
- Acceptance: objective coverage map reflects the new workflow candidate and its limits.

### WCE5. Workflow Coverage Close Gate

Status: completed

- Deliverable: close gate script, tests, `docs/reports/2026-07-05-workflow-coverage-expansion-close-report.md`
- Acceptance: new coverage evidence is connected to product trust, parser/runtime, and firm-facing demo surfaces.

## Decision Log

- Breadth is only useful if each new workflow has a testable output and human-review boundary.
- Candidate domains include 1113 fair value, 1036 impairment, 1037 provisions, 1110 consolidation, and disclosure/closing support.
