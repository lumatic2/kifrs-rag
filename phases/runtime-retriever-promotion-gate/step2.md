# Step 2: Regression And Latency Gate

## 읽어야 할 파일
- docs/reports/2026-07-05-rpg1-promotion-evidence-inventory.md — 왜: RPG2가 검증해야 할 evidence 목록이다.
- docs/horizons/runtime-retriever-promotion-gate.md — 왜: RPG2 acceptance를 확인한다.
- scripts/default_retriever_guard.py — 왜: 기존 default guard와 충돌하지 않는 gate를 만든다.

## 작업
promote/defer 판단 전에 recall/citation regression과 기본 runtime cost limit을 확인하는 gate를 구현한다.

## Acceptance Criteria
```bash
python -m pytest tests\test_retriever_regression_latency_gate.py -q
python scripts\retriever_regression_latency_gate.py --format text --write
```

## 검증 절차
1. AC 커맨드 실행.
2. gate가 regression, citation, latency/cost, missing evidence를 분리하는지 확인.
3. phase index step 2 상태를 completed로 갱신한다.

## 금지사항
- happy-path 점수만으로 promote 처리하지 마라.
