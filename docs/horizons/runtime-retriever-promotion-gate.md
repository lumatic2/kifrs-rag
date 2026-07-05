# Horizon: Runtime Retriever Promotion Gate

> Status: active
> Created: 2026-07-05
> Previous: `docs/horizons/workflow-coverage-expansion.md`

## Goal

Decide whether the opt-in repair retriever stack should become a runtime default, and make the promote/defer
decision reversible, measurable, and public-safe.

## Why This Exists

The RAG quality work produced a stronger opt-in retriever stack, but the product default is still guarded.
That is the correct safety posture until runtime regression, latency, failure-boundary, operator command,
and rollback evidence are tied together. This horizon turns "it scores well in eval" into a product promotion
decision.

## Milestones

### RPG1. Promotion Evidence Inventory

Status: completed

- Deliverable: `docs/reports/2026-07-05-rpg1-promotion-evidence-inventory.md`
- Acceptance: current eval gates, default guard, quality reports, failure boundaries, and product trust
  evidence are inventoried.

### RPG2. Regression And Latency Gate

Status: active

- Deliverable: regression/latency gate, tests, `docs/reports/2026-07-05-rpg2-regression-latency-gate.md`
- Acceptance: promotion cannot pass unless recall/citation regressions and basic runtime cost limits are
  explicitly checked.

### RPG3. Failure And Rollback Policy

Status: pending

- Deliverable: rollback policy validator, tests, `docs/reports/2026-07-05-rpg3-failure-rollback-policy.md`
- Acceptance: failed promotion has a clear fallback to the current default retriever and operator remediation.

### RPG4. Operator Promotion Command

Status: pending

- Deliverable: promotion command dry-run, tests, `docs/reports/2026-07-05-rpg4-operator-promotion-command.md`
- Acceptance: operator can see promote/defer status and required evidence without editing runtime code by hand.

### RPG5. Promotion Gate Close Report

Status: pending

- Deliverable: close gate script, tests, `docs/reports/2026-07-05-runtime-retriever-promotion-gate-close-report.md`
- Acceptance: the horizon closes with an explicit `promote`, `defer`, or `block` result and rollback evidence.

## Decision Log

- Promotion is not assumed. `defer` is a valid product decision if runtime or authorization evidence is weak.
- This horizon does not add protected source text, private payload, embeddings, or dogfood material to the repo.
