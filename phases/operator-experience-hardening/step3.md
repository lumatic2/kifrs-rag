# Step 3: Report Manifest And Navigation Surface

## 읽어야 할 파일
- docs/reports/2026-07-05-oeh1-operator-command-inventory.md — 왜: manifest에 연결할 command/report map이다.
- docs/reports/2026-07-05-oeh2-run-doctor.md — 왜: manifest의 preflight 항목이다.

## 작업
operator가 ROADMAP 내부를 읽지 않고도 핵심 reports를 순서대로 열 수 있는 manifest/navigation report를 만든다.

## Acceptance Criteria
```bash
python -m pytest tests\test_operator_report_manifest.py -q
python scripts\operator_report_manifest.py --format text --write
```

## 검증 절차
1. AC 커맨드 실행.
2. manifest가 phase별 핵심 리포트, 추천 읽기 순서, missing hint를 포함하는지 확인.
3. phase index step 3 상태를 completed로 갱신한다.

## 금지사항
- manifest에 protected body, private payload, embedding dump 경로를 넣지 마라.
