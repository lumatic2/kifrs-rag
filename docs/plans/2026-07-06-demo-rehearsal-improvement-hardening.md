# Plan: Demo Rehearsal Improvement Hardening

> Objective: `docs/OBJECTIVE.md`
> Horizon: `docs/horizons/demo-rehearsal-improvement-hardening.md`

## Summary

This horizon implements the three internal DRQ4 backlog fixes: retriever timing threshold, freshness metadata, and a compact operator summary. The close gate verifies those fixes without changing default retriever behavior.

## Milestone / Step Tree

### DRI1 — Retriever Timing Threshold

- [x] DRI1.1 — Add retriever-decision timing variance threshold to quality checklist.
- [x] DRI1.2 — Update tests and DRQ2 report.

### DRI2 — Rehearsal Freshness Metadata

- [x] DRI2.1 — Add generated-at and freshness checks to rehearsal evidence capture.
- [x] DRI2.2 — Update tests and DRQ3 report.

### DRI3 — Operator Summary Surface

- [x] DRI3.1 — Add one-screen operator summary to progress map data.
- [x] DRI3.2 — Update tests and progress map report.

### DRI4 — Horizon Close Gate

- [x] DRI4.1 — Verify DRI1~DRI3 evidence.
- [x] DRI4.2 — Write close report and sync ROADMAP/horizon/phase state.

## Decision Log

- 결정 없음. DRQ4 backlog의 내부 개선 3개를 그대로 구현한다.
- 중단점: protected payload, external dependency, or default retriever behavior change appears.
