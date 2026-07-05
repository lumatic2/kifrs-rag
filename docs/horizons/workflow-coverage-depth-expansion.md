# Horizon: Workflow Coverage Depth Expansion

> Status: active
> Created: 2026-07-05
> Previous: `docs/horizons/external-source-body-connector-expansion.md`

## Goal

Expand automation coverage depth against the firm-service map. The product already has selected workflow evidence, but the Objective asks how far accountant work can be automated; that requires a broader and more explicit sampling plan across service lines and workflow types.

This horizon does not introduce external accountant outreach or packaging. It deepens internal, public-safe workflow evidence.

## Milestones

### WCD1. Service-Line Coverage Rerank

Status: completed

- Deliverable: rerank script, tests, `docs/reports/2026-07-05-wcd1-service-line-coverage-rerank.md`
- Acceptance: firm-service map gaps are ranked by automation value, evidence availability, implementation cost, and public-safety boundary.

### WCD2. Workflow Sample Contract Pack

Status: completed

- Deliverable: workflow sample contract script/report.
- Acceptance: selected workflow samples have input facts, authority needs, output surface, review boundary, and failure states.

### WCD3. Minimal Adapter Expansion

Status: completed

- Deliverable: minimal adapter script/report for the highest-ranked workflow.
- Acceptance: at least one additional workflow produces decision-prep metadata without protected payload exposure.

### WCD4. Coverage Depth Metric Update

Status: completed

- Deliverable: coverage metric script/report.
- Acceptance: automation coverage depth is updated with service-line and workflow-surface counts.

### WCD5. Horizon Close And Demo Rehearsal Handoff

Status: active

- Deliverable: close report.
- Acceptance: workflow coverage depth status is closed and demo rehearsal quality loop is named.

## Decision Log

- Expand internal workflow evidence before any external feedback or packaging.
- Use the firm-service map as the sampling frame.
- Keep source/body/private payload constraints inherited from prior horizons.
