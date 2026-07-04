# FF2 — Feedback Questionnaire Refresh

## Objective

회계사가 demo를 본 뒤 바로 답할 수 있는 피드백 질문지를 작성한다. 질문은 정확성, 유용성, 검토 부담,
위험, 다음 PoC 후보로 나눈다.

## 읽어야 할 파일

- `docs/reports/field-feedback/2026-07-05-demo-brief.md` — 왜: 질문지가 참조할 demo flow.
- `docs/reports/2026-07-05-pk5-demo-brief-feedback.md` — 왜: 기존 질문지의 출발점.
- `docs/reports/demo-poc/evidence-boundary.md` — 왜: external evidence 관련 질문 필요.
- `docs/reports/demo-poc/statement-candidates.md` — 왜: F/S candidate와 evidence column 질문 필요.

## 작업

1. `docs/reports/field-feedback/2026-07-05-feedback-questionnaire.md`를 작성한다.
2. 질문을 다섯 섹션으로 나눈다.
   - 정확성/근거
   - 실무 유용성
   - 검토 부담
   - 위험/통제
   - 다음 PoC 후보
3. 회계사가 답하기 쉽게 점수형 질문과 서술형 질문을 섞는다.
4. evidence boundary와 synthetic fact에 대한 질문을 포함한다.

## Acceptance Criteria

```powershell
Test-Path docs\reports\field-feedback\2026-07-05-feedback-questionnaire.md
Select-String -Path docs\reports\field-feedback\2026-07-05-feedback-questionnaire.md -Pattern "정확성"
Select-String -Path docs\reports\field-feedback\2026-07-05-feedback-questionnaire.md -Pattern "synthetic"
Select-String -Path docs\reports\field-feedback\2026-07-05-feedback-questionnaire.md -Pattern "다음 PoC"
git diff --check
```

## Deliverable

- `docs/reports/field-feedback/2026-07-05-feedback-questionnaire.md`

## 금지사항

- 도입 여부를 묻는 영업 질문으로 흐르지 않는다.
- 피드백을 "좋다/나쁘다" 수준으로만 받지 않는다.

