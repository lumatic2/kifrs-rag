# Horizon: Demo Rehearsal Improvement Hardening

> Status: closed
> Created: 2026-07-06
> Previous: `docs/horizons/demo-rehearsal-quality-loop.md`

## Goal

Implement the three internal fixes from DRQ4 so the demo rehearsal evidence is easier to trust and operate:
timing variance threshold, freshness metadata, and one-screen operator summary.

This horizon stays local and public-safe. It does not change default retriever behavior or introduce external dependencies.

## Milestones

### DRI1. Retriever Timing Threshold

Status: completed

- Deliverable: quality checklist update and tests, `docs/reports/2026-07-05-drq2-demo-run-quality-checklist.md`
- Acceptance: `retriever-decision` has an explicit expected timing variance threshold.

### DRI2. Rehearsal Freshness Metadata

Status: completed

- Deliverable: rehearsal evidence update and tests, `docs/reports/2026-07-05-drq3-demo-rehearsal-evidence.md`
- Acceptance: stage results and report expose generated-at freshness metadata and freshness checks.

### DRI3. Operator Summary Surface

Status: completed

- Deliverable: progress map summary update and tests, `docs/reports/2026-07-05-accounting-intelligence-progress-map.md`
- Acceptance: progress map starts with a compact operator summary.

### DRI4. Horizon Close Gate

Status: completed

- Deliverable: close gate report, `docs/reports/2026-07-06-demo-rehearsal-improvement-hardening-close-report.md`
- Acceptance: DRI1~DRI3 evidence is verified and the horizon is closed.

## Close Result

`demo_rehearsal_improvements_hardened` — DRQ4-1, DRQ4-2, and DRQ4-3 are implemented and verified.

## Decision Log

- Implement all three DRQ4 backlog items as internal evidence hardening.
- Keep outputs public-safe and synthetic.
- Do not add external dependencies.
