# FS1 Statement Draft Surface Inventory

> Date: 2026-07-05
> Horizon: `f-acc-financial-statement-draft`
> Step: FS1 — statement draft surface inventory
> Sources: `kifrs/workflows/kifrs1109/review_pack.py`, `kifrs/workflows/kifrs1115/review_pack.py`, `kifrs/workflows/kifrs1116/review_pack.py`

## 결론

기존 F-ACC review pack은 이미 재무제표 표시 초안으로 보낼 수 있는 세 가지 surface를 갖고 있다.

1. **분개 line**: 계정명과 차/대 금액이 있어 재무제표 line candidate의 가장 강한 source다.
2. **판단 결과**: 1109 classification, 1115 path, 1116 path/judgment_summary가 표시 위치와 review
   question을 정한다.
3. **주석/checklist**: 본문 표시만으로 닫히지 않는 항목을 note link 또는 human review question으로 넘긴다.

따라서 FS2는 새 판단 엔진을 만들지 않고, review pack을 읽어 재무상태표/손익/OCI/주석 연결 후보를
생성하는 공통 schema와 adapter부터 만든다.

## 1109 금융상품 review pack surface

| Source field | 현재 의미 | F/S draft 연결 | 자동화 상태 |
|---|---|---|---|
| `standard` | `KIFRS1109` | source standard | ready |
| `case_id` | fixture/거래 label | source case id | ready |
| `status` | `automated` 또는 `needs_human_review` | line candidate status | ready |
| `classification` | `AC`, `FVOCI_DEBT`, `FVOCI_EQUITY`, `FVPL` | 금융자산 표시 분류, PL/OCI 분기 | ready if automated |
| `journal_entry.lines[]` | 최초인식 계정, 차/대 금액 | 재무상태표 금융자산/현금, PL 수수료비용 | ready if present |
| `review_memo` | 분류·측정 판단 memo | note link, reviewer context | ready |
| `review_checklist[]` | SPPI/사업모형, 최초분개, 후속측정 검토 | review questions | ready |
| `needs_human_review[]` | 회사 보유 목적, 후속측정 입력, 재분류/FX boundary | presentation status and questions | ready |
| `citations[]` | 기준서 문단 id | note support | ready |

### 1109 표시 후보

- 재무상태표:
  - `AC금융자산` → 금융자산(상각후원가 측정)
  - `FVOCI금융자산` / `FVOCI금융자산(자본)` → 금융자산(FVOCI)
  - `FVPL금융자산` → 금융자산(FVPL)
  - `현금` credit → 현금및현금성자산 감소
- 손익계산서:
  - `수수료비용` → 금융상품 취득 관련 비용(FVPL 거래원가)
  - 후속측정 module의 `이자수익`, `평가이익(PL)`, `평가손실(PL)`은 FS3에서 second-pass source 후보.
- OCI:
  - 후속측정 module의 `평가이익(OCI)`, `평가손실(OCI)`은 FVOCI 표시 후보.
- 주석 연결:
  - classification, SPPI/사업모형 판단, 공정가치 출처, 위험관리 정책 확인 질문.

### 1109 NeedsHumanReview boundary

- 재분류(`scenario_08`)는 statement line을 확정하지 않고 재분류일, 공정가치, 변경 전후 분류 후보를
  review question으로 넘긴다.
- FX dual-track(`scenario_10`)은 1109 분류와 1021 환산 표시가 갈라지므로, 환산차이/공정가치 변동의
  PL/OCI 구분 질문을 line candidate에 붙여야 한다.

## 1115 수익인식 review pack surface

| Source field | 현재 의미 | F/S draft 연결 | 자동화 상태 |
|---|---|---|---|
| `standard` | `KIFRS1115` | source standard | ready |
| `case_id` | fixture/계약 label | source case id | ready |
| `status` | `automated` 또는 `needs_human_review` | line candidate status | ready |
| `path` | material right, financing component, repurchase 등 | 수익/계약부채/금융요소 표시 분기 | ready if automated |
| `measurement.recognized_revenue` | 당기 수익 초안 | 손익계산서 수익 | ready |
| `measurement.deferred_revenue` | 이연/계약부채 초안 | 재무상태표 계약부채 | ready when non-zero |
| `measurement.financing_effect` | 금융요소 또는 재매입 spread | 손익/부채 표시 후보 | ready when non-zero |
| `measurement.repurchase_liability` | 재매입약정 금융부채 | 재무상태표 금융부채 | ready when non-zero |
| `measurement.allocation[]` | 수행의무별 배분 | 주석 또는 reviewer context | ready |
| `journal_entries[].lines[]` | 수익/계약부채/매출채권/금융부채 분개 | F/S line candidate source | ready |
| `review_checklist[]` | 5단계 판단, 측정표, 분개, 메모 | review questions | ready |
| `needs_human_review[]` | 계약 원문, SSP, 확률, 지급조건 확인 | presentation status and questions | ready |
| `citations[]` | 기준서 문단 id | note support | ready |

