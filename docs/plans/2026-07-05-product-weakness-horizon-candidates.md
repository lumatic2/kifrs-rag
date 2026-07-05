# Plan: Product Weakness Horizon Candidates

> Objective: `docs/OBJECTIVE.md`
> Queue owner: Accounting Intelligence Expansion
> Status: candidate sequence, with `real-local-parser-prototype` active

## Summary

The product is no longer weak because it lacks isolated scripts. Its weak points are now product-shaped:
realistic local inputs, non-IFRS evidence, broader accountant workflow coverage, runtime promotion safety,
and operator usability. The next horizons should close those gaps in dependency order.

## Candidate Horizon Queue

### 1. `real-local-parser-prototype`

- Product weakness: real accountant work starts from contracts, trial balances, policies, and working papers,
  but the current parser path is still mostly contract/synthetic.
- Product value: proves the toolkit can turn local private material into structured facts without committing
  private payload.
- Milestones: RLP1 asset inventory, RLP2 local fixture adapter, RLP3 deletion simulation, RLP4 leak tests,
  RLP5 close gate.
- Status: closed.
- Plan: `docs/plans/2026-07-05-real-local-parser-prototype.md`.

### 2. `source-body-ingestion-controlled-lane`

- Product weakness: K-IFRS alone is not enough for actual accounting work; interpretive, regulatory, legal,
  filing, and client-private evidence need controlled dataization.
- Product value: proves one non-IFRS source lane can be parsed, chunked, retrieved, and reported under an
  explicit authority/storage policy.
- Milestones: SBI1 source selection, SBI2 policy record, SBI3 synthetic parser/chunker, SBI4 retrieval gate,
  SBI5 close gate.
- Status: active.
- Plan: `docs/plans/2026-07-05-source-body-ingestion-controlled-lane.md`.

### 3. `workflow-coverage-expansion`

- Product weakness: existing automation evidence is still concentrated around a small set of standards and
  review-pack surfaces.
- Product value: expands the firm-service map into one more accountant workflow with a testable
  decision-prep output.
- Milestones: WCE1 coverage ranking, WCE2 workflow contract, WCE3 minimal adapter, WCE4 coverage metric,
  WCE5 close gate.
- Status: planned.
- Plan: `docs/plans/2026-07-05-workflow-coverage-expansion.md`.

### 4. `runtime-retriever-promotion-gate`

- Product weakness: the best evaluated retriever stack exists as opt-in repair behavior, not as a product
  default.
- Product value: gives a defensible promote/defer/rollback decision for the runtime retriever.
- Milestones: RPG1 promotion evidence inventory, RPG2 regression and latency gate, RPG3 failure/rollback
  policy, RPG4 operator promotion command, RPG5 close gate.
- Status: planned.
- Plan: `docs/plans/2026-07-05-runtime-retriever-promotion-gate.md`.

### 5. `operator-experience-hardening`

- Product weakness: the toolkit has many scripts and reports, but the operator path is hard to discover and
  recover.
- Product value: makes the local toolkit runnable by following one command/report surface instead of reading
  internal ROADMAP history.
- Milestones: OEH1 command inventory, OEH2 run doctor, OEH3 report manifest, OEH4 recovery playbook,
  OEH5 close gate.
- Status: planned.
- Plan: `docs/plans/2026-07-05-operator-experience-hardening.md`.

## Parked Integration Candidate

### `end-to-end-demo-scenario`

- Product weakness: demos are still report-heavy rather than one continuous "input to review pack" experience.
- Why parked: it should consume the five horizons above instead of preceding them.
- Likely trigger: after local parser, controlled source lane, workflow coverage, promotion gate, and operator
  hardening are closed.

## Decision Log

- The active next horizon is now `source-body-ingestion-controlled-lane`.
- `real-accountant-session` stays parked until the user explicitly reopens actual outreach or feedback capture.
- No protected K-IFRS text, private client payload, source body, parsed database, embedding dump, dogfood
  material, or secret is introduced by this queue.
