# FH4 — FX Dual-track Boundary

> Date: 2026-07-05
> Horizon: `f-acc-1109-hardening`

## 결과

`scenario_10_foreign_currency_bond_1109_1021`은 NeedsHumanReview로 유지한다. 대신 review pack에
1109 분류·측정과 1021 외화환산 표시를 분리한 boundary memo를 포함한다.

## 추가된 산출물

- `kifrs/workflows/kifrs1109/fx_dual_track.py`
- `generate_fx_dual_track_memo()`
- `tests/test_1109_fx_dual_track.py`

## Boundary memo 섹션

1. 왜 dual-track인가
2. 1109 입력
3. 1021 입력
4. 표시 질문
5. 결론 보류

## 왜 자동 결론이 아닌가

외화 금융상품은 1109 분류와 1021 환산 표시가 동시에 필요하다. 기능통화, 계약통화, 취득일/보고일 환율,
이자·원금 수취일 환율, 공정가치 변동 자료가 없으면 자동 결론은 위험하다. FH4는 결론 자동화 대신 두
트랙을 분리해 사람이 이어받을 질문과 입력을 명확히 한다.

## 다음

FH5에서 1109 hardening 전후 automated/NeedsHumanReview 변화와 남은 경계를 리포트로 닫는다.
