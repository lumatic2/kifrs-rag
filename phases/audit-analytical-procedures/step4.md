# Step 4: f-acc-output-linkage

Status: completed

## 읽어야 할 파일

- `phases/audit-analytical-procedures/step3.md` — 왜: anomaly finding과 renderer가 만들어진 상태를 이어받는다.
- `kifrs/workflows/audit_analytics/metrics.py` — 왜: finding의 linked statement candidates를 F-ACC output과 연결할 위치다.
- `kifrs/workflows/statement_draft/schema.py` — 왜: F-ACC output linkage 대상 schema다.
- `tests/test_audit_analytics.py` — 왜: AP4 linkage test를 추가한다.

## 작업

`AnomalyFinding.linked_statement_candidates`와 `StatementLineCandidate`를 연결하는 helper를 추가한다. 예:
부채비율 상승 finding은 리스부채/금융부채/계약부채 candidate와 연결되고, 수익 관련 finding은 수익/계약부채
candidate와 연결된다.

## Acceptance Criteria

```powershell
python -m pytest tests/test_audit_analytics.py tests/test_statement_draft.py
git diff --check
```

## 금지사항

- 연결을 감사 결론으로 승격하지 않는다. 이유: linkage는 추가 검토 후보를 묶는 기능이다.
- F-ACC statement candidate schema를 깨지 않는다.

## 완료 요약

`LinkedStatementCandidate`와 `link_statement_candidates()`를 추가했다. audit finding의 연결 후보명과
F-ACC `StatementLineCandidate.line_item`을 매칭해, 예를 들어 부채비율 상승 finding을 1115 금융부채
candidate와 연결한다. 연결은 감사 결론이 아니라 추가 검토 link로 유지한다.
`tests/test_audit_analytics.py tests/test_statement_draft.py` 14개가 통과했다.
