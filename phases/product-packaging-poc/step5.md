# Step 5: demo-brief-feedback-questionnaire

Status: pending

## 읽어야 할 파일

- `docs/reports/2026-07-05-pk1-demo-scenario-selection.md` — 왜: 10분 demo 구성과 선택 근거.
- `docs/reports/demo-poc/MANIFEST.md` — 왜: demo output bundle 구조.
- `README.md` — 왜: setup/demo 실행 안내.
- `docs/horizons/product-packaging-poc.md` — 왜: horizon 목표와 boundary.

## 작업

회계법인 소개용 10분 demo brief와 회계사 피드백 질문지를 작성한다. 제품이 무엇을 자동화했고 무엇을
사람 검토로 남기는지 결정사항까지 분명히 적는다.

## Acceptance Criteria

```powershell
python -m pytest tests/test_demo_poc.py tests/test_audit_analytics.py tests/test_statement_draft.py
git diff --check
```

## 결과물

- `docs/reports/2026-07-05-pk5-demo-brief-feedback.md`
