# Step 2: ratio-trend-schema

Status: completed

## 읽어야 할 파일

- `docs/reports/2026-07-05-ap1-analytical-procedure-scope-inventory.md` — 왜: AP2 schema와 fixture 범위가 정리되어 있다.
- `docs/reports/2026-07-05-fs5-statement-draft-report.md` — 왜: AP4에서 연결할 F-ACC statement candidate 경계를 확인한다.
- `kifrs/workflows/statement_draft/schema.py` — 왜: 기존 공통 dataclass 스타일을 따른다.
- `tests/test_statement_draft.py` — 왜: workflow-level test 스타일과 fixture 위치를 참고한다.

## 작업

`kifrs/workflows/audit_analytics/`에 synthetic F/S fixture, line schema, ratio/trend metric 계산 runner를
추가한다. AP2는 anomaly note 문서화 전 단계이므로 finding renderer는 만들지 않는다.

## Acceptance Criteria

```powershell
python -m pytest tests/test_audit_analytics.py
git diff --check
```

## 금지사항

- DART API나 외부 파일을 읽지 않는다. 이유: AP2는 no-credential deterministic 계산 surface다.
- 감사의견, 중요성, KAM, sampling 판단을 만들지 않는다.

## 완료 요약

`kifrs/workflows/audit_analytics/`에 synthetic F/S fixture, `FinancialStatementLine`,
`AnalyticalProcedureInput`, `AnalyticalMetric`, `calculate_metrics()`를 추가했다. line item별 증감과
매출총이익률, 영업이익률, 유동비율, 부채비율을 deterministic하게 계산한다.
`tests/test_audit_analytics.py` 4개가 통과했다.
