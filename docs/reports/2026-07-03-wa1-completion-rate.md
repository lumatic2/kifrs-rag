# WA1 — 1109 파일럿 완료율 리포트

> Generated: 2026-07-03
> Objective 움직이는 축: 시나리오 완료율 (`docs/OBJECTIVE.md`)
> Horizon: `docs/horizons/workflow-automation.md`

## 완료율: 6/10 (60%)

"완료" = 구조화 거래 입력 -> SPPI/사업모형 판단 -> 최초인식 분개 -> 후속측정 -> 검토메모까지
사람 개입·수정 없이 코드가 끝까지 산출. 100% 미달은 실패가 아니다 — 이번 milestone의
목표는 "측정 가능한 상태"이지 100% 통과가 아니다(docs/plans/2026-07-03-wa1-1109-pilot-engine.md).

## 자동화됨

| 시나리오 | 분류 | 최초인식 | 후속측정 분개 수 |
|---|---|---|---|
| scenario_01_corporate_bond_ac | AC | 930,432 | 5 |
| scenario_02_corporate_bond_fvoci | FVOCI_DEBT | 1,910,000 | 6 |
| scenario_03_credit_linked_note_fvpl | FVPL | 502,500 | 4 |
| scenario_04_listed_equity_fvoci_irrevocable | FVOCI_EQUITY | 50,125,000 | 2 |
| scenario_07_convertible_bond_holder | FVPL | 985,000 | 2 |
| scenario_09_fvpl_designation_accounting_mismatch | FVPL | 1,910,000 | 0 |

## 사람 개입 필요 (WA1 core pipeline 밖)

| 시나리오 | 사유 |
|---|---|
| scenario_05_ifric19_debt_equity_swap | scenario_05_ifric19_debt_equity_swap: special_case='ifric19_debt_equity_swap' — WA1 core pipeline 밖 |
| scenario_06_floating_rate_bond_sppi_nuance | scenario_06_floating_rate_bond_sppi_nuance: special_case='sppi_reset_mismatch' — WA1 core pipeline 밖 |
| scenario_08_business_model_change_reclassification | scenario_08_business_model_change_reclassification: special_case='reclassification' — WA1 core pipeline 밖 |
| scenario_10_foreign_currency_bond_1109_1021 | scenario_10_foreign_currency_bond_1109_1021: special_case='fx_dual_track' — WA1 core pipeline 밖 |

## 다음

- 사람 개입 필요 4건(IFRIC19 발행자 부채소멸, SPPI 변동금리 재설정 불일치, 재분류,
  외화 이중트랙)은 각자 별도 결정 로직이 필요 — WA2/WA3 후보로 승격 검토
  (`docs/horizons/workflow-automation.md`).
- 자동화 6건은 회귀 테스트로 고정(`tests/test_workflow_1109_regression.py`) —
  향후 리팩토링이 숫자를 바꾸면 테스트가 먼저 실패한다.

## RGA1 갱신 (2026-07-03) — 런타임 citation 존재 검증 반영

`docs/horizons/rag-agent-integration.md` RGA1이 `classify()`에 런타임 grounding(존재 검증만,
의미적 일치 검증은 실측 결과 신뢰도 부족으로 제외 — `docs/plans/2026-07-03-rga1-runtime-citation-
grounding.md` 결정 로그 참조)을 배선한 뒤 10개 시나리오를 재실행한 결과:

**완료율: 6/10 (60%), 변화 없음.** 자동화된 6건의 하드코딩 인용이 전부 존재 검증을 통과했다 —
`kifrs.workflows.kifrs1109.grounding`이 처음으로 "이 인용이 실제 DB 조항을 가리키는가"를 코드로
확인했고, 인용이 잘못됐거나 존재하지 않으면 이제 `NeedsHumanReview`로 자동 에스컬레이션된다
(`tests/test_workflow_1109_grounding.py`로 검증). 숫자는 그대로지만 그 숫자를 뒷받침하는 근거의
성격이 "검증 안 된 문자열"에서 "존재가 확인된 인용"으로 바뀌었다.
