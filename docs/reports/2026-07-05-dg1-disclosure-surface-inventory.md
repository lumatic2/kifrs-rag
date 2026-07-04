# DG1 — Disclosure Surface Inventory

> Date: 2026-07-05
> Horizon: `f-acc-disclosure-generalization`

## 왜 이 inventory가 필요한가

F-ACC review pack은 1116, 1109, 1115로 반복됐다. 이제 다음 질문은 "검토메모와 분개 초안 옆에 주석
초안/checklist를 여러 기준서로 붙일 수 있는가"다. DG1은 코드 공통 schema를 만들기 전에, 각 도메인의
어떤 output이 주석 작성 surface로 재사용될 수 있는지 정리한다.

## 현재 도메인별 surface

| 도메인 | 이미 있는 산출물 | 주석 surface로 재사용할 field | 자동화 상태 |
|---|---|---|---|
| 1116 리스 | disclosure requirement, portfolio contribution, disclosure note, DART cross-check | 요구항목 id, citation, fillable flag, 집계 field, maturity bucket, conditional item | 8/11 정량 자동 + 조건부 항목 human |
| 1115 수익 | decision path, five-step, measurement, journal entries, review checklist, human review action | 수익인식 path, material right/financing/repurchase 여부, 수익/이연/금융요소 금액, 입력 추정치 검토 질문 | 4/4 review pack 자동, disclosure skeleton 미구현 |
| 1109 금융상품 | classification, initial entry, subsequent measurement count, review checklist, human review action, citations | 분류, SPPI/사업모형 판단, 후속측정 입력값, 공정가치/이자/배당/위험관리 자료 요청 | 6/10 review pack 자동, disclosure skeleton 미구현 |

## 공통 disclosure schema 후보

```text
DisclosureChecklistItem
  standard
  item_id
  label
  citation
  source_kind          # requirement | decision | measurement | human_input
  source_field
  fill_status          # auto | needs_human_review | not_applicable
  draft_value
  required_inputs[]
  review_questions[]
```

공통 renderer는 "요구항목 → 현재 값/상태 → 근거 → 사람 보완 질문" 순서로 만들 수 있다.

## 기준서별 첫 pilot 후보

| 후보 | 왜 먼저 할 만한가 | DG step |
|---|---|---|
| 1115 material right / significant financing / repurchase disclosure skeleton | R15가 이미 path, 측정표, human review action을 모두 갖고 있어 source 연결이 쉽다 | DG3 |
| 1109 financial instrument classification/measurement disclosure skeleton | 1109는 공시 요구가 넓지만 pack에 분류·후속측정·공정가치/위험자료 요청이 이미 있다 | DG4 |
| 1116 existing disclosure adapter | 이미 구현된 요구항목 schema를 common schema로 감싸는 기준점 | DG2 |

## NeedsHumanReview 경계

주석은 회사 전체 포트폴리오, 회계정책 문구, 위험관리 서술, 조건부 거래 유무가 필요하다. 따라서 일반화
schema의 핵심은 자동 초안보다 **누락된 회사자료와 리뷰 질문을 빠뜨리지 않는 것**이다.

| 경계 | 예시 | 처리 |
|---|---|---|
| 회사 전체 자료 필요 | 1116 변동리스료, 전대리스, 판매후리스 | `needs_human_review` |
| 추정치/SSP 검증 필요 | 1115 material right SSP, 행사확률 | `needs_human_review` 질문 |
| 위험관리 서술 필요 | 1109 신용위험, 유동성위험, 시장위험 | skeleton + required_inputs |
| 원문/회사 주석 문체 필요 | 회계정책 문구 | renderer 밖 human edit |

## DG2 구현 방향

1. 1116 `DisclosureRequirement`를 그대로 감싸는 common item을 만든다.
2. 1115 review pack에서 `path`, `measurement`, `needs_human_review`를 disclosure item source로 매핑한다.
3. 1109 review pack에서 `classification`, `review_checklist`, `needs_human_review`를 disclosure item source로 매핑한다.
4. renderer는 숫자가 있으면 금액을 표시하고, 없으면 required input/review question을 표시한다.

## 결론

DG1 결론은 "주석 일반화는 가능하지만, 바로 완성 주석을 쓰는 문제가 아니라 checklist/source mapping 문제"다.
1116은 정량 요구항목 중심, 1115는 계약 판단·측정 중심, 1109는 분류·위험자료 중심으로 서로 다르다.
따라서 DG2에서는 완성 문장 생성보다 `DisclosureChecklistItem` schema와 domain adapter부터 만든다.
