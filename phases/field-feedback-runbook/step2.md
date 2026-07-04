# Step FB2: Session Runbook

## 읽어야 할 파일

- `docs/reports/firm-facing-poc/2026-07-05-one-page-brief.md` - 왜: 10분 소개와 30분 demo 흐름의 시작점이다.
- `docs/reports/demo-poc/MANIFEST.md` - 왜: demo bundle 파일 순서를 확인한다.
- `docs/reports/real-transaction-poc/INDEX.md` - 왜: 익명화 거래 sample 흐름을 포함한다.
- `docs/reports/2026-07-05-af3-feedback-incorporation-report.md` - 왜: correction이 action plan으로 이어지는 모습을 보여준다.
- `docs/reports/field-feedback/2026-07-05-feedback-questionnaire.md` - 왜: 세션 중 기록할 질문지다.
- `docs/reports/field-feedback/2026-07-05-incorporated-review-questions.md` - 왜: 추가 review question supplement다.

## 작업

30분 회계사 피드백 세션 runbook과 operator checklist를 작성한다.

## Acceptance Criteria

```powershell
Test-Path docs\reports\field-feedback-runbook\2026-07-05-30min-session-runbook.md
Test-Path docs\reports\field-feedback-runbook\2026-07-05-operator-checklist.md
```

## 검증 절차

1. AC 커맨드를 실행한다.
2. runbook이 사전 준비, 타임라인, 질문, 사후 처리, boundary를 포함하는지 확인한다.
3. FB2를 completed로 업데이트한다.

## 금지사항

- 기준서 원문, DB, 임베딩, 고객자료 업로드를 요구하지 않는다.
