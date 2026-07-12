# Changeset: PP1-S1 — imagegen visual assets

## Target

- ROADMAP milestone: PP1 — 비주얼 보강 (imagegen)
- Plan: `docs/plans/2026-07-12-portfolio-viz-polish.md` PP1-S1

## Scope

- Files: `web/public/images/hero-archive.jpg`, `texture-hanji.jpg`,
  `still-ledger.jpg`, `still-seal.jpg`, `still-inkdrift.jpg`,
  `still-thread.jpg`
- Reason: 사이트의 한지·서가·인주·원장청록 정물 컨셉을 위한 이미지 생성
- Expected effect: PP1-S2에서 히어로·섹션 반입에 사용할 JPEG 자산 6장 제공

## Contract

- Source of truth: `docs/imagegen-manifest.md` BASE STYLE + 슬롯별 subject prompt
- Compatibility: 모든 자산 JPEG, 1536×1024, 가로 3:2
- Out of scope: 코드·스타일·사이트 구조 수정, 이미지 반입·브라우저 E2E(PP1-S2)

## Verification

- [x] Targeted check: manifest의 6개 filename 모두 생성·저장
- [x] Image check: 6/6 JPEG, 1536×1024, RGB
- [x] Visual check: 한지·서가·원장·인주·먹 확산·제본 톤, 무로고·비판독 처리 확인
- [x] Dirty-tree review: 요청된 이미지 6개와 이 changeset 기록만 추가

## Result

- Status: completed (2026-07-12)
- Evidence: `web/public/images/` — 6 files; all format/size checks passed
- Notes: built-in `image_gen` 사용. PP1 milestone은 PP1-S2가 남아 active 유지.
