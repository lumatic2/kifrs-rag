# Plan: RGA1 — 런타임 Citation Grounding 레이어

> Objective: `docs/OBJECTIVE.md`
> Horizon: `docs/horizons/rag-agent-integration.md` (`rag-agent-integration`)
> Milestone: RGA1 — 런타임 grounding 레이어 구축
> Created: 2026-07-03

## Scope boundary

`kifrs/workflows/kifrs1109/`의 결정 엔진(`sppi.py`, `business_model.py`, `classify.py`,
`initial_entry.py`, `review_memo.py`)이 `reasons` 문자열에 하드코딩한 조항 인용
(예: `[1109-4.1.2(b)/4.1.2A(b), B4.1.7~7B]`)을 런타임에 `kifrs.store`/`kifrs.embed` 직접 import로
검증한다. 검증 = ① 인용된 조항 ID가 DB에 실제 존재하는지, ② 그 문단 텍스트가 reason 문구와
의미적으로 부합하는지. 부합하지 않거나 문단을 못 찾으면 `NeedsHumanReview`.

Out of scope (이번 milestone에서 다루지 않음, 이유):
- **MCP 프로토콜 경유 호출** — horizon 결정으로 직접 import만 사용.
- **인용을 엔진이 스스로 찾아 채우는 기능(자동 인용 생성)** — 이번 범위는 *기존 하드코딩 인용의
  검증*이지, 새 인용의 자동 발견이 아니다. 새 시나리오/규칙 추가 시 인용은 여전히 사람이 채운다.
- **grounding 결과 캐싱/성능 튜닝** — RGA2 후보. 이번엔 정확성만 확보.
- **다른 도메인(1116 등) 포팅** — RGA3/WA2 후보.

## Step tree (leaf test 적용 — 시그니처 수준)

- [ ] **Step 1 — 인용 추출 유틸** (`kifrs/workflows/kifrs1109/grounding.py::extract_citations`)
  `reasons` 문자열에서 `[1109-...]` 형태 토큰을 정규식으로 파싱해 조항 ID 리스트로 분해
  (예: `4.1.2(b)`, `B4.1.18~19`). (verify: sppi.py/business_model.py/classify.py/initial_entry.py/
  review_memo.py의 기존 인용 문자열 전수를 파싱해 예외 없이 ID 리스트 산출하는 단위 테스트)

- [ ] **Step 2 — 존재 검증** (`grounding.py::verify_citation_exists`)
  `kifrs.store`를 직접 import해 조항 ID로 문단을 조회, 존재 여부 반환. (verify: Step 1에서 추출한
  전체 인용 ID가 DB에서 조회되는지 확인하는 테스트 — 존재하지 않는 가짜 ID로 음성 테스트 포함)

- [ ] **Step 3 — 의미적 일치 확인** (`grounding.py::verify_citation_matches_reason`)
  조회된 문단 텍스트와 reason 문구 사이 최소 일치(`kifrs.embed` 임베딩 코사인 유사도 threshold 또는
  키워드 overlap)를 확인. (verify: 알려진 정답 쌍 3~5개로 threshold 통과, 의도적으로 틀린 쌍 1~2개로
  실패 확인하는 단위 테스트)

- [ ] **Step 4 — NeedsHumanReview 배선** (`classify.py`, `sppi.py`, `business_model.py` 등 호출부)
  각 판정 함수가 반환 직전 Step 1~3 grounding 파이프라인을 통과시키고, 실패 시 기존
  `NeedsHumanReview` 예외 패턴으로 던진다. (verify: 기존 10개 시나리오 회귀 재실행 — 자동화된
  6건은 grounding 통과로 그대로 자동 산출, 나머지 4건은 기존 `special_case` 경로 유지)

- [ ] **Step 5 (integration) — 회귀 갱신 + 완료율 재측정** (`tests/test_workflow_1109_regression.py`,
  `docs/reports/2026-07-03-wa1-completion-rate.md` 갱신 또는 신규 리포트)
  grounding 경로 포함해 10개 시나리오 전체 재실행, 완료율이 6/10에서 변화했는지 기록.
  (verify: `python -m pytest tests/ -q` 전체 통과 + 리포트 파일 갱신)

## 결정 로그

- **grounding 시점: 런타임** — 사용자 결정. Objective의 "K-IFRS 기반" 전제를 실질적으로 지키려면
  빌드 시점 검증만으로는 부족하다고 판단.
- **호출 경로: 직접 import** — 사용자 결정. MCP는 프로세스 경계를 넘는 외부 세션용 레이어이고,
  엔진은 같은 프로세스 내부 코드 — 한계 #6(MCP stdio fragility) 우회.
- **불일치 처리: NeedsHumanReview 에스컬레이션** — 사용자 결정. fallback으로 하드코딩 인용을
  그대로 쓰면 grounding이 사실상 무력화되므로, 완료율 지표의 정직성을 위해 검증 실패는 사람에게
  넘긴다.
- **의미적 일치 threshold 값** — 아직 미정. Step 3 구현 중 실제 인용-문단 쌍으로 보정 필요.
  구현 중 도출된 값이 지나치게 엄격/느슨해 기존 6개 자동화 시나리오가 grounding 실패로 전환되면,
  그건 새 리스크/스코프 변경이므로 중단하고 사용자에게 보고 — 무중단 진행 예외.
- 이 외 예상되는 사용자 소유 결정 없음 — 위 항목들로 소진됨.

## Integration verification (milestone close)

- `python -m pytest tests/test_workflow_1109_regression.py -q` — grounding 포함 완료율 재측정
- `python -m pytest tests/ -q` — 기존 79개 테스트 비퇴행
- `python scripts/quality_preflight.py --format text` — ok: True
- 완료율 리포트 갱신 — 6/10에서 변화 여부(개선이든 악화든) 정직하게 기록
