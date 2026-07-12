# Changeset: DR3-S2 — MCP 응답 pending drift 자동 경고

## Target

- ROADMAP milestone: DR3 — 주간 감지 + 세션 자동 경고 (`drift-watch-automation` horizon)
- Plan: `docs/plans/2026-07-12-drift-watch-automation.md` DR3-S2

## Scope

- Files: `kifrs/mcp_server.py` (`_pending_drifts` mtime 캐시 + `_annotate_drift` — search 전 모드·
  get_paragraph 에 적용), `~/projects/custom-skills/accounting/SKILL.md` (drift_warning 안내)
- Reason: 주간 감지가 남긴 pending 상태를 세션 안에서 자동 표면화 — 물어보지 않아도 stale 기준서
  인용 시 경고.
- Expected effect: pending drift 기준서의 검색 히트/문단 조회에 `drift_warning` 필드 자동 포함.

## Contract

- Source of truth: `kifrs/mcp_server.py`, 스킬은 custom-skills (setup.sh 배포).
- Compatibility: 필드 추가만(경고 없으면 응답 불변). 로컬 파일 stat/read 만 — 네트워크·모델 로드 없음,
  mtime 캐시로 호출당 stat 1회.
- Out of scope: 자동 갱신(사용자 결정 제외), reload/기타 tool 경고.

## Verification

- [x] Targeted tests: in-memory MCP — 빈 PENDING 미발화 / synthetic PENDING(1116) 발화(mtime 캐시
      갱신 포함) / get_paragraph 발화 / 비대상 기준서(1115) 무경고. 실 PENDING 원복 확인
- [x] CLI smoke: focused pytest(test_eval_gates, test_user_notes) 5 passed — 기존 경로 비퇴행
- [x] Sync/deploy: setup.sh → 배포본 grep `drift_warning` 1 hit
- [x] Dirty-tree review: 커밋 대상 = mcp_server.py + changeset + plan/ROADMAP sync (data/ 는 로컬)

## Result

- Status: completed (2026-07-12)
- Evidence: 위 checklist 실행 로그
- Notes: 현 세션 kifrs MCP 서버는 구버전 — 경고 필드는 서버 재접속 후 세션에 반영.
