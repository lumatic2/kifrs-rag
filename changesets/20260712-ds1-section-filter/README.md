# Changeset: DS1 — search() section/exclude_bc 후보 필터

## Target

- ROADMAP milestone: DS1 — search `section` 필터 (`h10-disclosure-search-repair` horizon)
- Plan: `docs/plans/2026-07-12-h10-disclosure-search-repair.md` DS1-S1 + DS1-S2

## Scope

- Files: `kifrs/mcp_server.py`, `tests/test_store_search.py`
- Reason: issue-back #4 (H10 C8-2 공시 체크리스트) — "공시 절만" 조회에서 공시 절 문단이
  BC·측정 절에 밀려 회수율이 구조적으로 낮음 (1016은 공시 8문단 중 5개가 top-20 밖).
- Expected effect: `search(section=..., exclude_bc=...)` 로 후보 필터링 — 랭킹 알고리즘
  불변, 오버샘플(fetch_limit = limit×5, 100~500) 후 필터 통과분만 반환.

## Contract

- **계획 대비 편차**: plan 은 store/embed 검색 함수에 파라미터 관통을 명시했으나,
  구현은 MCP 레이어 후처리 필터(`_apply_candidate_filter`) + 오버샘플로 단순화 —
  5개 모드 전부 한 곳에서 커버, store/embed 시그니처·eval 경로 완전 불변(비퇴행이
  구조적으로 보장). horizon acceptance(재현 개선 + 비퇴행 + 미존재 section 빈 결과)는
  전부 충족하므로 편차 승인 사유로 기록.
- 필터 통과분이 limit 미만이면 정직하게 적게 반환(필터 전 결과로 채우지 않음),
  히트에 `filter_applied` 필드 표시. 미지정 시 기존 동작과 바이트 단위 동일.
- Out of scope: `_BC_DEMOTE` 변경(IB2 캘리브레이션 보존), paragraph_type 파생 분류.

## Verification

- [x] Targeted tests: `python -m pytest tests/test_store_search.py` 20 passed
      (신규 7건: 부분일치·exclude_bc·정직한 부족 반환·noop 불변·기본값 동일성·live 필터)
- [x] 미존재 section → `[]` (오류 아님) 확인
- [x] mcp-log 재현 4쿼리 (§7/§15/§17/§22) — 공시절 top-20 회수 5→20, 4→14, 3→8, 2→16.
      acceptance 세부(1016 73~79 노출 3→6+)는 3→8 로 초과 달성
- [x] 필터 미사용 hybrid eval 비퇴행: recall@10 0.747 / @20 0.910 / MRR 0.488 —
      baseline 과 정확히 일치 (`data/eval/results/retrieval_20260712_183353.json`)

## Result

- Status: completed (2026-07-12)
- Evidence: 재현 로그(본 README Verification), eval 리포트 JSON
- Notes: 공시 절 전수 수집의 정본 경로는 여전히 `list_sections → get_context`
  (전략 A, 5/5 완전 회수) — search(section=) 는 검색 정밀도 보조. DS2 에서 /accounting 표면화.
