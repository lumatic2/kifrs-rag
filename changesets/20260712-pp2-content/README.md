# Changeset: PP2-S2 — 콘텐츠 확장 (drift 스토리 + 수리 루프 연대기 + 상호 링크)

## Target

- ROADMAP milestone: PP2 (`portfolio-viz-polish` horizon)
- Plan: `docs/plans/2026-07-12-portfolio-viz-polish.md` PP2-S2

## Scope

- Files: `web/src/components/{DriftLoop,RepairLoop}.astro`(신규), `web/src/pages/index.astro`(Ⅴ·Ⅵ 섹션 + nav)
- Reason: 수리 루프 2회전·drift 무인 감시가 완성됐는데 사이트에 "살아있는 엔진" 서사가 없음.
- Expected effect: #drift(4단계 루프 + 스탯 4타일) + #repair-loop(2회전 타임라인, before/after 지표) + account.askewly.com 외부 링크.

## Contract

- 기준서 본문 무반입 — 하드코딩된 숫자·날짜·지표만(15건 갱신/83+3/134행/recall 0.887→0.910/0.747·0.910·0.488 등). amendment 134는 pipeline.json 참조.
- 기존 디자인 토큰만 사용, 새 색 없음.
- Out of scope: universe/, web/src/data.

## Verification

- [x] Targeted: `npm run build` 통과 + gate PASS(5파일, 본문 표본 17,244건 비포함)
- [x] Integrated smoke: 실브라우저 — Ⅴ·Ⅵ 섹션 렌더, nav 링크, 외부 링크(noopener), 지표 표기 정확성 육안 대조
- [x] Dirty-tree review: Scope 파일만

## Result

- Status: completed (2026-07-12)
- Evidence: drift-section 스크린샷(스크래치패드)
