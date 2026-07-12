# Roadmap Gap Review

Date: 2026-07-12

## North Star
목표: 메타데이터 전용 포트폴리오 시각화 사이트 — 기준서 지도·참조 그래프·eval 대시보드·아키텍처 스토리 4뷰, Astro + Cloudflare(`kifrs.askewly.com`). 본문 비노출 public-safe gate 필수. 사용자 발제 예외 3건째(2026-07-12). (상세 → `docs/horizons/portfolio-viz-site.md`, step 트리 → `docs/plans/2026-07-12-portfolio-viz-site.md`)

## Current State
- PV1: PV1 — 데이터 레이어 (export + 참조 추출) (evidence: changesets/20260712-pv1-web-data-export/README.md; changesets/20260712-pv1-crossref-extraction/README.md)
- PV2: PV2 — Astro 사이트 구현 (4뷰) (evidence: changesets/20260712-pv2-astro-scaffold-map/README.md; changesets/20260712-pv2-refgraph-island/README.md; changesets/20260712-pv2-evaldash-pipeline/README.md)
- PV3: PV3 — 배포 + 공개 검증 (evidence: changesets/20260712-pv3-deploy/README.md; https://kifrs.askewly.com)
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
