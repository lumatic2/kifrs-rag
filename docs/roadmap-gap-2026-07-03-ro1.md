# Roadmap Gap Review

Date: 2026-07-03

## North Star
목표: 잔여 miss 9건(hybrid K=20 기준)을 얕은 랭킹/깊은 랭킹으로 진단하고 recall을 재측정한다. 상세 계획: `docs/horizons/rag-optimization-resume.md` **상태**: RGA1 완료 후 2026-07-03 논의로 재개(2026-07-03 세션 초반 park됐던 후보). 재측정 결과 baseline drift 없음(hybrid recall@20=0.907 그대로), K=100까지 넓히면 9건 중 2건(Q004/Q041) 회복 — 얕은 랭킹/깊은 랭킹(7건) 분리 확인. **세부 계획**: `docs/plans/2026-07-03-ro1-residual-miss-diagnosis.md` ### Active Milestones

## Current State
- RO1: RO1 (evidence: docs/reports/2026-07-03-ro1-deep-miss-diagnosis.md;docs/horizons/rag-optimization-resume.md)

## Gap
- Active harness milestones are exhausted.
- Compare the north star above with current evidence before starting new implementation.
- Do not infer completion without a new DoD and evidence path.

## Proposed Next Horizon
- N1 - define the next measurable gap.
- N2 - create one evidence-producing milestone.
- N3 - add the smallest validation or smoke gate.

## Recommendation
Promote one proposed item to ROADMAP.md only after the user approves the next horizon.
