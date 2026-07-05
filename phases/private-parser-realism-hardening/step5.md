# Step 5: Horizon Close And Source Connector Handoff

## 읽어야 할 파일

- `docs/reports/2026-07-05-ppr1-authorization-safe-adapter-proof.md` - 왜: authorization proof evidence다.
- `docs/reports/2026-07-05-ppr2-fixture-adapter-contract.md` - 왜: adapter contract evidence다.
- `docs/reports/2026-07-05-ppr3-deletion-retention-rehearsal.md` - 왜: lifecycle evidence다.
- `docs/reports/2026-07-05-ppr4-public-report-leak-gate.md` - 왜: leak gate evidence다.

## 작업

private parser realism hardening horizon을 close하고 다음 objective-gap horizon을 지정한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_private_parser_realism_close_gate.py -q
python scripts\private_parser_realism_close_gate.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. ROADMAP/OBJECTIVE/phase 상태를 close 결과와 동기화한다
3. phase index 업데이트

## 금지사항

- close gate가 실패했는데 ROADMAP을 완료로 바꾸지 마라.
