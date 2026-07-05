# Step 4: Parser Leak And Public Report Gate

## 읽어야 할 파일

- `docs/reports/2026-07-05-ppr2-fixture-adapter-contract.md` - 왜: public report schema 기준이다.
- `docs/reports/2026-07-05-ppr3-deletion-retention-rehearsal.md` - 왜: artifact lifecycle evidence다.

## 작업

public report leak gate를 만들고 synthetic negative cases로 protected content가 출력되지 않는지 확인한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_private_parser_public_report_leak_gate.py -q
python scripts\private_parser_public_report_leak_gate.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. negative cases가 실제 private payload가 아니라 synthetic markers인지 확인
3. phase index 업데이트

## 금지사항

- protected content를 테스트 fixture로 커밋하지 마라.
