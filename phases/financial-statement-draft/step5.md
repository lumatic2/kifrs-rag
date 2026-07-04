# Step 5: fs-draft-report

Status: pending

## 읽어야 할 파일

- `docs/reports/2026-07-05-fs1-statement-draft-surface-inventory.md` — 왜: F/S draft surface inventory 결론.
- `phases/financial-statement-draft/step2.md` — 왜: 공통 schema/adapters 구현 요약.
- `phases/financial-statement-draft/step3.md` — 왜: 1109 pilot 구현 요약.
- `phases/financial-statement-draft/step4.md` — 왜: 1115 pilot 구현 요약.
- `tests/test_statement_draft.py` — 왜: 자동화 증거와 남은 경계 확인.
- `docs/horizons/f-acc-financial-statement-draft.md` — 왜: horizon 목표와 boundary.

## 작업

F/S draft horizon completion report를 작성한다. 무엇이 자동화됐고, 무엇이 아직 회사별 TB/mapping/human
review boundary로 남는지 쉽게 설명한다.

## Acceptance Criteria

```powershell
python -m pytest tests/test_statement_draft.py tests/test_disclosure_common.py tests/test_1109_review_pack.py tests/test_1115_review_pack.py tests/test_1116_review_pack.py
git diff --check
```

## 결과물

- `docs/reports/2026-07-05-fs5-statement-draft-report.md`
