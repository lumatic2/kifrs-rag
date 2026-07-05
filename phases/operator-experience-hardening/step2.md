# Step 2: Run Doctor And Environment Checks

## 읽어야 할 파일
- docs/reports/2026-07-05-oeh1-operator-command-inventory.md — 왜: doctor가 검사할 command/report surface를 이어받는다.
- CLAUDE.md — 왜: protected data boundary와 로컬 실행 규칙을 확인한다.

## 작업
Python, uv, 필수 디렉터리, protected-data boundary, 핵심 리포트 존재 여부를 점검하는 run doctor를 구현한다.

## Acceptance Criteria
```bash
python -m pytest tests\test_operator_run_doctor.py -q
python scripts\operator_run_doctor.py --format text --write
```

## 검증 절차
1. AC 커맨드 실행.
2. missing report hints와 protected boundary checks가 있는지 확인.
3. phase index step 2 상태를 completed로 갱신한다.

## 금지사항
- doctor가 private DB, embedding, dogfood 자료 내용을 읽거나 출력하지 않게 하라.
