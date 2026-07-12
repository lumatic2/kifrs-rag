# Changeset: PV2-S2 — 참조 네트워크 그래프 island

## Target

- ROADMAP milestone: PV2 — Astro 사이트 구현 (`portfolio-viz-site` horizon)
- Plan: `docs/plans/2026-07-12-portfolio-viz-site.md` PV2-S2

## Scope

- Files: `web/src/components/RefGraph.astro` (신규), `web/src/pages/index.astro` (섹션 Ⅱ 연결),
  `web/package.json` (+d3-force)
- Reason: 655 기준서 쌍 참조 데이터를 보여줄 표면.
- Expected effect: canvas + d3-force 그래프 — 선 굵기=참조 횟수, 원 크기=받은 참조,
  hover 이웃 강조 + 참조 강도 필터(전체/3+/8+).

## Contract

- Source of truth: `web/src/components/RefGraph.astro`. 데이터는 crossref.json aggregate 만.
- Compatibility: island 스크립트는 클라이언트 번들 — 기존 뷰 영향 없음.
- Out of scope: 대시보드·스토리(PV2-S3).

## Verification

- [x] Targeted tests: `npm run build` 성공 (d3-force 번들 포함)
- [x] CLI smoke: preview 렌더 — 기본 필터(3+) force layout, 1109/1001/1107 허브 관측
- [x] Integrated smoke: 필터 8+ 전환 → 코어 서브그래프 재배치(1109 최대 허브) — 도메인 정합
- [x] Dirty-tree review: web/ 3파일 + changeset 만

## Result

- Status: completed (2026-07-12)
- Evidence: 스크린샷 pv2-s2-graph2/filter8.png (로컬)
- Notes: hover 이웃 강조·툴팁은 canvas 히트테스트(코드 경로 단순) — 라이브 검증은 PV3 에서 병행.
