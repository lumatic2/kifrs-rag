# Step 5: cross-domain-disclosure-report

Status: completed (2026-07-05)

## 읽어야 할 파일

- `docs/reports/2026-07-05-dg1-disclosure-surface-inventory.md` — 왜: DG1의 surface 비교.
- `kifrs/workflows/disclosure/` — 왜: DG2 common schema와 adapter.
- `kifrs/workflows/kifrs1115/disclosure.py` — 왜: DG3 pilot.
- `kifrs/workflows/kifrs1109/disclosure.py` — 왜: DG4 pilot.

## 작업

1116/1115/1109 disclosure surface의 자동화 가능성과 NeedsHumanReview 경계를 비교 리포트로 남긴다.

## Acceptance Criteria

```powershell
python -m pytest tests/test_disclosure_common.py tests/test_1115_disclosure.py tests/test_1109_disclosure.py
git diff --check
```

## 결과

- Cross-domain report: `docs/reports/2026-07-05-dg5-cross-domain-disclosure-report.md`.
- 다음 sequence를 `f-acc-1109-hardening`으로 넘긴다.
