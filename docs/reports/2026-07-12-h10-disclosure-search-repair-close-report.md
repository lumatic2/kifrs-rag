# Close Report: h10-disclosure-search-repair

> Date: 2026-07-12
> Horizon: `docs/horizons/h10-disclosure-search-repair.md` (closed)
> Input: BACKLOG Issue-back Queue #4 — H10 C8-2 공시 체크리스트 실험 (5번째 실소비)
> Close Result: `h10_disclosure_search_repaired`

## 무엇을 고쳤나

`search()` 에 `section`(부분일치)·`exclude_bc` 후보 필터 추가 — 랭킹 알고리즘 불변,
오버샘플(limit×5, 100~500) 후 필터 통과분만 정직하게 반환(`filter_applied` 표시,
부족분 backfill 없음). 구현·1차 검증은 워커 changeset #46
(`changesets/20260712-ib4-search-section-filter/`, 커밋 1c0fdf4), 재현·비퇴행 게이트와
표면화는 오케스트레이터(커밋 6a663d7~).

## 증거

- **재현 4쿼리** (mcp-log §7/§15/§17/§22, `section="공시"` 적용): 공시절 top-20 회수
  5→20 / 4→14 / 3→8 / 2→16. acceptance 세부(1016 문단 73~79 노출 3→6+)는 **3→8 전량 노출**.
- **5개 기준서 전수** (changeset #46 표): reranked/hierarchical 둘 다 5/5 기준서 개선
  (예: 1107 2/58→20/58, 1012 9/20→17/20).
- **비퇴행**: 필터 미사용 hybrid eval recall@10 0.747 / @20 0.910 / MRR 0.488 — baseline
  정확 일치 (`data/eval/results/retrieval_20260712_183353.json`). 기본값 미지정 호출은
  바이트 단위 동일(단위 테스트 고정). pytest 20 passed.
- **표면화**: search docstring(공시 절 수집 안내) + /accounting SKILL.md "절 단위 전수
  수집" 항목(정본 = `list_sections→get_context`, 필터 = 보조) 배포본 grep 확인.

## 잔여 한계 (자체 착수 금지 — issue-back 회귀 시만)

- 1115처럼 공시가 "공시"+세부 5개 절로 분산된 기준서는 substring 필터로 전부 못 잡음 —
  정본 경로(`list_sections→get_context`)가 여전히 필요한 구조적 이유. SKILL.md에 명시.
- 필터는 후보 풀(오버샘플 최대 500) 안에서만 작동 — 코퍼스에 조건 문단이 그보다 깊게
  묻히면 회수 불가(현 재현에서는 미관측).

## 크기 회고 (§A1)

- **DS1 인플레 적발**: changeset 1개로 닫힘 = step 크기 (roadmap_sync 자동 적발).
  DS2도 changeset 1개(기록형). **이 horizon 전체가 milestone 1개 크기**였다 — 다음
  issue-back 이 "필터/파라미터 추가 + 표면화" 규모면 horizon 을 milestone 2개로 쪼개지
  말고 milestone 1개(구현+표면화 step 2개)로 잡을 것.

## 운영 노트

- 이번 회전에서 구현 워커와 오케스트레이터가 같은 결함을 이중 작업하는 사고 발생
  (오케스트레이터가 워커 커밋 1c0fdf4 를 인지 못하고 중복 changeset 작성 → 즉시 정리,
  #46 을 정본 채택). 원인: compact 후 재개 시 작업 트리 미커밋 변경을 "내 착수분"으로
  오인. 교훈: **재개 직후 dirty tree 는 git log/diff 로 출처 확인 후 착수**.
- 워커 노트: `uv sync --extra eval` 이 GPU torch 를 CPU 휠로 되돌림 — cu128 재설치로
  복구 (CLAUDE.md 한계 #4 함정의 신규 변종).
