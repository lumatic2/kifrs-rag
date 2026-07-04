# Step FC1: Horizon and Plan Setup

## 읽어야 할 파일

- `docs/OBJECTIVE.md` - 왜: 회계사 실제 피드백이 중간 관문임을 확인한다.
- `ROADMAP.md` - 왜: 직전 runbook 다음 추천 horizon을 active로 전환한다.
- `docs/reports/field-feedback-runbook/2026-07-05-30min-session-runbook.md` - 왜: capture notes template을 이어받는다.

## 작업

`field-feedback-capture` horizon, plan, phase files를 만든다.

## Acceptance Criteria

```powershell
Test-Path docs\horizons\field-feedback-capture.md
Test-Path docs\plans\2026-07-05-field-feedback-capture.md
Test-Path phases\field-feedback-capture\index.json
```

## 검증 절차

1. AC 커맨드를 실행한다.
2. ROADMAP/OBJECTIVE가 active horizon을 가리키는지 확인한다.
3. FC1을 completed로 업데이트한다.

## 금지사항

- 실제 피드백을 받지 않았는데 완료 증거로 표현하지 않는다.
