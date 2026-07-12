# Changeset: PV2-S3 — eval 대시보드 + 파이프라인 스토리

## Target

- ROADMAP milestone: PV2 — Astro 사이트 구현 (`portfolio-viz-site` horizon)
- Plan: `docs/plans/2026-07-12-portfolio-viz-site.md` PV2-S3

## Scope

- Files: `web/src/components/EvalDash.astro`, `web/src/components/Pipeline.astro`,
  `web/src/pages/index.astro` (섹션 Ⅲ·Ⅳ 연결)
- Reason: 품질 증거(지표)와 시스템 서사(파이프라인)가 포트폴리오의 설득 축.
- Expected effect: 스탯 타일 4개(recall@20 0.910·MRR·기출 86%·goldset 50) + retriever 비교
  막대(빌드타임 SVG, 측정일 병기) + 6단계 파이프라인 카드(실 시퀀스라 번호 정당).

## Contract

- Source of truth: `web/src/components/`. 지표는 eval_history.json(aggregate)에서 빌드타임 파생.
- Compatibility: dataviz 스킬 규율 — 팔레트 validator PASS(#0e8a62 계열), 단일 축, 직접 라벨,
  단일 시리즈 막대(범례 불요), 측정일 상이 주석 명기(corpus 개편 전후 혼재의 정직한 공개).
- Out of scope: 배포(PV3).

## Verification

- [x] Targeted tests: 팔레트 validator PASS (lightness·chroma·CVD·contrast)
- [x] CLI smoke: `npm run build` 성공
- [x] Integrated smoke: /browse 전체 페이지 — 4뷰(서가·그래프·대시보드·파이프라인) E2E 렌더,
      파이프라인 그리드 빈 셀 수정(3열×2행)
- [x] Dirty-tree review: web/ 3파일 + changeset 만

## Result

- Status: completed (2026-07-12)
- Evidence: 스크린샷 pv2-s3-full.png (로컬), validator 실행 로그
- Notes: eval 이력이 시계열로 쓰기엔 희소(6/27 집중)·corpus 개편 혼재 → 시계열 대신
  retriever별 최신 측정 막대 + 측정일 병기로 정직하게 표시.