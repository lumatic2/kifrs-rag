# Step 4: 1115-statement-draft-pilot

Status: pending

## 읽어야 할 파일

- `phases/financial-statement-draft/step2.md` — 왜: 공통 statement draft schema와 adapter가 만들어진 상태를 이어받는다.
- `phases/financial-statement-draft/step3.md` — 왜: FS3에서 후속 source를 review pack에 보존한 패턴을 참고한다.
- `kifrs/workflows/statement_draft/adapters.py` — 왜: 1115 adapter를 pilot 수준으로 확장할 위치다.
- `kifrs/workflows/kifrs1115/measurement.py` — 왜: recognized/deferred/financing/repurchase 금액 source.
- `kifrs/workflows/kifrs1115/journal_entry.py` — 왜: 수익/계약부채/금융부채/금융비용 표시 후보 source.
- `tests/test_statement_draft.py` — 왜: FS4 1115 pilot 기대값을 추가한다.

## 작업

1115 statement draft adapter를 pilot 수준으로 확장한다. material right, significant financing,
repurchase financing arrangement에서 수익, 계약부채, 매출채권, 이연금융수익, 금융부채, 금융비용 후보가
명확히 나오도록 한다.

## Acceptance Criteria

```powershell
python -m pytest tests/test_statement_draft.py tests/test_workflow_1115.py tests/test_1115_review_pack.py
git diff --check
```

## 금지사항

- 1115 판단 path를 새로 늘리지 않는다. 이유: FS4는 표시 pilot이지 revenue engine 확장이 아니다.
- 계약 원문 검토, SSP 확률 검증, 지급조건 판단을 자동 확정하지 않는다.
