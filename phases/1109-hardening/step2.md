# Step 2: sppi-reset-nuance-hardening

Status: completed (2026-07-05)

## 읽어야 할 파일

- `kifrs/workflows/kifrs1109/schema.py` — 왜: reset mismatch 구조화 입력을 추가한다.
- `kifrs/workflows/kifrs1109/sppi.py` — 왜: SPPI 판단 로직을 확장한다.
- `kifrs/workflows/kifrs1109/fixtures.py` — 왜: scenario_06을 special_case에서 automated로 승격한다.

## 작업

변동금리 재설정 주기와 기준금리 테너 불일치 케이스를 구조화 입력으로 처리하고, benchmark cash flow 비교상
유의적 변형이 없으면 SPPI Pass로 분류한다.

## Acceptance Criteria

```powershell
python -m pytest tests/test_workflow_1109.py tests/test_workflow_1109_regression.py tests/test_1109_review_pack.py
git diff --check
```

## 결과

- scenario_06이 AC automated review pack으로 승격.
- 1109 automated fixture: 6/10 → 7/10.
- report: `docs/reports/2026-07-05-fh2-sppi-reset-hardening.md`.
