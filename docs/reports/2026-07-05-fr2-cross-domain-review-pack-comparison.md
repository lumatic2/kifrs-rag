# FR2 — Cross-domain Review Pack Comparison

> Date: 2026-07-05
> Horizon: `f-acc-1109-review-pack`

## 왜 비교했나

1116 리스와 1109 금융상품 모두 F-ACC review pack을 만들 수 있게 됐다. 이제 질문은 "다음 도메인도
같은 방식으로 붙일 수 있는가"와 "지금 공통 schema를 코드로 뽑아도 되는가"다.

FR2의 결론은 다음과 같다.

> 공통 제품 구조는 이미 보인다. 하지만 코드 공통화는 아직 하지 않는다. 세 번째 도메인 또는 주석 대사
> 표면이 생긴 뒤 추출하는 편이 낫다.

## 공통 구조

| 공통 요소 | 1116 리스 | 1109 금융상품 | 제품 의미 |
|---|---|---|---|
| 기준서 | `KIFRS1116` | `KIFRS1109` | 어떤 기준서 pack인지 식별 |
| case id | lease label | fixture label | workpaper 단위의 식별자 |
| 상태 | automated / needs_human_review | automated / needs_human_review | 자동화 경계 표시 |
| 판단 요약 | 리스 경로와 산출물 수 | 분류와 최초인식 금액 | manager가 먼저 읽는 한 줄 |
| 분개 초안 | 최초 리스 분개 | 최초 금융상품 분개 | 회계처리 초안 |
| 검토메모 | 1116 검토메모 | 1109 검토메모 | 회계자문팀 산출물 본문 |
| 리뷰 checklist | ready / needs_human_review 항목 | ready / needs_human_review 항목 | reviewer가 확인할 업무 queue |
| 사람 검토 필요 항목 | 추가자료, 리뷰 질문, 기준서 방향 | 추가자료, 리뷰 질문, 기준서 방향 | AI가 멈춘 뒤 사람이 이어받는 지점 |
| 인용 목록 | 1116/1109 citation | 1109 citation | 기준서 근거 trace |
| markdown renderer | workpaper draft | workpaper draft | PoC에서 보여줄 산출물 |

## 도메인별 차이

| 차이 | 1116 리스 | 1109 금융상품 | 해석 |
|---|---|---|---|
| 핵심 판단 축 | 리스 식별, 리스이용자/제공자, 측정, 변경 | SPPI, 사업모형, 금융상품 분류 | 판단트리는 도메인별 유지 |
| 도메인 필드 | `disclosure_draft` | `classification` | 공통 schema의 optional extension 후보 |
| 주석 초안 | 있음 | 없음 | 1116은 B5 주석 작성까지 연결, 1109 FR1은 B3 판단/분개 중심 |
| 자동화율 | 9/10 | 6/10 | 1116은 입력 구조가 더 결정론적, 1109는 특수 케이스가 더 많음 |
| NeedsHumanReview 성격 | 복합 리스 변경, 회사 정책/조건부 주석 | IFRIC19, SPPI nuance, 재분류, 외화 이중트랙 | 사람 검토 queue는 공통, 질문 내용은 도메인별 |
| renderer section | 검토메모 / 분개 / 주석 / checklist | 검토메모 / 분개 / checklist | section ordering은 공통 + optional section으로 처리 가능 |

## 공통 schema 후보

지금 보이는 공통 상위 모델은 다음 정도다.

```text
ReviewPackBase
  standard
  case_id
  status
  judgment_summary
  journal_entry
  review_memo
  review_checklist[]
  needs_human_review[]
  citations[]

HumanReviewAction
  issue
  why_blocked
  required_inputs[]
  review_questions[]
  candidate_guidance[]

ReviewChecklistItem
  label
  status
  note
```

도메인별 확장 후보:

```text
Lease1116ReviewPack
  disclosure_draft

FinancialInstrument1109ReviewPack
  classification
```

## 지금 코드 공통화를 하지 않는 이유

1. 아직 도메인이 2개뿐이다. 지금 추출하면 1116/1109의 우연한 공통점까지 framework가 될 위험이 있다.
2. 1116은 주석 초안까지 포함하지만 1109는 아직 분류·분개·검토메모 중심이다.
3. 1115 수익 또는 주석 대사처럼 세 번째 표면이 생기면, 어떤 필드가 진짜 공통이고 어떤 필드가 도메인 확장인지 더 분명해진다.
4. 지금은 중복 코드보다 제품 학습 속도가 더 중요하다.

## 다음 실행 순서

FR2 이후에는 두 갈래가 있다.

| 후보 | 하는 일 | 추천도 |
|---|---|---|
| FR3 — next-domain readiness decision | 1115 신규 엔진, 1109 hardening, 주석 대사 확장 중 다음 기술 확장을 고른다 | 높음 |
| Common schema extraction | `kifrs/workflows/review_pack/` 공통 base schema와 renderer helper를 만든다 | 보류 |

추천은 FR3다. 공통화는 하나 더 도메인을 붙인 뒤 해도 늦지 않다.

## 결론

F-ACC review pack은 이제 단일 리스 기능이 아니라, 회계자문팀 workpaper 초안이라는 반복 가능한 제품
구조로 보인다. 다만 코드는 아직 기준서별 전용 모듈로 유지한다. 다음은 새 도메인/기능을 하나 더 붙여
공통 구조를 더 확실히 만든 뒤 추출 여부를 다시 판단한다.
