# Horizon: Operator Experience Hardening

> Status: active
> Created: 2026-07-05
> Previous: `docs/horizons/runtime-retriever-promotion-gate.md`

## Goal

Turn the CLI/report collection into a smoother local operator experience with command discovery, run diagnostics, report manifests, and error recovery.

## Milestones

### OEH1. Operator Command Inventory

Status: completed

- Deliverable: `docs/reports/2026-07-05-oeh1-operator-command-inventory.md`
- Acceptance: demo, readiness, quality, parser, source, and workflow commands are indexed by operator goal.

### OEH2. Run Doctor And Environment Checks

Status: completed

- Deliverable: run doctor script, tests, `docs/reports/2026-07-05-oeh2-run-doctor.md`
- Acceptance: Python, uv, local data expectations, protected boundaries, and missing report hints are checked.

### OEH3. Report Manifest And Navigation Surface

Status: completed

- Deliverable: manifest script/report, tests, `docs/reports/2026-07-05-oeh3-report-manifest.md`
- Acceptance: operator can open the right reports in sequence without reading ROADMAP internals.

### OEH4. Error Recovery Playbook

Status: completed

- Deliverable: recovery playbook/checker, tests, `docs/reports/2026-07-05-oeh4-error-recovery-playbook.md`
- Acceptance: common failures point to specific rerun/remediation commands.

### OEH5. Operator Experience Close Gate

Status: active

- Deliverable: close gate script, tests, `docs/reports/2026-07-05-operator-experience-hardening-close-report.md`
- Acceptance: local operator can discover, run, verify, and recover the demo path through one documented surface.

## Decision Log

- This horizon improves local operator ergonomics, not public SaaS packaging.
- No protected data is exposed in manifests or diagnostics.
