# Plan: Private Parser Realism Hardening

> Objective: `docs/OBJECTIVE.md`
> Horizon: `docs/horizons/private-parser-realism-hardening.md`

## Summary

This horizon addresses the Objective gap that private parser evidence is still fixture-heavy. The goal is to harden realistic local-file handling boundaries without exposing protected content or starting real ingestion without explicit authorization.

## Milestone / Step Tree

### PPR1 — Authorization-Safe Adapter Proof Plan

- [x] PPR1.1 — Inventory private parser evidence and authorization gates.
- [x] PPR1.2 — Define local-only adapter proof rules.
- [x] PPR1.3 — Write PPR1 proof plan report.

### PPR2 — Realistic Local Fixture Adapter Contract

- [ ] PPR2.1 — Define file classes and structured output contract. `(next)`
- [ ] PPR2.2 — Define parser failure and redaction states.
- [ ] PPR2.3 — Write adapter contract report.

### PPR3 — Deletion And Retention Rehearsal

- [ ] PPR3.1 — Define local artifact lifecycle.
- [ ] PPR3.2 — Simulate retained/deleted evidence states.
- [ ] PPR3.3 — Write deletion rehearsal report.

### PPR4 — Parser Leak And Public Report Gate

- [ ] PPR4.1 — Define public report leak checks.
- [ ] PPR4.2 — Add synthetic negative cases.
- [ ] PPR4.3 — Write leak gate report.

### PPR5 — Horizon Close And Source Connector Handoff

- [ ] PPR5.1 — Combine PPR1~PPR4 evidence.
- [ ] PPR5.2 — Close horizon and name next objective-gap horizon.
- [ ] PPR5.3 — Sync ROADMAP/OBJECTIVE/progress map.

## Decision Log

- No real protected payload handling without explicit user authorization.
- This horizon improves parser realism, not packaging.
- External accountant feedback remains parked.
