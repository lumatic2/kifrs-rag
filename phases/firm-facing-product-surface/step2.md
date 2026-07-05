# Step 2: Operator Demo Command

## Result

FPS2 added one operator command that renders the recommended 1116 firm-facing walkthrough packet.

## Evidence

- `scripts/firm_facing_operator_demo_command.py`
- `tests/test_firm_facing_operator_demo_command.py`
- `docs/reports/2026-07-05-fps2-operator-demo-command.md`

## Acceptance Criteria

```powershell
python -m pytest tests\test_firm_facing_operator_demo_command.py -q
python scripts\firm_facing_operator_demo_command.py --format text --write
```
