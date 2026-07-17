# Plan: RGA1 — 런타임 Citation Grounding 레이어

> Objective: `docs/OBJECTIVE.md`
> Horizon: `docs/horizons/rag-agent-integration.md` (`rag-agent-integration`)
> Milestone: RGA1 — 런타임 grounding 레이어 구축
> Created: 2026-07-03

## Scope boundary

`kifrs/workflows/kifrs1109/`의 결정 엔진(`sppi.py`, `business_model.py`, `classify.py`,
`initial_entry.py`, `review_memo.py`)이 `reasons` 문자열에 하드코딩한 조항 인용
(예: `[1109-4.1.2(b)/4.1.2A(b), B4.1.7~7B]`)을 런타임에 `kifrs.store` 직접 import로 검증한다.
검증 = 인용된 조항 ID가 DB에 실제 존재하는지(존재 검증만 — 아래 §Step 3 발견 참조).
존재하지 않으면 `NeedsHumanReview`.

**축소 결정 (구현 중 발견, 2026-07-03)**: 원래 계획은 존재 검증 + 의미적 일치 검증(reason 문구가
인용된 조항의 실제 내용과 부합하는지) 2단계였다. 구현 중 실제 15개 하드코딩 인용으로 keyword
overlap과 bge-m3 cosine 유사도, cross-encoder 리랭커(`bge-reranker-v2-m3`)를 모두 실측했으나
어느 방식도 정답/오답을 신뢰성 있게 구분하지 못했다(정답 유사도 0.41~0.63 vs 오답 0.33~0.51로
크게 겹침; 리랭커도 정답 다수가 0.000~0.008로 오답과 구분 불가). 원인은 `reasons` 문구가 압축된
회계 판단 요약이라 조문 원문 어휘와 거리가 멀기 때문 — `CLAUDE.md` 한계 #1과 동일한 문제. 사용자
결정(2026-07-03): 의미적 일치 검증은 RGA1에서 제외하고 존재 검증만으로 축소, 의미적 일치는 근본
적으로 다른 접근(코드 작성 시점 인용-근거 동시 기록, 또는 사람의 1회성 감사)이 필요해 별도 후속
후보로 이관.

Out of scope (이번 milestone에서 다루지 않음, 이유):
- **MCP 프로토콜 경유 호출** — horizon 결정으로 직접 import만 사용.
- **의미적 일치 검증** — 위 발견으로 RGA1에서 제외. 후속 후보(신규 접근 필요, RGA2/미정)로 이관.
- **인용을 엔진이 스스로 찾아 채우는 기능(자동 인용 생성)** — 이번 범위는 *기존 하드코딩 인용의
  존재 검증*이지, 새 인용의 자동 발견이 아니다. 새 시나리오/규칙 추가 시 인용은 여전히 사람이 채운다.
- **grounding 결과 캐싱/성능 튜닝** — RGA2 후보. 이번엔 정확성만 확보.
- **다른 도메인(1116 등) 포팅** — RGA3/WA2 후보.

## Step tree (leaf test 적용 — 시그니처 수준)

- [x] **Step 1 — 인용 추출 유틸** (`kifrs/workflows/kifrs1109/grounding.py::extract_citations`)
  `reasons` 문자열에서 `[1109-...]` 형태 토큰을 정규식으로 파싱해 조항 ID 리스트로 분해
  (예: `4.1.2(b)`, `B4.1.18~19`). (verify: `tests/test_workflow_1109_grounding.py::test_extract_citations`)

- [x] **Step 2 — 존재 검증** (`grounding.py::verify_citation_exists`)
  `kifrs.store`를 직접 import해 조항 ID로 문단을 조회, 존재 여부 반환. (verify:
  `tests/test_workflow_1109_grounding.py::test_verify_citation_exists_*`)

- [x] **Step 3 — 의미적 일치 확인** — **취소** (구현 중 발견으로 RGA1 범위에서 제외, 위 §Scope
  boundary 참조). keyword overlap·cosine 유사도·리랭커 실측 결과를 근거로 사용자 승인.

- [x] **Step 4 — NeedsHumanReview 배선** (`classify.py` 호출부, 결과 집계 지점 1곳)
  `classify()`가 반환 직전 자신의 reasons + sppi.reasons + business_model.reasons를 모아 Step 1~2
  grounding(존재 검증)을 통과시키고, 실패 시 기존 `NeedsHumanReview` 패턴으로 던진다. (verify:
  `tests/test_workflow_1109_regression.py` 10개 시나리오 그대로 6/10 통과 +
  `tests/test_workflow_1109_grounding.py::test_classify_escalates_to_needs_human_review_on_bad_citation`)

- [x] **Step 5 (integration) — 회귀 갱신 + 완료율 재측정** (`tests/test_workflow_1109_regression.py`,
  `docs/reports/2026-07-03-wa1-completion-rate.md` 갱신)
  grounding 경로 포함해 10개 시나리오 전체 재실행, 완료율 6/10 변화 없음 — RGA1 갱신 섹션에 기록.
  (verify: `python -m pytest tests/ -q` 92/92 전체 통과 + 리포트 파일 갱신 완료)

## 결정 로그

- **grounding 시점: 런타임** — 사용자 결정. Objective의 "K-IFRS 기반" 전제를 실질적으로 지키려면
  빌드 시점 검증만으로는 부족하다고 판단.
- **호출 경로: 직접 import** — 사용자 결정. MCP는 프로세스 경계를 넘는 외부 세션용 레이어이고,
  엔진은 같은 프로세스 내부 코드 — 한계 #6(MCP stdio fragility) 우회.
- **불일치 처리: NeedsHumanReview 에스컬레이션** — 사용자 결정. fallback으로 하드코딩 인용을
  그대로 쓰면 grounding이 사실상 무력화되므로, 완료율 지표의 정직성을 위해 검증 실패는 사람에게
  넘긴다.
- **의미적 일치 검증 제외, 존재 검증만으로 축소** — 사용자 결정(2026-07-03, 구현 중 발견).
  keyword overlap·cosine 유사도·리랭커 실측 결과 정답/오답 구분 불가로 확인 → 원 계획 리스크가
  실제로 발생 → 중단·보고 후 사용자 승인으로 스코프 축소.
- 이 외 예상되는 사용자 소유 결정 없음 — 위 항목들로 소진됨.

## Integration verification (milestone close)

- [x] `python -m pytest tests/test_workflow_1109_regression.py -q` — grounding 포함 완료율 재측정, 6/10 그대로
- [x] `python -m pytest tests/ -q` — 92/92 통과 (기존 79 + 신규 13, 비퇴행)
- [x] `python scripts/quality_preflight.py --format text` — ok: True
- [x] 완료율 리포트 갱신 (`docs/reports/2026-07-03-wa1-completion-rate.md` "RGA1 갱신" 섹션) — 6/10 유지, 근거 성격 변화 기록
