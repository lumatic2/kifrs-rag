# Plan: Firm-Facing Product Surface

> Objective: `docs/OBJECTIVE.md`
> Horizon: `docs/horizons/firm-facing-product-surface.md`
> Previous gate: `docs/reports/2026-07-05-client-private-parser-runtime-close-report.md`

## Summary

The engine now has K-IFRS RAG quality gates, non-IFRS source records, multi-authority runtime separation, and a client-private parser runtime boundary. This horizon turns that proof into a local operator-facing demo surface.

## Milestone / Step Tree

### FPS1 — Product Surface Inventory And Demo Flow

- [x] FPS1.1 — Inventory existing demo/gate/report surfaces.
- [x] FPS1.2 — Select first recommended demo flow.
- [x] FPS1.3 — Classify FPS2~FPS5 gaps.
- [x] FPS1.4 — Write FPS1 report.

### FPS2 — Operator Demo Command

- [ ] FPS2.1 — Define demo packet schema.
- [ ] FPS2.2 — Generate one walkthrough packet with workflow output, authority boundary, private-runtime boundary, and verification status.
- [ ] FPS2.3 — Add focused tests.
- [ ] FPS2.4 — Write FPS2 report.

### FPS3 — Readiness Checklist And Local Install Path

- [ ] FPS3.1 — Define prerequisites and local commands.
- [ ] FPS3.2 — Document protected/private boundary.
- [ ] FPS3.3 — Write readiness checklist report.

### FPS4 — Product Narrative README Surface

- [ ] FPS4.1 — Explain current capabilities plainly.
- [ ] FPS4.2 — Explain limits and non-goals plainly.
- [ ] FPS4.3 — Connect demo command to product objective.

### FPS5 — Firm-Facing Surface Close Gate

- [ ] FPS5.1 — Implement product surface gate.
- [ ] FPS5.2 — Run carried runtime/RAG regressions.
- [ ] FPS5.3 — Close horizon.

## Stop Conditions

- Stop if the surface needs protected K-IFRS source text, embeddings, dogfood material, or real client files.
- Stop if the demo hides known limitations or implies autonomous audit/tax/legal conclusion authority.
