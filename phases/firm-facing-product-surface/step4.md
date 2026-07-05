# Step 4: Product Narrative README

## Result

FPS4 refreshed README around the firm-facing local demo and added a narrative checker.

## Evidence

- `README.md`
- `scripts/firm_facing_product_narrative.py`
- `tests/test_firm_facing_product_narrative.py`
- `docs/reports/2026-07-05-fps4-product-narrative.md`

## Acceptance Criteria

```powershell
python -m pytest tests\test_firm_facing_product_narrative.py -q
python scripts\firm_facing_product_narrative.py --format text --write
```
