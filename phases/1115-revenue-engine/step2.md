# Step 2: five-step-decision-engine

Status: completed (2026-07-05)

## 읽어야 할 파일

- `docs/horizons/f-acc-1115-revenue-engine.md` — 왜: R15-2가 요구하는 5단계 판단 범위가 있다.
- `kifrs/workflows/kifrs1115/classify.py` — 왜: R15-1 decision path를 5단계 판단으로 확장한다.
- `tests/test_workflow_1115.py` — 왜: 4개 seed fixture의 path/citation 회귀와 5단계 결론을 검증한다.

## 작업

1115 decision output에 다음 5단계 결론을 추가한다.

1. 계약 식별
2. 수행의무 식별
3. 거래가격 산정
4. 거래가격 배분
5. 수익인식 시점/방식

## Acceptance Criteria

```powershell
python -m pytest tests/test_workflow_1115.py
git diff --check
```

## 결과

- `RevenueDecision.five_step`에 5개 `FiveStepConclusion`을 항상 채운다.
- 계약 식별의 기본 사실이 부족하면 `NeedsHumanReview`로 보낸다.
- material right, significant financing, repurchase call option의 step별 결론을 테스트로 고정했다.
