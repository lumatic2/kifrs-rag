# Step 5: analytical-procedure-report

Status: pending

## 읽어야 할 파일

- `phases/audit-analytical-procedures/step1.md` — 왜: scope와 excluded audit 책임 경계.
- `phases/audit-analytical-procedures/step2.md` — 왜: metric schema/runner 구현 요약.
- `phases/audit-analytical-procedures/step3.md` — 왜: anomaly finding/note 구현 요약.
- `phases/audit-analytical-procedures/step4.md` — 왜: F-ACC linkage 구현 요약.
- `tests/test_audit_analytics.py` — 왜: completion evidence.
- `docs/horizons/f-audit-analytical-procedures.md` — 왜: horizon goal과 boundary.

## 작업

F-AUD analytical procedures horizon completion report를 작성한다. 계산표, 이상징후 메모, F-ACC linkage가
무엇을 자동화했고 감사 책임 영역은 무엇으로 남는지 정리한다.

## Acceptance Criteria

```powershell
python -m pytest tests/test_audit_analytics.py tests/test_statement_draft.py
git diff --check
```

## 결과물

- `docs/reports/2026-07-05-ap5-analytical-procedure-report.md`
