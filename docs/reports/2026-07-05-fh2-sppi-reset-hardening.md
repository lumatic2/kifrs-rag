# FH2 — SPPI Reset Nuance Hardening

> Date: 2026-07-05
> Horizon: `f-acc-1109-hardening`

## 결과

`scenario_06_floating_rate_bond_sppi_nuance`를 NeedsHumanReview에서 automated pack으로 승격했다.

## 무엇을 바꿨나

- `Transaction1109`에 변동금리 재설정 mismatch 입력을 추가했다.
  - `floating_rate_reset_frequency_months`
  - `floating_rate_benchmark_tenor_months`
  - `floating_rate_mismatch_significant`
- `classify_sppi()`가 재설정 주기와 기준금리 테너 불일치를 해석한다.
- mismatch가 있지만 benchmark cash flow 비교상 유의적 변형이 아니면 SPPI Pass로 처리한다.
- scenario_06 fixture를 `special_case`에서 제거하고 AC automated case로 승격했다.

## 완료율 변화

| 구분 | 이전 | 이후 |
|---|---:|---:|
| 1109 총 fixture | 10 | 10 |
| automated | 6 | 7 |
| NeedsHumanReview | 4 | 3 |

## 남은 NeedsHumanReview

- `scenario_05_ifric19_debt_equity_swap`
- `scenario_08_business_model_change_reclassification`
- `scenario_10_foreign_currency_bond_1109_1021`

## 다음

FH3은 `scenario_08_business_model_change_reclassification`의 검토메모 skeleton 강화다. 자동 결론보다는
사업모형 변경 승인 자료, 변경일, 재분류일 공정가치 입력을 구조화해 사람이 이어받기 쉽게 만든다.
