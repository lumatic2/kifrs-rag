# Step 2: Synthetic Source-Body Fixture Contract

## 읽어야 할 파일

- `docs/reports/2026-07-05-esb1-source-body-connector-selection.md` - 왜: fixture contract의 policy boundary다.

## 작업

synthetic/authorized source-body fixture input과 parser/chunker output schema를 정의한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_external_source_body_fixture_contract.py -q
python scripts\external_source_body_fixture_contract.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. raw body publication rule이 금지로 명시됐는지 확인
3. phase index 업데이트

## 금지사항

- 실제 source body를 fixture로 커밋하지 마라.
