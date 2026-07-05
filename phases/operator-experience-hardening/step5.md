# Step 5: Operator Experience Close Gate

## 읽어야 할 파일
- docs/reports/2026-07-05-oeh1-operator-command-inventory.md — 왜: command discovery evidence다.
- docs/reports/2026-07-05-oeh2-run-doctor.md — 왜: diagnostics evidence다.
- docs/reports/2026-07-05-oeh3-report-manifest.md — 왜: navigation evidence다.
- docs/reports/2026-07-05-oeh4-error-recovery-playbook.md — 왜: recovery evidence다.
- docs/reports/2026-07-05-runtime-retriever-promotion-gate-close-report.md — 왜: 직전 horizon close evidence다.

## 작업
operator가 discover, run, verify, recover를 하나의 documented surface로 할 수 있는지 close gate를 구현한다.

## Acceptance Criteria
```bash
python -m pytest tests\test_operator_experience_close_gate.py -q
python scripts\operator_experience_close_gate.py --format text --write
```

## 검증 절차
1. AC 커맨드 실행.
2. ROADMAP, horizon doc, phase index를 completed로 갱신한다.
3. 1~5 제품 약점 horizon queue 완료 상태를 반영한다.

## 금지사항
- SaaS packaging이나 외부 outreach를 이 horizon에 끼워 넣지 마라.
