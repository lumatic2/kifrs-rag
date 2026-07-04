# Step AF1: Horizon and Plan Setup

## 읽어야 할 파일

- `docs/OBJECTIVE.md` - 왜: 실제 회계사 피드백 반영이 objective의 중간 관문임을 확인한다.
- `ROADMAP.md` - 왜: 직전 `real-anonymized-transaction-poc` 다음 추천 horizon을 active로 전환한다.
- `docs/reports/2026-07-05-ra4-real-transaction-poc-close-report.md` - 왜: 직전 horizon의 queue sample과 다음 추천을 이어받는다.

## 작업

`accountant-feedback-incorporation` horizon, plan, phase files를 만든다.

## Acceptance Criteria

```powershell
Test-Path docs\horizons\accountant-feedback-incorporation.md
Test-Path docs\plans\2026-07-05-accountant-feedback-incorporation.md
Test-Path phases\accountant-feedback-incorporation\index.json
```

## 검증 절차

1. AC 커맨드를 실행한다.
2. ROADMAP/OBJECTIVE가 active horizon을 가리키는지 확인한다.
3. AF1을 completed로 업데이트한다.

## 금지사항

- 실제 피드백이 없는데 "회계사가 검증했다"고 표현하지 않는다.
