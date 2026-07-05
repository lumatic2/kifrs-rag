# Step 2: Realistic Local Fixture Adapter Contract

## 읽어야 할 파일

- `phases/private-parser-realism-hardening/index.json` - 왜: PPR1 완료 summary를 이어받는다.
- `docs/reports/2026-07-05-ppr1-authorization-safe-adapter-proof.md` - 왜: adapter contract의 authorization boundary다.

## 작업

지원할 local fixture file class와 structured output contract를 정의한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_private_parser_fixture_adapter_contract.py -q
python scripts\private_parser_fixture_adapter_contract.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. failure/redaction states가 명시됐는지 확인
3. phase index 업데이트

## 금지사항

- actual protected file parser를 구현했다고 주장하지 마라.
