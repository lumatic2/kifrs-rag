# Roadmap Gap Review

Date: 2026-07-12

## North Star
목표: KASB 제·개정 공표와 로컬 DB 사이 drift 감지(MCP tool `check_drift` + `kifrs/drift.py` 코어) + 감지된 기준서 단위 갱신 경로(재다운로드→재인제스트→amendment 기록). 자체 발제 — 사용자 승인 예외(2026-07-12). (상세 plan → `docs/horizons/kasb-drift-watch.md`, step 트리 → `docs/plans/2026-07-12-kasb-drift-watch.md`)

## Current State
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
