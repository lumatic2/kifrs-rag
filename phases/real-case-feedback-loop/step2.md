# Step RC2: Reviewer Correction Capture

## 읽어야 할 파일

- `kifrs/feedback/case_intake.py` - 왜: correction이 어떤 case id와 domain에 붙는지 확인한다.
- `docs/reports/field-feedback/2026-07-05-feedback-questionnaire.md` - 왜: 기존 field feedback 질문 축을 structured correction으로 연결한다.

## 작업

회계사 피드백을 `ReviewerCorrection`으로 구조화한다. correction은 issue, severity, suggested_fix,
missing_evidence, disposition(eval_seed/backlog/no_action)을 포함한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_real_case_feedback.py -q
```

## 검증 절차

1. AC 커맨드를 실행한다.
2. correction에 raw source body를 넣을 수 없는지 확인한다.
3. RC2를 completed로 업데이트한다.

## 금지사항

- reviewer correction을 최종 회계 판단으로 표현하지 않는다.
- 원문 body나 고객 식별자를 correction에 저장하지 않는다.
