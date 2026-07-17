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

- [x] PPR2.1 — Define file classes and structured output contract.
- [x] PPR2.2 — Define parser failure and redaction states.
- [x] PPR2.3 — Write adapter contract report.

### PPR3 — Deletion And Retention Rehearsal

- [x] PPR3.1 — Define local artifact lifecycle.
- [x] PPR3.2 — Simulate retained/deleted evidence states.
- [x] PPR3.3 — Write deletion rehearsal report.

### PPR4 — Parser Leak And Public Report Gate

- [x] PPR4.1 — Define public report leak checks.
- [x] PPR4.2 — Add synthetic negative cases.
- [x] PPR4.3 — Write leak gate report.

### PPR5 — Horizon Close And Source Connector Handoff

- [x] PPR5.1 — Combine PPR1~PPR4 evidence.
- [x] PPR5.2 — Close horizon and name next objective-gap horizon.
- [x] PPR5.3 — Sync ROADMAP/OBJECTIVE/progress map.

## Decision Log

- No real protected payload handling without explicit user authorization.
- This horizon improves parser realism, not packaging.
- External accountant feedback remains parked.
