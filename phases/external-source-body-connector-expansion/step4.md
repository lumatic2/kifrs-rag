# Step 4: Connector Leak And Policy Gate

## 읽어야 할 파일

- `docs/reports/2026-07-05-esb2-source-body-fixture-contract.md` - 왜: policy leak 기준이다.
- `docs/reports/2026-07-05-esb3-chunk-retrieval-dry-run.md` - 왜: scan 대상 report다.

## 작업

connector public reports가 protected body text나 secret을 노출하지 않는지 gate를 만든다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_external_source_body_connector_leak_gate.py -q
python scripts\external_source_body_connector_leak_gate.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. synthetic negative cases만 사용했는지 확인
3. phase index 업데이트

## 금지사항

- blocked marker 원문을 machine result에 공개하지 마라.
