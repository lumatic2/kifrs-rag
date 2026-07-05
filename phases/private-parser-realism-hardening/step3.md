# Step 3: Deletion And Retention Rehearsal

## 읽어야 할 파일

- `docs/reports/2026-07-05-ppr2-fixture-adapter-contract.md` - 왜: deletion rehearsal 대상 artifact states다.

## 작업

local artifact lifecycle을 retained/deleted evidence states로 rehearsal한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_private_parser_deletion_retention_rehearsal.py -q
python scripts\private_parser_deletion_retention_rehearsal.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. retained/deleted 상태가 public-safe인지 확인
3. phase index 업데이트

## 금지사항

- 실제 사용자 파일을 삭제했다고 주장하지 마라.
