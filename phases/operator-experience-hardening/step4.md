# Step 4: Error Recovery Playbook

## 읽어야 할 파일
- docs/reports/2026-07-05-oeh2-run-doctor.md — 왜: doctor failure를 recovery case로 연결한다.
- docs/reports/2026-07-05-oeh3-report-manifest.md — 왜: navigation failure를 recovery case로 연결한다.

## 작업
일반적인 실패를 rerun/remediation command로 연결하는 recovery playbook/checker를 만든다.

## Acceptance Criteria
```bash
python -m pytest tests\test_operator_error_recovery.py -q
python scripts\operator_error_recovery.py --format text --write
```

## 검증 절차
1. AC 커맨드 실행.
2. recovery cases가 pytest failure, missing report, default retriever guard failure, protected data warning을 포함하는지 확인.
3. phase index step 4 상태를 completed로 갱신한다.

## 금지사항
- recovery가 destructive cleanup이나 git reset을 제안하지 않게 하라.
