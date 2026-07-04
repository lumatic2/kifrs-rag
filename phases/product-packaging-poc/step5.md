# Step 5: demo-brief-feedback-questionnaire

Status: completed

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

## 완료 요약

10분 demo script와 회계사 피드백 질문지를 작성했다. demo는 1115 수익인식, F/S 표시 후보, audit analytics
linkage, 1116 lease card를 보여주며, 기준서 원문/DB/embedding 비배포와 회계사 검토 책임을 명시한다.
`tests/test_demo_poc.py tests/test_audit_analytics.py tests/test_statement_draft.py` 16개와 `git diff --check`가 통과했다.
