# IB1 — 리픽싱 계열 검색 수리 (H4 issue-back)

> Date: 2026-07-12
> Milestone: IB1 (`docs/horizons/h4-issue-back-repair.md`)
> Input: ai-accounting-firm H4 RCPS 실험 mcp-log #5/#7/#11 (`BACKLOG.md` Issue-back Queue #1)
> Public-safe: 문단 번호·순위·점수만 기록, 기준서 원문 인용 없음.

## 결함 요약

실무 용어 "리픽싱(전환가액 조정)"의 실체 규정은 1032가 아니라 **1001-한138.5**(본문)와
1001 BC(`1#4` 통짜 문단 내 한BC104.1)에 있다. H4 실소비에서:

- mcp-log #7: `search("전환가액 조정 리픽셔닝 희석 방지 조항", hybrid, standard=1032)` → 사실상 실패
  (① standard 필터가 1001을 차단 ② "리픽셔닝" 표기 변형 ③ 본문 어휘는 "행사가격이 조정되는 조건")
- mcp-log #5: "고정 대 고정"은 1032 본문 부재 — 기준서 표현은 "확정 수량"·"확정 금액"(1032-16)
- 우회 성공 경로는 `search("리픽싱", lexical, 필터 없음)`뿐이었음

## 수리 내용 (changeset 2건)

1. **`20260712-ib1-repricing-term-bridge`** — term_bridge user_note seed 3건
   (`scripts/seed_user_notes.py`, user_note_v2 20→23 rows):
   - `리픽싱` → 행사가격이 조정되는 조건; 주가 변동; 전환권; 신주인수권; … (anchor 1001-한138.5)
   - `리픽셔닝` → 리픽싱; 행사가격이 조정되는 조건; … (표기 변형 브리지)
   - `고정 대 고정` → 확정 수량; 확정 금액; 자기지분상품; 교환 (anchor 1032-16)
   `expand_query()`가 lexical(FTS)·semantic(qvec)·hybrid·reranked 후보 생성 전부에 적용됨.
2. **`20260712-ib1-standard-filter-guidance`** — standard 필터 함정 안내 2표면:
   `kifrs/mcp_server.py` search docstring + `/accounting` SKILL.md §2 (custom-skills 커밋 + setup.sh 배포).

## BC 임베딩 진단 (계획 항목 ③)

- 1001 BC 계열(`#` suffix 문단) 전부 embedding 존재 — "임베딩 부재"는 아님.
- 단 `1#2`=32,357자, `1#4`=5,576자 통짜 문단에 vector 1개 → 의미 희석으로 semantic 매칭 구조적 약함.
- 한BC 문단은 개별 row로 존재하지 않음 → 근본 수리는 IB2(BC 세분화 재파싱).

## 수리 후 재현 (기본 경로, 필터 없음 — DoD 검증)

| 쿼리 (mcp-log 원문) | mode | 수리 전 | 수리 후 |
|---|---|---|---|
| 전환가액 조정 리픽싱 희석 방지 조항 | hybrid | 한138.5 top-10 밖 | **한138.5 rank 1** |
| 전환가액 조정 리픽싱 희석 방지 조항 | reranked | (1#4 rank 1, 한138.5 없음) | **1001-1#4 rank 1 (0.70)** — 한138.5 계열 도달, 개별 문단화는 IB2 |
| 전환가액 조정 리픽셔닝 희석 방지 조항 (#7) | hybrid | 사실상 실패 | **한138.5 rank 1** |
| 고정 대 고정 확정수량 보통주 전환 지분상품 조건 (#5) | hybrid | 부분 유효 | **1032-16 rank 2** |
| 전환가액이 시가 변동에 따라 조정되는… (#11) | hybrid/reranked | 상위권 없음(로그 시점) | 한138.5 rank 3 / rank 2 (seed 전에도 도달 — 로그 이후 개선 반영 추정) |

비퇴행: `quality_preflight.py` ok (focused_pytest·local_rag_threshold_gate·authority·user_note audit 전부 통과),
`pytest -k "mcp or search"` 16 passed, seed idempotent 재실행 new rows 0.

## 남은 것

- reranked에서 한138.5가 top-5 밖(1#4 BC blob이 대신 top-1) — IB2 BC 세분화 후 재측정(IB3).
- 낮은 신뢰도 자동 감지·자동 필터 해제는 범위 밖(안내 우선) — 재발 시 재판단.
