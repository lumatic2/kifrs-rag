# Step 5: Horizon Close And Next Gap Handoff

## 읽어야 할 파일

- `docs/reports/2026-07-05-rqf1-validation-contract.md` - 왜: validation contract evidence다.
- `docs/reports/2026-07-05-rqf2-baseline-snapshot.md` - 왜: baseline evidence다.
- `docs/reports/2026-07-05-rqf3-regression-matrix.md` - 왜: regression evidence다.
- `docs/reports/2026-07-05-rqf4-promotion-decision.md` - 왜: final retriever decision evidence다.

## 작업

RAG quality fresh validation horizon을 close하고 다음 objective-gap horizon을 지정한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_rag_quality_fresh_validation_close_gate.py -q
python scripts\rag_quality_fresh_validation_close_gate.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. ROADMAP/OBJECTIVE/phase 상태를 close 결과와 동기화한다
3. `phases/rag-quality-fresh-validation/index.json` step 업데이트

## 금지사항

- close gate가 실패했는데 ROADMAP을 완료로 바꾸지 마라.
