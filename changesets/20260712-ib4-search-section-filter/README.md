# Changeset

## Target

- ROADMAP milestone: (maintenance changeset — issue-back queue #4, 신규 horizon/milestone 아님)
- Plan: BACKLOG.md Issue-back Queue "2026-07-12(b) — H10 C8-2" 결함 #4 수리 — `search()` 가
  공시 절 수집에서 BC·측정 절 문단에 희석되는 문제. 후보 필터링(`section`/`exclude_bc`)으로
  정밀도 개선. 소비자 원 로그:
  `~/projects/ai-accounting-firm/docs/cases/2026-07-12-disc-checklist/mcp-log.md` §전략 비교 종합.

## Scope

- Files: `kifrs/mcp_server.py`(`search` 도구·`_search_impl`·신규 `_apply_candidate_filter`
  헬퍼), `tests/test_store_search.py`(신규 단위/통합 테스트 9건).
- Reason: `search(reranked/hierarchical)`가 "공시" 자연어 쿼리에서도 BC(결론도출근거)·측정
  절 문단에 밀려 공시 절이 회수되지 않음(5개 기준서 전수 재현). 랭킹 알고리즘 자체는 이
  희석을 구조적으로 해결하기 어려움(BC/측정이 동일 어휘를 공유) — 후보 필터링으로 우회.
- Expected effect: `section="공시"`(부분일치) / `exclude_bc=True` 필터로 "공시 절만" 요청하는
  검색의 정밀도 향상. `list_sections→get_context` 정본 경로는 그대로 유지(여전히 100% 회수
  보장 경로), search()는 보조 수단으로 개선.

## Contract

- Source of truth: `docs/cases/2026-07-12-disc-checklist/mcp-log.md`(소비자 원 로그),
  `kifrs/mcp_server.py::search` docstring(공시 절 수집 시 `section="공시"` 권장 + 정본 경로 병기).
- Compatibility: **필터 파라미터 기본값 None/False — 미지정 호출은 완전 불변**(오버샘플 없이
  기존 limit 그대로 하위 검색 함수 호출, `_apply_candidate_filter`는 필터 없으면 원본 그대로
  반환). 기존 테스트(`test_mcp_server_search_lexical_mode_matches_store_search_fts`,
  `test_mcp_server_search_reranked_mode_matches_embed_search_reranked`) 그대로 통과.
- Out of scope: 랭킹 알고리즘(RRF 가중치·BC demote·centroid) 변경 없음. `list_paragraphs`의
  기존 `section` 파라미터(정확일치)는 건드리지 않음 — `search()`의 신규 `section`은 부분일치로
  별도 설계(기준서마다 "질적 공시"/"양적 공시"처럼 세분화된 라벨을 포괄하기 위함).

## Verification

- [x] Targeted tests: `tests/test_store_search.py` 9건 신규(순수 함수 `_apply_candidate_filter`
      단위 테스트 4건 — section substring/exclude_bc/honest-short-result/no-op-불변, DB 통합
      테스트 3건 — 기본 호출 불변·section 필터·exclude_bc 필터) + 기존 18건 회귀 없음. 전체
      `pytest tests/test_store_search.py -q` → **20 passed**.
- [x] CLI smoke: 5개 기준서(1116/1115/1107/1016/1012) `search("공시 요구사항", mode=reranked/
      hierarchical)` vs `search(..., section="공시")` before/after 비교(스크립트:
      스크래치패드 `ib4_smoke.py`, 결과는 아래 Result 표).
- [x] Integrated smoke: `python -m kifrs.eval.retrieval` 재실행 — hybrid recall@20 **0.9100**
      (CLAUDE.md 문서 기준치 0.910과 일치, 필터 미사용 기본 경로 완전 비퇴행 확인).
- [x] Dirty-tree review: `git diff` 확인 — `kifrs/mcp_server.py` + `tests/test_store_search.py`
      만 변경, BACKLOG.md/ROADMAP.md 미변경(오케스트레이터 몫).

## Result

- Status: 완료.
- Evidence: before/after 회수율 표(golden = 각 기준서 `list_sections`에서 section 값에 "공시"
  포함된 모든 문단, limit=20 기준 매칭 개수):

  | 기준서 | golden | reranked before | reranked after | hierarchical before | hierarchical after |
  |---|---|---|---|---|---|
  | 1116 | 44 | 6/44 | 20/44 | 9/44 | 20/44 |
  | 1115 | 21 | 5/21 | 9/21 | 4/21 | 10/21 |
  | 1107 | 58 | 2/58 | 20/58 | 5/58 | 20/58 |
  | 1016 | 21 | 12/21 | 18/21 | 7/21 | 18/21 |
  | 1012 | 20 | 9/20 | 17/20 | 4/20 | 17/20 |

  after 결과는 5/5 기준서 전부 `filter_applied` 필드로 필터 적용 표시 확인. 1115가 다른
  기준서 대비 개선폭이 작은 이유는 원 로그(mcp-log.md §참고 1)에서 이미 지적된 구조적 원인 —
  1115 공시 절이 "공시"(총론) + 5개 세부 섹션명으로 분산되어 있어 단순 substring 필터로는
  전부 포괄되지 않음(정본 경로 `list_sections→get_context`가 여전히 필요한 이유).
- Notes: 필터는 오버샘플(`limit*5`, 최소 100·최대 500) 후 후보 필터링 방식 — 결과 부족 시
  필터 전 결과로 채우지 않고 정직하게 적은 결과 반환(`test_apply_candidate_filter_honest_short_result_not_backfilled`로
  회귀 방지). 구현 중 `uv sync --extra eval`이 GPU torch(`+cu128`)를 CPU 휠로 되돌린 사고 발생
  — `uv pip install --reinstall torch --index-url https://download.pytorch.org/whl/cu128`로
  즉시 복구 확인(`torch.cuda.is_available() == True`). BACKLOG 상태 갱신은 오케스트레이터 몫.
