# Changeset: PP1 — imagegen 비주얼 보강 (한지/서가 정물 6장)

## Target

- ROADMAP milestone: PP1 (`portfolio-viz-polish` horizon)
- Plan: `docs/plans/2026-07-12-portfolio-viz-polish.md` PP1-S1 + PP1-S2

## Scope

- Files: `web/public/images/*.jpg`(6장 신규 — codex imagegen), `web/src/pages/index.astro`(도판 5개 + .plate 스타일), `docs/imagegen-manifest.md`(선행 커밋 c337871)
- Reason: 텍스트-only 사이트에 컨셉 톤(한지·서가·인주) 시각 자산 부재.
- Expected effect: 히어로 도판(장서각) + 섹션 배너 4(원장=품질/실제본=파이프라인/묵 번짐=drift/인장=수리 루프). texture-hanji.jpg 는 예비.

## Contract

- 스타일 = 사이트 디자인 시스템(한지 화이트/청록먹/인주) 정물 계열 — 어스회계법인(기업 실사)과 의도적 차별화.
- 이미지 내 판독 가능한 글자·로고 없음(육안 검수). 기준서 본문과 무관한 생성 이미지 — 저작권 경계 무관.
- 히어로만 eager, 배너 4는 lazy + max-height 캡.

## Verification

- [x] Targeted: codex imagegen 6/6 생성(실패 0) + 대표 2장 육안 검수(글자 판독 불가·컨셉 톤 일치)
- [x] CLI smoke: `npm run build` 통과 + gate PASS(회귀 확인)
- [x] Integrated smoke: 실브라우저 — 도판 5개 전부 naturalSize 1536×1024 로드, 레이아웃 확인
- [x] Dirty-tree review: Scope 파일만
- 운영 노트: 1차 codex exec 이 stdin 대기로 startup hang(세션 파일 미생성, CPU 0.08s) — kill 후 `</dev/null` 로 재실행하여 해결. **background codex exec 는 stdin 을 닫고 실행할 것.**

## Result

- Status: completed (2026-07-12)
- Evidence: kifrs-home-v5 스크린샷(스크래치패드), 이미지 6장
