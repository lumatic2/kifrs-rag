# Roadmap Gap Review

Date: 2026-07-12

## North Star
목표: drift 감지의 무인화 — Windows 작업 스케줄러 주 1회 감지 + MCP 응답에 pending drift 자동 경고 (갱신은 수동 유지). 사용자 발제 예외 2건째(2026-07-12). (상세 → `docs/horizons/drift-watch-automation.md`, step 트리 → `docs/plans/2026-07-12-drift-watch-automation.md`)

## Current State
- DR3: DR3 — 주간 감지 + 세션 자동 경고 (evidence: changesets/20260712-dr3-scheduled-drift-check/README.md; changesets/20260712-dr3-mcp-drift-warning/README.md)
- DR1: DR1 — Drift 감지 코어 + MCP tool (evidence: changesets/20260712-dr1-drift-detection-core/README.md; changesets/20260712-dr1-check-drift-mcp-tool/README.md)
- DR2: DR2 — 단위 갱신 경로 + 개정 이력 (evidence: changesets/20260712-dr2-unit-update-path/README.md; changesets/20260712-dr2-report-update-link/README.md)

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
