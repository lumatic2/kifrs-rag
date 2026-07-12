# Changeset: DR2-S2 — drift 리포트↔갱신 경로 연결 + horizon close 검증

## Target

- ROADMAP milestone: DR2 — 단위 갱신 경로 + 개정 이력 (`kasb-drift-watch` horizon)
- Plan: `docs/plans/2026-07-12-kasb-drift-watch.md` DR2-S2

## Scope

- Files: `kifrs/drift.py` (drift 항목에 `update_cmd` 필드 + CLI 갱신 안내 출력)
- Reason: 감지 리포트를 본 사람(또는 check_drift 를 부른 Claude)이 다음 행동을 바로 알 수 있어야
  감지→갱신 루프가 닫힘.
- Expected effect: 리포트 JSON·CLI 출력·MCP check_drift 응답의 각 drift 항목에 갱신 커맨드 포함.

## Contract

- Source of truth: `kifrs/drift.py`. check_drift 는 report["drifts"] 를 그대로 반환하므로 자동 반영.
- Compatibility: 필드 추가만 — 기존 소비자 없음.
- Out of scope: 잔여 drift 일괄 갱신(운영 판단), 스케줄.

## Verification

- [x] Targeted tests: compare() synthetic drift 에 `update_cmd` 포함 확인 PASS
- [x] CLI smoke: 감지→갱신 통주 — check(2101 filename_changed + 갱신 커맨드 출력) → `--update 2101`
      (46 문단, amendment 2건) → check 재실행 drift 해소
- [x] Integrated smoke: quality_preflight 체크 4/4 ok(local_rag_threshold_gate 0.921·authority·user_note)
      + focused pytest 18 passed (pytest 는 시스템 python — .venv 는 eval extra 미설치, 기존 환경 특성)
- [x] Dirty-tree review: 커밋 대상 = drift.py + changeset 문서만. data/ 변경(DB·PDF·리포트)은 로컬 자산

## Result

- Status: completed (2026-07-12)
- Evidence: 위 checklist 실행 로그, `data/drift/report-20260712-154622.json` (2101 해소, 로컬)
- Notes: 잔여 실 drift 13건(1001/1101/1103/1109/1110/1116/1012/1034/1036/1037/1039/1041/2106)은
  운영 후속 — 각 `--update <id>` 1분 내외. horizon close 후 사용자 판단.
