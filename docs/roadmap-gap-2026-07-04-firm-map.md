# Roadmap Gap Review

Date: 2026-07-04

## North Star
`docs/horizons/automation-expansion.md` — close (2026-07-04). AE1(1116 엔진 9/10) + AE2(1116 주석 8/11 자동, DART 3사 대사) 완료. 완료율 축 2-도메인화 + 커버리지 축 3→4/33. AE3(NeedsHumanReview 인터페이스)는 신호 종속으로 이월. Objective 임팩트: 두 축 동시 전진, 차별점 가설 2차 지지. <!-- harness:goal id="practice-map" status="closed" --> `docs/horizons/practice-map.md` — 조건부 close (2026-07-04). PM1(taxonomy 33 task) + PM3(전수 판정 + 추천: 1116 먼저 + 주석 다음) 완료, PM2는 위 Next Candidates로 이월. 상세 marker 이력 → `BACKLOG.md`. <!-- harness:goal id="workflow-automation" status="closed" --> `docs/horizons/workflow-automation.md` — close (2026-07-04). WA1 완료(6/10, `docs/reports/2026-07-03-wa1-completion-rate.md`), WA2→AE1 흡수, WA3→AE3 이관.

## Current State
- AE2: AE2 (evidence: tests/test_1116_disclosure.py;docs/reports/2026-07-04-ae2-disclosure-coverage.md)
- AE1: AE1 (evidence: tests/test_workflow_1116_regression.py;docs/reports/2026-07-04-ae1-completion-rate.md)

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
