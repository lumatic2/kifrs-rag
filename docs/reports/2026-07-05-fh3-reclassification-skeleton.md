# FH3 — Reclassification Memo Skeleton

> Date: 2026-07-05
> Horizon: `f-acc-1109-hardening`

## 결과

`scenario_08_business_model_change_reclassification`은 여전히 NeedsHumanReview다. 다만 이제 빈 pack이 아니라
재분류 검토메모 skeleton을 포함한다.

## 추가된 산출물

- `kifrs/workflows/kifrs1109/reclassification.py`
- `generate_reclassification_memo()`
- `tests/test_1109_reclassification.py`

## Skeleton 섹션

1. 재분류 트리거
2. 필요 입력
3. 판단 질문
4. 처리 방향 초안
5. 결론 보류

## 왜 자동 결론이 아닌가

재분류는 사업모형 변경이 실제로 발생했는지, 변경일/재분류일이 언제인지, 재분류일 공정가치를 어떻게
측정했는지에 따라 결론이 달라진다. fixture 하나로 자동 결론을 내리면 제품 신뢰도를 해친다. 따라서
FH3의 hardening은 결론 자동화가 아니라 사람이 이어받을 workpaper skeleton 제공이다.

## 다음

FH4는 `scenario_10_foreign_currency_bond_1109_1021`의 1109/1021 dual-track boundary를 정리한다.
