# Roadmap Gap Review

Date: 2026-07-03

## North Star
목표: `kifrs/workflows/kifrs1109/` 결정 엔진의 하드코딩 인용을 런타임 `kifrs.store`/`kifrs.embed` 직접 호출로 grounding 검증한다. 상세 계획: `docs/horizons/rag-agent-integration.md` **상태**: WA1(1109 파일럿 엔진) 완료 후, 2026-07-03 논의로 두 horizon 후보(RAG 최적화 재개 / RAG 엔진↔에이전트 통합) 중 후자를 우선 채택. grounding 시점=런타임, 호출경로=직접 import, 불일치처리=NeedsHumanReview 3개 결정 확정. **세부 계획**: `docs/plans/2026-07-03-rga1-runtime-citation-grounding.md` ### Active Milestones

## Current State
- RGA1: RGA1 (evidence: kifrs/workflows/kifrs1109/grounding.py;tests/test_workflow_1109_grounding.py;docs/reports/2026-07-03-wa1-completion-rate.md)

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
