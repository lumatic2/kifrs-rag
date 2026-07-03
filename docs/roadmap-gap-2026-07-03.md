# Roadmap Gap Review

Date: 2026-07-03

## North Star
목표: Phase 4 dogfood에서 확인한 세 축(자동 채점, 외부 권위 인덱스, user_note 운영 품질)을 구현해 RAG 답변 품질을 반복 운영 가능한 로컬 루프로 만든다. 상세 계획: `docs/horizons/engine-quality-ops.md` **상태**: P4C1~P4C5 콘텐츠 dogfood 완료 후 EQ1/EQ2/EQ3/EQ4/EQ5 품질 운영 루프 완료. **상위 계획/성공기준**: `docs/plans/2026-06-30-kifrs-direction-success-criteria.md` **세부 계획**: `docs/plans/2026-06-30-engine-quality-ops.md` ### Active Milestones

## Current State
- EQ1: EQ1 (evidence: changesets/20260630-user-note-quality/README.md; changesets/20260630-auto-grading/README.md; changesets/20260630-authority-index/README.md; scripts/engine_quality_smoke.py)
- EQ2: EQ2 (evidence: changesets/20260630-auto-grading-expanded/README.md; changesets/20260630-authority-source-pack/README.md; changesets/20260630-user-note-schema-v2/README.md; scripts/engine_quality_expanded_smoke.py)
- EQ4: EQ4 (evidence: changesets/20260630-user-note-v2-runtime/README.md)
- EQ3: EQ3 (evidence: changesets/20260630-authority-source-pack-rules/README.md)
- EQ5: EQ5 (evidence: changesets/20260630-quality-preflight-ci/README.md)
- P4C1: P4C1 (evidence: data/dogfood/cpa2/q/q07.md; data/eval/manual/q07_1115_revenue_trace.md; data/scenarios/1115_revenue/WORKFLOW.md)
- P4C2: P4C2 (evidence: data/scenarios/1116_lease/WORKFLOW.md)
- P4C3: P4C3 (evidence: data/user_notes/2026-06-30-p4c3-seed-preview.md; scripts/seed_user_notes.py; kifrs/store.py)
- P4C4: P4C4 (evidence: docs/plans/2026-06-30-p4c4-fair-value-entry.md; data/scenarios/1113_fair_value/WORKFLOW.md)
- P4C5: P4C5 (evidence: docs/plans/2026-06-30-p4c5-employee-benefits-entry.md; data/scenarios/1019_employee_benefits/WORKFLOW.md; kifrs/store.py; kifrs/mcp_server.py)

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
