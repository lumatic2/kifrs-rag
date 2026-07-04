# R15 — 1115 Revenue Engine Completion Report

> Date: 2026-07-05
> Horizon: `f-acc-1115-revenue-engine`

## 한 문장 결과

1115 수익인식 seed 4개 유형이 구조화 입력에서 판단 경로, 5단계 판단, 측정표, 분개 초안, 검토메모,
F-ACC review pack까지 자동 산출된다.

## 자동화율

| 구분 | 개수 |
|---|---:|
| 총 fixture | 4 |
| automated review pack | 4 |
| needs_human_review seed | 0 |
| 자동화율 | 100% |

## Fixture별 결과

| fixture | path | journal entries | checklist | human review actions | citation ids |
|---|---|---:|---:|---:|---:|
| `scenario_01_renewal_option` | `material_right_renewal_option` | 1 | 4 | 1 | 7 |
| `scenario_02_discount_right` | `material_right_discount_option` | 1 | 4 | 1 | 8 |
| `scenario_03_significant_financing` | `significant_financing_component` | 1 | 4 | 1 | 9 |
| `scenario_04_repurchase_call_option` | `repurchase_financing_arrangement` | 2 | 4 | 1 | 4 |

## 산출물 연결

| 단계 | 산출물 | evidence |
|---|---|---|
| R15-1 | schema + seed fixture inventory | `kifrs/workflows/kifrs1115/schema.py`, `fixtures.py` |
| R15-2 | five-step decision engine | `kifrs/workflows/kifrs1115/classify.py` |
| R15-3 | measurement + journal entry draft | `measurement.py`, `journal_entry.py` |
| R15-4 | review memo renderer | `review_memo.py` |
| R15-5 | review pack integration | `review_pack.py`, `tests/test_1115_review_pack.py` |

## 사람 검토 경계

4개 seed fixture는 자동 pack까지 생성된다. 그러나 pack은 최종 판단이 아니라 초안이다. 각 자동 pack에는
`입력 사실과 추정치 검토` action이 포함된다. 실제 업무에서는 계약 원문, SSP, 권리 행사 확률, 지급조건,
경영진 판단 메모를 사람이 확인해야 한다.

입력값이 부족하면 `needs_human_review` pack으로 내려간다. 예: 유의적 금융요소 flag만 있고
현금판매가격/약속대가가 없으면 자동 메모·분개를 생성하지 않고, 필요한 추가자료와 리뷰 질문을 표시한다.

## 제품 의미

1115는 1116/1109 다음의 세 번째 F-ACC review pack 표면이다. 이로써 F-ACC workpaper pack이 단일 기준서
전용이 아니라, 서로 다른 판단 도메인에도 반복 가능한 제품 구조라는 증거가 강해졌다.

다음 sequence는 `f-acc-disclosure-generalization`이다. 이유는 1116에서 이미 주석 초안과 DART 대사를
실증했고, 1115/1109가 판단·분개·검토메모 표면을 확장했으므로 이제 B5 주석 작성 자동화를 여러 기준서로
일반화할 차례다.
