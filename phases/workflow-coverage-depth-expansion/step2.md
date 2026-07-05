# Step 2: Workflow Sample Contract Pack

## 읽어야 할 파일

- `docs/reports/2026-07-05-wcd1-service-line-coverage-rerank.md` - 왜: sample contract 후보의 우선순위다.

## 작업

선택된 workflow samples의 input facts, authority needs, output surface, review boundary, failure states를 계약으로 정의한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_workflow_sample_contract_pack.py -q
python scripts\workflow_sample_contract_pack.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. public-safe fixture/metadata만 쓰는지 확인
3. phase index 업데이트

## 금지사항

- protected client payload를 sample input으로 넣지 마라.
