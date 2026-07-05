# Plan: Product Trust And Quality Evidence

> Objective: `docs/OBJECTIVE.md`
> Horizon: `docs/horizons/product-trust-and-quality-evidence.md`
> Previous gate: `docs/reports/2026-07-05-firm-facing-product-surface-close-report.md`

## Summary

The demo can now be run. This horizon makes it trustable by tying quality gates, confidence labels, failure boundaries, and retriever-promotion decisions into product-facing evidence.

## Milestone / Step Tree

### PTQ1 — Trust Evidence Inventory

- [x] PTQ1.1 — Inventory quality/RAG/default/runtime/review-pack evidence. `(verify: python -m pytest tests\test_product_trust_evidence_inventory.py -q)`
- [x] PTQ1.2 — Classify evidence by fast/heavy/private/public-safe.
- [x] PTQ1.3 — Write PTQ1 report.

### PTQ2 — Review Pack Confidence Contract

- [ ] PTQ2.1 — Define confidence label schema.
- [ ] PTQ2.2 — Map review-pack signals to ready/caution/human-review-required.
- [ ] PTQ2.3 — Add focused tests and report.

### PTQ3 — Failure Boundary Matrix

- [ ] PTQ3.1 — Define failure categories and operator actions.
- [ ] PTQ3.2 — Link each failure to verification/remediation commands.
- [ ] PTQ3.3 — Add focused tests and report.

### PTQ4 — Promotion Decision Evidence Pack

- [ ] PTQ4.1 — Summarize RAG final gate and default guard evidence.
- [ ] PTQ4.2 — Connect promotion decision to failure matrix.
- [ ] PTQ4.3 — Add report and tests without changing runtime default.

### PTQ5 — Trust And Quality Close Gate

- [ ] PTQ5.1 — Implement trust quality gate.
- [ ] PTQ5.2 — Run carried regressions.
- [ ] PTQ5.3 — Close horizon.

## Decision Log

- No unresolved user decision.
- Default retriever promotion remains deferred unless a later explicit authorization changes it.

## Stop Conditions

- Stop if a change would expose protected K-IFRS text, dogfood material, private client data, or credentials.
- Stop if a confidence label implies final accounting judgment rather than decision-support evidence.
