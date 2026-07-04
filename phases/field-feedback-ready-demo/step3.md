# FF3 — Known Limitations and Human-Review Boundary

## Objective

회계사 피드백 전에 demo의 한계와 사람 검토 경계를 명확히 문서화한다. 외부 evidence, synthetic fact,
review pack, statement draft, audit analytics가 무엇을 의미하고 무엇을 의미하지 않는지 분리한다.

## 읽어야 할 파일

- `docs/reports/field-feedback/2026-07-05-demo-brief.md` — 왜: brief에서 설명한 경계와 일관되어야 함.
- `docs/reports/field-feedback/2026-07-05-feedback-questionnaire.md` — 왜: 질문지의 위험/통제 문항과 연결.
- `docs/reports/demo-poc/evidence-boundary.md` — 왜: external evidence boundary 실제 출력.
- `docs/reports/2026-07-05-rt5-runtime-close-demo.md` — 왜: deliberately out-of-scope 항목.

## 작업

1. `docs/reports/field-feedback/2026-07-05-known-limitations.md`를 작성한다.
2. 항목을 다음으로 나눈다.
   - 데이터/저작권 경계
   - 판단 책임 경계
   - external evidence 경계
   - synthetic fact 경계
   - audit analytics 경계
   - 다음 PoC에서 확인할 것
3. 회계사에게 피드백 요청 전 먼저 읽힐 수 있게 짧고 명확하게 쓴다.

## Acceptance Criteria

```powershell
Test-Path docs\reports\field-feedback\2026-07-05-known-limitations.md
Select-String -Path docs\reports\field-feedback\2026-07-05-known-limitations.md -Pattern "회계사 검토"
Select-String -Path docs\reports\field-feedback\2026-07-05-known-limitations.md -Pattern "synthetic"
Select-String -Path docs\reports\field-feedback\2026-07-05-known-limitations.md -Pattern "외부 evidence"
git diff --check
```

## Deliverable

- `docs/reports/field-feedback/2026-07-05-known-limitations.md`

## 금지사항

- 한계를 숨기지 않는다.
- "검토 시간을 줄일 수 있음"을 "검토가 필요 없음"으로 표현하지 않는다.

