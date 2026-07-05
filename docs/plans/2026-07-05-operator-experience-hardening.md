# Plan: Operator Experience Hardening

> Objective: `docs/OBJECTIVE.md`
> Horizon: `docs/horizons/operator-experience-hardening.md`

## Summary

This horizon makes the local toolkit easier for an operator to run, diagnose, navigate, and recover.

## Milestone / Step Tree

### OEH1 — Operator Command Inventory

- [x] OEH1.1 — Inventory operator-facing commands.
- [x] OEH1.2 — Group commands by operator goal.
- [x] OEH1.3 — Write OEH1 report.

### OEH2 — Run Doctor And Environment Checks

- [x] OEH2.1 — Define local environment checks.
- [x] OEH2.2 — Implement run doctor.
- [x] OEH2.3 — Add tests/report.

### OEH3 — Report Manifest And Navigation Surface

- [ ] OEH3.1 — Define report order/manifest.
- [ ] OEH3.2 — Implement manifest generator.
- [ ] OEH3.3 — Add tests/report.

### OEH4 — Error Recovery Playbook

- [ ] OEH4.1 — Define common failure cases.
- [ ] OEH4.2 — Link failures to remediation commands.
- [ ] OEH4.3 — Add tests/report.

### OEH5 — Operator Experience Close Gate

- [ ] OEH5.1 — Implement close gate.
- [ ] OEH5.2 — Run carried regressions.
- [ ] OEH5.3 — Close horizon.

## Decision Log

- This is local operator hardening, not SaaS packaging.
- No protected data appears in diagnostics or manifests.
