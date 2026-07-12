# Changeset: PV1-S1 — 웹 메타데이터 export + public-safe gate

## Target

- ROADMAP milestone: PV1 — 데이터 레이어 (`portfolio-viz-site` horizon)
- Plan: `docs/plans/2026-07-12-portfolio-viz-site.md` PV1-S1

## Scope

- Files: `scripts/export_web_data.py`, `scripts/check_web_data_safety.py`, `web/src/data/*.json`(산출물)
- Reason: 사이트에 넣을 메타데이터가 없고, 저작권 경계(본문 비노출)를 자동 검증할 gate 도 없음.
- Expected effect: DB→JSON export(기준서 계층·규모, eval 이력 aggregate, 파이프라인 통계) +
  gate 가 본문 유출을 기계적으로 차단.

## Contract

- Source of truth: 이 레포 scripts/. 기준서 제목은 `data/drift/snapshot.json`(KASB 목록 메타)에서 매핑.
- Compatibility: DB 읽기 전용. export 산출물(web/src/data/)은 **메타데이터만 — 커밋 대상**
  (gate PASS 가 커밋 전제). eval 이력은 aggregate 만(goldset 쿼리·gold 문단 포함 금지).
- Out of scope: cross_reference 추출(PV1-S2), 사이트 구현(PV2).

## Verification

- [x] Targeted tests: export → standards.json 100건(title 누락 0) + eval_history 11건 + pipeline.json
- [x] CLI smoke: gate PASS — 전수 17,244 문단 스니펫 비포함 + 길이 상한, 0.2s
- [x] Failure mode: 실 문단(1116-26, 141자 — 길이 상한 우회 케이스) 주입 시 gate FAIL(exit 1) → 원복 PASS.
      **초기 표본(500건) 방식이 이 주입을 놓쳐 전수 대조로 강화** — gate 의 gate 역할 실증
- [x] Dirty-tree review: scripts 2 + web/src/data 3 JSON + changeset 만

## Result

- Status: completed (2026-07-12)
- Evidence: 위 checklist 실행 로그
- Notes: 검사 2중 = 길이 상한 200자 + 전체 문단(≥30자) 선두 30자 스니펫 전수 대조.
  eval_history 는 aggregate 만 (goldset 쿼리·gold 문단 제외 — 기출 저작권).
