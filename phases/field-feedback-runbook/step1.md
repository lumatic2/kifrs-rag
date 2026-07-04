# Step FB1: Horizon and Plan Setup

## 읽어야 할 파일

- `docs/OBJECTIVE.md` - 왜: 회계사 피드백이 중간 관문임을 확인한다.
- `ROADMAP.md` - 왜: 직전 `accountant-feedback-incorporation` 다음 추천 horizon을 active로 전환한다.
- `docs/reports/2026-07-05-af4-accountant-feedback-incorporation-close-report.md` - 왜: runbook에 묶을 최신 피드백 루프를 확인한다.

## 작업

`field-feedback-runbook` horizon, plan, phase files를 만든다.

## Acceptance Criteria

```powershell
Test-Path docs\horizons\field-feedback-runbook.md
Test-Path docs\plans\2026-07-05-field-feedback-runbook.md
Test-Path phases\field-feedback-runbook\index.json
```

## 검증 절차

1. AC 커맨드를 실행한다.
2. ROADMAP/OBJECTIVE가 active horizon을 가리키는지 확인한다.
3. FB1을 completed로 업데이트한다.

## 금지사항

- 실제 회계사 피드백을 이미 받은 것처럼 표현하지 않는다.
