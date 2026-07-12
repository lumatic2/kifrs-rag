# Changeset: PV3-S1 — Cloudflare 배포 + 공개 검증

## Target

- ROADMAP milestone: PV3 — 배포 + 공개 검증 (`portfolio-viz-site` horizon)
- Plan: `docs/plans/2026-07-12-portfolio-viz-site.md` PV3-S1

## Scope

- Files: `web/wrangler.toml` (신규). 시스템 상태: Cloudflare Worker `kifrs-viz` +
  `kifrs.askewly.com` custom domain.
- Reason: 로컬 빌드는 포트폴리오 증거가 아님 — 공개 URL 이 최종 산출물.
- Expected effect: wrangler assets-only 배포로 정적 사이트 라이브.

## Contract

- Source of truth: `web/wrangler.toml` (재배포 = `cd web && npx wrangler deploy`).
- Compatibility: assets-only — Worker 코드 없음. 배포 전 `npm run build` + 배포 산출물(dist)
  대상 본문 비포함 스캔 필수.
- Out of scope: analytics, 도메인 외 배포처.

## Verification

- [x] Targeted tests: dist/ 전체 파일 대상 문단 스니펫 17,244건 전수 스캔 — 포함 0건 PASS
- [x] CLI smoke: `npx wrangler deploy` 성공 — 초기 TOML 함정(top-level routes 가 [assets] 뒤에
      있으면 무시됨) 수정 후 custom domain trigger 등록
- [x] Integrated smoke: https://kifrs.askewly.com 200 + workers.dev 라이브 4뷰 실브라우저 렌더
- [x] Dirty-tree review: wrangler.toml + changeset 만

## Result

- Status: completed (2026-07-12)
- Evidence: https://kifrs.askewly.com (라이브), 스크린샷 pv3-live.png (로컬)
- Notes: 재배포 = `cd web && npm run build && npx wrangler deploy`. 데이터 갱신 시
  export_web_data.py + build_cross_references.py → gate → build → deploy 순.
