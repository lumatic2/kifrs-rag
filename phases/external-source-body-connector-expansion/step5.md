# Step 5: Horizon Close And Workflow Coverage Handoff

## 읽어야 할 파일

- `docs/reports/2026-07-05-esb1-source-body-connector-selection.md` - 왜: source selection evidence다.
- `docs/reports/2026-07-05-esb2-source-body-fixture-contract.md` - 왜: fixture contract evidence다.
- `docs/reports/2026-07-05-esb3-chunk-retrieval-dry-run.md` - 왜: dry-run evidence다.
- `docs/reports/2026-07-05-esb4-connector-leak-policy-gate.md` - 왜: leak/policy evidence다.

## 작업

external source-body connector expansion horizon을 close하고 다음 objective-gap horizon을 지정한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_external_source_body_connector_expansion_close_gate.py -q
python scripts\external_source_body_connector_expansion_close_gate.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. ROADMAP/OBJECTIVE/phase 상태를 close 결과와 동기화한다
3. phase index 업데이트

## 금지사항

- close gate가 실패했는데 ROADMAP을 완료로 바꾸지 마라.
