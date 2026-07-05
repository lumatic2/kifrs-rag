# Step 4: Promotion Decision Gate

## 읽어야 할 파일

- `docs/reports/2026-07-05-rqf2-baseline-snapshot.md` - 왜: default baseline evidence다.
- `docs/reports/2026-07-05-rqf3-regression-matrix.md` - 왜: opt-in retriever evidence다.
- `docs/reports/2026-07-05-default-retriever-guard.md` - 왜: default 변경 guard 조건이다.

## 작업

promote/defer/rollback 중 하나를 결정하는 gate를 만든다. explicit authorization이 없으면 default 변경은 실행하지 않고 decision만 기록한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_rag_quality_promotion_decision_gate.py -q
python scripts\rag_quality_promotion_decision_gate.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. result가 promote/defer/rollback 중 하나인지 확인
3. `phases/rag-quality-fresh-validation/index.json` step 업데이트

## 금지사항

- 사용자 explicit authorization 없이 default retriever를 변경하지 마라.
