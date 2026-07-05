# Step 2: Demo Run Quality Checklist

## 읽어야 할 파일

- `docs/reports/2026-07-05-drq1-demo-rehearsal-script.md` - 왜: quality checklist의 stage source다.

## 작업

각 demo stage의 pass/fail checks, failure notes, recovery route를 정의한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_demo_run_quality_checklist.py -q
python scripts\demo_run_quality_checklist.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. failure/recovery path가 stage별로 존재하는지 확인
3. phase index 업데이트

## 금지사항

- 성공 경로만 있는 checklist를 만들지 마라.
