# Step 3: Readiness Checklist

## Result

FPS3 added the local install/run path and protected-data boundary checklist.

## Evidence

- `scripts/firm_facing_readiness_checklist.py`
- `tests/test_firm_facing_readiness_checklist.py`
- `docs/reports/2026-07-05-fps3-readiness-checklist.md`

## Acceptance Criteria

```powershell
python -m pytest tests\test_firm_facing_readiness_checklist.py -q
python scripts\firm_facing_readiness_checklist.py --format text --write
```
