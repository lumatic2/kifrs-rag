# Plan: End-to-End Demo Scenario

> Objective: `docs/OBJECTIVE.md`
> Horizon: `docs/horizons/end-to-end-demo-scenario.md`

## Summary

This horizon turns the completed product-weakness work into one end-to-end demonstration. The demo should explain: local source intake is controlled, accounting workflow output is review-ready, retriever default promotion is conservative, and the operator can run, inspect, diagnose, and recover the path.

## Milestone / Step Tree

### E2E1 — Demo Asset Inventory And Storyboard

- [x] E2E1.1 — Inventory required public-safe reports.
- [x] E2E1.2 — Order reports into a single demo story.
- [x] E2E1.3 — Write E2E1 report.

### E2E2 — Scenario Contract

- [x] E2E2.1 — Define stage-level contract from input to review checkpoint.
- [x] E2E2.2 — Encode required artifacts and public-safety rules.
- [x] E2E2.3 — Write scenario contract report.

### E2E3 — Demo Packet Builder

- [x] E2E3.1 — Build one ordered packet/index from reports.
- [x] E2E3.2 — Add operator command and rerun hints.
- [x] E2E3.3 — Write packet report.

### E2E4 — Demo Smoke And Navigation Gate

- [ ] E2E4.1 — Verify all packet links exist. `(next)`
- [ ] E2E4.2 — Verify public-safety and missing-report failure path.
- [ ] E2E4.3 — Write smoke report.

### E2E5 — Horizon Close Gate

- [ ] E2E5.1 — Combine E2E1~E2E4 evidence.
- [ ] E2E5.2 — State demo-ready result and residual risks.
- [ ] E2E5.3 — Close horizon or name the next integration horizon.

## Decision Log

- Demo scenario first, packaging later.
- Use synthetic/public-safe evidence only.
- No external accountant outreach in this plan.
- Continue through the horizon unless a protected-data, secret, or missing-critical-artifact blocker appears.
