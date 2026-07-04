# FH5 — 1109 Hardening Delta Report

> Date: 2026-07-05
> Horizon: `f-acc-1109-hardening`

## 한 문장 결과

1109 review pack은 hardening 전 6/10 automated에서 hardening 후 7/10 automated로 개선됐고, 남은
NeedsHumanReview 3개 중 2개는 구조화 skeleton memo를 제공한다.

## 전후 비교

| 지표 | FH 시작 전 | FH 완료 후 |
|---|---:|---:|
| 총 fixture | 10 | 10 |
| automated review pack | 6 | 7 |
| NeedsHumanReview | 4 | 3 |
| NeedsHumanReview 중 skeleton memo 제공 | 0 | 2 |

## 케이스별 상태

| fixture | 상태 | classification | review memo | 의미 |
|---|---|---|---|---|
| `scenario_01_corporate_bond_ac` | automated | AC | 있음 | 기존 유지 |
| `scenario_02_corporate_bond_fvoci` | automated | FVOCI_DEBT | 있음 | 기존 유지 |
| `scenario_03_credit_linked_note_fvpl` | automated | FVPL | 있음 | 기존 유지 |
| `scenario_04_listed_equity_fvoci_irrevocable` | automated | FVOCI_EQUITY | 있음 | 기존 유지 |
| `scenario_05_ifric19_debt_equity_swap` | needs_human_review | — | 없음 | IFRIC19 별도 horizon 전까지 범위 밖 |
| `scenario_06_floating_rate_bond_sppi_nuance` | automated | AC | 있음 | FH2에서 자동화 |
| `scenario_07_convertible_bond_holder` | automated | FVPL | 있음 | 기존 유지 |
| `scenario_08_business_model_change_reclassification` | needs_human_review | — | skeleton 있음 | FH3에서 skeleton 강화 |
| `scenario_09_fvpl_designation_accounting_mismatch` | automated | FVPL | 있음 | 기존 유지 |
| `scenario_10_foreign_currency_bond_1109_1021` | needs_human_review | — | boundary 있음 | FH4에서 1109/1021 boundary 강화 |

## 남은 경계

- IFRIC19 부채-지분 스왑은 해석서 성격이 강해 별도 horizon 전까지 자동화하지 않는다.
- 재분류는 사업모형 변경 승인, 재분류일, 공정가치 입력이 필요하므로 skeleton memo로 사람이 이어받는다.
- 외화 dual-track은 1109 분류와 1021 외화환산 표시를 분리해 사람이 판단한다.

## 다음 sequence

다음 horizon은 `f-acc-financial-statement-draft`다. F-ACC pack이 판단·분개·검토메모·주석 checklist까지
갖췄으므로, 이제 F/S support 산출물인 재무제표 본문/표시 draft로 확장한다.
