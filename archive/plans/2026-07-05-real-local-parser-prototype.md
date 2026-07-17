# Plan: Real Local Parser Prototype

> Objective: `docs/OBJECTIVE.md`
> Horizon: `docs/horizons/real-local-parser-prototype.md`

## Summary

This horizon makes the private parser path more realistic while staying local-only and public-safe.

## Milestone / Step Tree

### RLP1 — Parser Prototype Asset Inventory

- [x] RLP1.1 — Inventory parser contracts, adapters, deletion gates, dry-runs.
- [x] RLP1.2 — Classify reusable vs missing pieces.
- [x] RLP1.3 — Write RLP1 report.

### RLP2 — Local Fixture Parser Adapter

- [x] RLP2.1 — Define adapter input/output contract.
- [x] RLP2.2 — Implement structured-facts-only conversion.
- [x] RLP2.3 — Add tests and report.

### RLP3 — Deletion Automation Simulation

- [x] RLP3.1 — Define deletion simulation states.
- [x] RLP3.2 — Gate close on deletion/retention attestation.
- [x] RLP3.3 — Add tests and report.

### RLP4 — Private Payload Leak Tests

- [x] RLP4.1 — Define forbidden payload patterns.
- [x] RLP4.2 — Add leak tests around parser outputs/reports.
- [x] RLP4.3 — Write leak-test report.

### RLP5 — Local Parser Prototype Close Gate

- [x] RLP5.1 — Implement close gate.
- [x] RLP5.2 — Run carried trust/runtime regressions.
- [x] RLP5.3 — Close horizon.

## Decision Log

- No real client files unless explicitly provided later.
- Public repo remains synthetic/schema/report only.
