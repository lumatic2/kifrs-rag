# Changeset: PV2-S1 — Astro scaffold + 디자인 토큰 + 기준서 지도(서가) 뷰

## Target

- ROADMAP milestone: PV2 — Astro 사이트 구현 (`portfolio-viz-site` horizon)
- Plan: `docs/plans/2026-07-12-portfolio-viz-site.md` PV2-S1

## Scope

- Files: `web/` Astro 프로젝트(package.json, astro.config.mjs, src/layouts, src/styles/tokens.css,
  src/pages/index.astro, src/components/Bookshelf.astro)
- Reason: 데이터만으론 포트폴리오가 아님 — 보여주는 표면의 뼈대(레이아웃·토큰)와 첫 뷰(지도).
- Expected effect: `npm run build` 가능한 정적 사이트 + 히어로 서가(100 기준서 문단수 비례) +
  기준서 지도 섹션.

## Contract

- Source of truth: `web/`. 데이터는 `web/src/data/*.json`(gate 통과본)만 import — DB 직접 접근 금지.
- Compatibility: Astro 정적 output(assets-only 배포 전제). 디자인 토큰은 `tokens.css` 한 곳.
- Out of scope: 참조 그래프(PV2-S2), 대시보드·스토리(PV2-S3), 배포(PV3).

## Verification

- [x] Targeted tests: `npm run build` 성공 — 1 page, 정적 dist/
- [x] CLI smoke: preview 서버 기동 (localhost:4321)
- [x] Integrated smoke: Playwright 실브라우저 — 히어로 서가(100책등, 카테고리 색) 렌더 + 1116 책등
      클릭→서지 카드(문단 568·본문/부록/BC 구성 바) + 모바일 390px 랩핑 확인(nav nowrap 수정) +
      favicon 404 해소(inline SVG)
- [x] Dirty-tree review: web/(node_modules·dist gitignore 추가) + changeset 만

## Result

- Status: completed (2026-07-12)
- Evidence: 스크린샷 pv2-s1-full/card/mobile.png (로컬), 위 실행 로그
- Notes: 디자인 시그니처 = 서가 히어로(책등 폭 ∝ √문단수). 토큰 = 한지 화이트/청록먹/인주.
  섹션 Ⅱ~Ⅳ는 placeholder — PV2-S2/S3 에서 채움.
