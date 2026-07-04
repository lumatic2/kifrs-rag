# FH1 — 1109 Blocker Taxonomy

> Date: 2026-07-05
> Horizon: `f-acc-1109-hardening`

## 현재 기준선

1109 review pack은 10개 fixture 중 6개 automated, 4개 NeedsHumanReview다. hardening의 목표는 모든
케이스를 억지 자동화하는 것이 아니라, 자동화 가능한 blocker와 skeleton 강화가 맞는 blocker를 나누는 것이다.

## NeedsHumanReview 4개

| fixture | special_case | 현재 issue | hardening 분류 | 다음 액션 |
|---|---|---|---|---|
| `scenario_05_ifric19_debt_equity_swap` | `ifric19_debt_equity_swap` | IFRIC 19 부채-지분 스왑 | 범위 밖 유지 | required input/checklist 유지, 별도 IFRIC horizon 전까지 자동화 보류 |
| `scenario_06_floating_rate_bond_sppi_nuance` | `sppi_reset_mismatch` | 변동금리 재설정 불일치 SPPI 판단 | 자동화 후보 | FH2에서 reset period/benchmark cash flow skeleton을 엔진화 |
| `scenario_08_business_model_change_reclassification` | `reclassification` | 사업모형 변경에 따른 재분류 | skeleton 강화 | FH3에서 재분류 검토메모 skeleton과 required input을 더 구조화 |
| `scenario_10_foreign_currency_bond_1109_1021` | `fx_dual_track` | 외화 금융상품 1109+1021 이중 트랙 | 경계 강화 | FH4에서 1109 분류와 1021 환산 표시를 분리한 boundary report 작성 |

## 우선순위

1. **FH2 — SPPI reset nuance hardening**
   - 가장 자동화 가능성이 높다.
   - 필요한 입력이 계약상 기준금리, 재설정 주기, 이자 산정기간, 시장금리 보정 조항으로 좁다.
   - 자동화 성공 시 1109 automated pack이 6/10 → 7/10으로 오른다.
2. **FH3 — reclassification memo skeleton**
   - 재분류는 자동 결론보다 검토메모 skeleton이 맞다.
   - 사업모형 변경 승인 자료, 변경일, 재분류일 공정가치를 구조화 입력으로 정리한다.
3. **FH4 — FX dual-track boundary**
   - 1109와 1021을 함께 봐야 하므로 이 repo의 1109 core engine만으로 닫지 않는다.
   - 필요한 입력과 표시 질문을 강화한다.
4. **IFRIC19**
   - 별도 해석서 성격이 강해 이번 FH horizon에서는 자동화하지 않는다.

## 결론

FH horizon의 첫 구현은 SPPI reset mismatch다. 그 다음은 재분류/외화 케이스의 skeleton 강화다. 목표는
자동화율 숫자만 올리는 것이 아니라, 사람이 이어받는 지점의 입력·질문·판단 메모를 더 선명하게 만드는 것이다.
