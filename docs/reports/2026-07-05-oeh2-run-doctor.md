# OEH2 Run Doctor

> Scope: local operator diagnostics for environment, reports, and protected boundaries.

## 한 줄 결론

The run doctor checks Python, uv availability, required public reports, and protected-data boundaries without reading private payloads.

## Environment

- Python: `3.12.10`
- uv available: True

## Required Reports

| Report | Path | Exists | Hint |
|---|---|---|---|
| command_inventory | `docs/reports/2026-07-05-oeh1-operator-command-inventory.md` | True | `python scripts\operator_command_inventory.py --format text --write` |
| progress_map | `docs/reports/2026-07-05-accounting-intelligence-progress-map.md` | True | `python scripts\accounting_intelligence_progress_map.py --format text --write` |
| weakness_queue | `docs/reports/2026-07-05-product-weakness-horizon-candidates.md` | True | `python scripts\product_weakness_horizon_candidates.py --format text --write` |
| retriever_close | `docs/reports/2026-07-05-runtime-retriever-promotion-gate-close-report.md` | True | `python scripts\runtime_retriever_promotion_close_gate.py --format text --write` |

## Protected Boundaries

| Boundary | OK |
|---|---|
| no_private_payload_scan | True |
| no_embedding_dump_scan | True |
| no_dogfood_material_scan | True |
| public_reports_only | True |

## Warnings

- none

## Checks

| Check | OK |
|---|---|
| python_available | True |
| uv_checked | True |
| required_reports_checked | True |
| required_reports_present | True |
| protected_boundaries_checked | True |

## Errors

- none

## Machine Result

```json
{
  "title": "OEH2 Run Doctor",
  "ok": true,
  "horizon": "operator-experience-hardening",
  "completed_milestone": "OEH2",
  "python_version": "3.12.10",
  "uv_available": true,
  "reports": {
    "command_inventory": {
      "path": "docs/reports/2026-07-05-oeh1-operator-command-inventory.md",
      "exists": true,
      "hint": "python scripts\\operator_command_inventory.py --format text --write"
    },
    "progress_map": {
      "path": "docs/reports/2026-07-05-accounting-intelligence-progress-map.md",
      "exists": true,
      "hint": "python scripts\\accounting_intelligence_progress_map.py --format text --write"
    },
    "weakness_queue": {
      "path": "docs/reports/2026-07-05-product-weakness-horizon-candidates.md",
      "exists": true,
      "hint": "python scripts\\product_weakness_horizon_candidates.py --format text --write"
    },
    "retriever_close": {
      "path": "docs/reports/2026-07-05-runtime-retriever-promotion-gate-close-report.md",
      "exists": true,
      "hint": "python scripts\\runtime_retriever_promotion_close_gate.py --format text --write"
    }
  },
  "missing_reports": [],
  "protected_boundaries": {
    "no_private_payload_scan": true,
    "no_embedding_dump_scan": true,
    "no_dogfood_material_scan": true,
    "public_reports_only": true
  },
  "warnings": [],
  "checks": {
    "python_available": true,
    "uv_checked": true,
    "required_reports_checked": true,
    "required_reports_present": true,
    "protected_boundaries_checked": true
  },
  "errors": [],
  "next_gate": "report_manifest_and_navigation_surface",
  "report_path": "docs/reports/2026-07-05-oeh2-run-doctor.md"
}
```