### 1115 표시 후보

- 손익계산서:
  - `수익` credit 또는 `recognized_revenue` → 수익
  - `금융비용` debit → 금융비용
  - financing component의 이연금융수익은 기간 경과 인식 전에는 부채성 또는 이연수익 표시 질문으로 둔다.
- 재무상태표:
  - `계약부채(중요한 권리)` → 계약부채
  - `매출채권` → 매출채권
  - `금융부채` / `repurchase_liability` → 금융부채
  - `현금` debit → 현금 증가
- 주석 연결:
  - 수행의무, 유의적 금융요소, 재매입약정, 중요 권리 배분 근거.

### 1115 NeedsHumanReview boundary

- 계약 식별 실패나 필수 입력 누락은 line candidate를 만들지 않고, `required_inputs`와 `review_questions`
  기반의 note/review queue로 넘긴다.
- 자동 산출된 금액도 계약 원문, 독립판매가격, 확률, 지급조건 확인 없이는 `draft` status로만 표시한다.

## 1116 리스 review pack surface

| Source field | 현재 의미 | F/S draft 연결 | 자동화 상태 |
|---|---|---|---|
| `standard` | `KIFRS1116` | source standard | ready |
| `case_id` | fixture/계약 label | source case id | ready |
| `status` | `automated` 또는 `needs_human_review` | line candidate status | ready |
| `judgment_summary` | 리스 판단 경로와 산출 개수 | reviewer context | ready |
| `journal_entry.lines[]` | 사용권자산/리스부채/리스채권/운용리스자산 등 | F/S line candidate source | ready if present |
| `review_memo` | 리스 식별, 측정, 결론 memo | note link, reviewer context | ready |
| `disclosure_draft` | 리스이용자 주석 초안 | note link | ready for lessee automated packs |
| `review_checklist[]` | 리스 판단, 최초분개, 주석 검토 | review questions | ready |
| `needs_human_review[]` | 회사 정책, 변동리스료, 전대리스 등 | presentation status and questions | ready |
| `citations[]` | 기준서 문단 id | note support | ready |

### 1116 표시 후보

- 재무상태표:
  - `사용권자산` → 사용권자산
  - `리스부채` → 리스부채
  - `복구충당부채` → 충당부채
  - `리스채권` → 리스채권
  - `운용리스자산` → 유형자산 또는 운용리스 관련 자산 표시 후보
- 손익계산서:
  - `리스료비용` → 리스료비용
  - 후속측정 module의 감가상각/이자비용은 FS2 이후 second-pass source 후보.
- 주석 연결:
  - `disclosure_draft` 전체가 note candidate이며, 만기분석/변동리스료/전대리스/판매후리스 질문을 포함한다.

### 1116 NeedsHumanReview boundary

- 리스범위 확장+축소 동시 변경은 line candidate를 확정하지 않고, 변경 전 장부금액, 축소 비율, 수정
  할인율, 변경 전후 지급 스케줄을 review question으로 남긴다.
- 리스제공자 주석은 현재 review pack의 자동 주석 범위 밖이므로 note link는 `needs_human_review`로 둔다.

## FS2 schema 후보

FS2에서 만들 공통 schema는 아래 정도면 충분하다.

```python
StatementLineCandidate(
    statement: Literal["balance_sheet", "income_statement", "oci", "note"],
    line_item: str,
    amount: float | None,
    debit_credit: Literal["debit", "credit", "none"],
    source_standard: str,
    source_case_id: str,
    source_field: str,
    presentation_status: Literal["draft", "needs_human_review", "not_applicable"],
    review_questions: list[str],
    note_links: list[str],
)
```

초기 adapter 우선순위:

1. `journal_entry.lines[]` 또는 `journal_entries[].lines[]`를 statement line으로 변환한다.
2. domain-specific field(`classification`, `path`, `measurement`)로 line item과 PL/OCI/BS 분기를 보정한다.
3. `needs_human_review[]`의 질문을 candidate에 붙인다.
4. amount가 없는 판단/주석 항목은 `statement="note"` candidate로 둔다.

## FS2에서 하지 않을 것

- 회사별 TB, 계정과목 mapping table, 재무제표 양식 rendering.
- 1109/1116 후속측정 전체를 한 번에 statement draft에 연결.
- DART 양식 자동 채우기.
- 최종 표시 판단 자동 확정.

FS2는 "review pack에서 재무제표 line candidate가 나온다"는 최소 product surface를 먼저 만든다.
