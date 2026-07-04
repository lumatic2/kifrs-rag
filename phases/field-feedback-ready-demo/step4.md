# FF4 — Feedback Package Smoke and Close

## Objective

field feedback package를 닫는다. demo command, demo bundle, brief, questionnaire, known limitations를 한 번에
찾을 수 있는 index를 만들고 smoke 검증을 실행한다.

## 읽어야 할 파일

- `docs/reports/field-feedback/2026-07-05-demo-brief.md` — 왜: package index의 brief 링크.
- `docs/reports/field-feedback/2026-07-05-feedback-questionnaire.md` — 왜: package index의 질문지 링크.
- `docs/reports/field-feedback/2026-07-05-known-limitations.md` — 왜: package index의 경계 문서 링크.
- `docs/reports/demo-poc/MANIFEST.md` — 왜: demo bundle link.
- `docs/reports/2026-07-05-rt5-runtime-close-demo.md` — 왜: upstream runtime evidence demo close evidence.

## 작업

1. `docs/reports/field-feedback/INDEX.md`를 작성한다.
2. `docs/reports/2026-07-05-ff4-feedback-package-close-report.md`를 작성한다.
3. demo command와 문서 존재/핵심 문구 검증을 실행한다.
4. ROADMAP과 phase index를 close 상태로 갱신한다.

## Acceptance Criteria

```powershell
python scripts\demo_poc.py --scenario revenue-financing --out docs\reports\demo-poc
python -m pytest tests\test_demo_poc.py tests\test_answer_boundary.py tests\test_statement_draft.py -q
Test-Path docs\reports\field-feedback\INDEX.md
Test-Path docs\reports\field-feedback\2026-07-05-demo-brief.md
Test-Path docs\reports\field-feedback\2026-07-05-feedback-questionnaire.md
Test-Path docs\reports\field-feedback\2026-07-05-known-limitations.md
python scripts\quality_preflight.py --format text
git diff --check
```

## Deliverable

- `docs/reports/field-feedback/INDEX.md`
- `docs/reports/2026-07-05-ff4-feedback-package-close-report.md`
- `ROADMAP.md`
- `phases/field-feedback-ready-demo/index.json`

## 금지사항

- 피드백 패키지를 도입 제안서처럼 과장하지 않는다.
- 회계사 피드백을 받기 전 PoC 성과를 확정된 것처럼 쓰지 않는다.

