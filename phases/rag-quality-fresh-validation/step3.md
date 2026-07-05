# Step 3: Opt-In Retriever Regression Matrix

## 읽어야 할 파일

- `docs/reports/2026-07-05-rqf1-validation-contract.md` - 왜: comparison criteria다.
- `docs/reports/2026-07-05-rqf2-baseline-snapshot.md` - 왜: opt-in retriever comparison 기준점이다.

## 작업

opt-in repair retriever를 baseline과 비교하는 regression matrix를 만든다. 품질, latency, rollback evidence를 분리해 기록한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_rag_quality_regression_matrix.py -q
python scripts\rag_quality_regression_matrix.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. regression과 latency가 각각 보고되는지 확인
3. `phases/rag-quality-fresh-validation/index.json` step 업데이트

## 금지사항

- optimistic pass만으로 promote를 제안하지 마라.
