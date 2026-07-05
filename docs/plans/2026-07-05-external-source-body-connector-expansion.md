# Plan: External Source Body Connector Expansion

> Objective: `docs/OBJECTIVE.md`
> Horizon: `docs/horizons/external-source-body-connector-expansion.md`

## Summary

This horizon addresses the Objective gap that external source connector evidence is still mostly metadata/demo-oriented. It expands toward source-body handling while keeping authorization, source policy, and public-safe reporting as hard gates.

## Milestone / Step Tree

### ESB1 — Source-Body Connector Selection And Policy Gate

- [x] ESB1.1 — Select first source-body class.
- [x] ESB1.2 — Define authorization and public-report policy.
- [x] ESB1.3 — Write ESB1 selection/policy report.

### ESB2 — Synthetic Source-Body Fixture Contract

- [x] ESB2.1 — Define body fixture schema.
- [x] ESB2.2 — Define parser/chunker output schema.
- [x] ESB2.3 — Write fixture contract report.

### ESB3 — Chunking And Retrieval Dry Run

- [x] ESB3.1 — Define synthetic chunks.
- [x] ESB3.2 — Simulate retrieval result metadata.
- [x] ESB3.3 — Write dry-run report.

### ESB4 — Connector Leak And Policy Gate

- [ ] ESB4.1 — Define protected body leak checks.
- [ ] ESB4.2 — Add synthetic negative cases.
- [ ] ESB4.3 — Write leak/policy gate report.

### ESB5 — Horizon Close And Workflow Coverage Handoff

- [ ] ESB5.1 — Combine ESB1~ESB4 evidence.
- [ ] ESB5.2 — Close horizon and name next objective-gap horizon.
- [ ] ESB5.3 — Sync ROADMAP/OBJECTIVE/progress map.

## Decision Log

- Start with authorization and policy, not live scraping.
- Do not include protected source body text in public reports.
- Packaging and external accountant feedback remain excluded.
