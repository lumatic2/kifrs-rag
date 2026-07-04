# FS5 Statement Draft Report

> Date: 2026-07-05
> Horizon: `f-acc-financial-statement-draft`
> Evidence: `kifrs/workflows/statement_draft/`, `tests/test_statement_draft.py`

## 한 줄 결론

F-ACC review pack이 이제 검토메모/분개/주석에서 멈추지 않고, 재무제표 본문 표시 후보까지 내려간다.
다만 회사별 TB, 계정과목 mapping, 최종 표시 판단은 아직 사람과 회사 정책 영역으로 남긴다.

## 무엇이 됐나

### 1. 공통 statement draft schema

`StatementLineCandidate`를 추가했다.

- `statement`: 재무상태표, 손익계산서, OCI, note 중 어디로 보낼지
- `line_item`: 표시 후보명
- `amount`: 금액
- `debit_credit`: 차변/대변
- `source_standard`, `source_case_id`, `source_field`: 어떤 기준서/fixture/field에서 왔는지
- `presentation_status`: draft, needs_human_review, not_applicable
- `review_questions`, `note_links`: 사람이 확인할 질문과 근거

이 schema의 의미는 "AI가 재무제표를 확정 작성한다"가 아니라, 회계사가 검토할 표시 후보를
근거와 함께 정리한다는 것이다.

### 2. 1109 금융상품 statement draft pilot

1109 review pack에서 다음 후보가 나온다.

| Source | Statement candidate |
|---|---|
| 최초인식 `AC금융자산` | 재무상태표 금융자산(상각후원가) |
| 최초인식 `FVOCI금융자산` | 재무상태표 금융자산(FVOCI) |
| 최초인식 `FVPL금융자산` | 재무상태표 금융자산(FVPL) |
| `수수료비용` | 손익계산서 금융상품 거래비용 |
| 후속측정 `이자수익` | 손익계산서 이자수익 |
| 후속측정 `평가이익/손실(PL)` | 손익계산서 평가손익 |
| 후속측정 `평가이익/손실(OCI)` | OCI 금융자산평가손익 |
| `classification` | 주석/검토 질문 |

기술적으로는 1109 runner가 이미 계산하던 후속측정 분개를 review pack에 보존했고, statement adapter가
그 분개를 PL/OCI 후보로 바꾼다.

### 3. 1115 수익인식 statement draft pilot

1115 review pack에서 다음 후보가 나온다.

| Path | Statement candidate |
|---|---|
| material right | 손익계산서 수익, 재무상태표 계약부채 |
| significant financing | 재무상태표 매출채권, 손익계산서 수익, 재무상태표 이연금융수익 |
| repurchase financing | 재무상태표 금융부채, 손익계산서 금융비용 |
| measurement | revenue/deferred/financing/repurchase liability note candidate |

따라서 1115 엔진 결과는 이제 "수익인식 검토메모"에서 끝나지 않고 수익, 계약부채, 금융요소, 금융부채
표시 후보까지 이어진다.

### 4. 1116 리스 연결

1116 review pack은 FS2에서 공통 adapter에 연결됐다.

| Source | Statement candidate |
|---|---|
| `사용권자산` | 재무상태표 사용권자산 |
| `리스부채` | 재무상태표 리스부채 |
| `복구충당부채` | 재무상태표 충당부채 |
| `리스채권` | 재무상태표 리스채권 |
| `리스료비용` | 손익계산서 리스료비용 |
| `disclosure_draft` | 주석 후보 |

리스제공자 주석, 변동리스료, 전대리스, 판매후리스 등은 기존 review question을 유지한다.

## 자동화된 것과 남은 것

| 영역 | 지금 자동화 | 남은 사람 검토 |
|---|---|---|
| 기준서 판단 output 연결 | review pack → statement candidate 자동 변환 | 입력 사실과 계약 원문 확인 |
| 분개 기반 line 후보 | 계정명/차대/금액을 statement candidate로 변환 | 회사 계정과목표와 TB mapping |
| 1109 표시 | AC/FVOCI/FVPL, PL/OCI 후보 | 재분류, FX dual-track, 공정가치 출처 |
| 1115 표시 | 수익, 계약부채, 매출채권, 금융부채, 금융비용 후보 | SSP, 확률, 지급조건, 계약 원문 |
| 1116 표시 | 사용권자산, 리스부채, 충당부채, 주석 후보 | 회사별 리스 정책, 리스제공자 주석 |
| 최종 F/S 작성 | 하지 않음 | 전체 재무제표 양식, 계정 재분류, 중요성 판단 |

## 회계법인 설명 방식

이 horizon의 데모 문장은 다음과 같다.

> "계약이나 금융상품 사실관계를 넣으면 K-IFRS 판단, 분개 초안, 검토메모, 주석 질문뿐 아니라
> 재무제표 어디에 표시될지까지 후보를 뽑아줍니다. 최종 계정 mapping과 표시 판단은 회계사가 검토합니다."

이 말이 중요한 이유는 단순 RAG와 차이가 분명하기 때문이다. 단순 RAG는 기준서 문단을 찾아주지만,
여기서는 기준서 판단 결과가 분개와 재무제표 후보 라인까지 내려간다.

## 검증

- `python -m pytest tests/test_statement_draft.py`: 7 passed.
- `python -m pytest tests/test_statement_draft.py tests/test_disclosure_common.py tests/test_1109_review_pack.py tests/test_1115_review_pack.py tests/test_1116_review_pack.py`: 20 passed.
- `git diff --check`: passed.

## 다음 horizon

다음 sequence는 `f-audit-analytical-procedures`다. F-ACC 산출물을 F-AUD 보조 업무로 확장하되,
감사의견이 아니라 공개 F/S 또는 synthetic F/S fixture 기반의 분석적 절차 계산표와 이상징후 메모까지만
다룬다.
