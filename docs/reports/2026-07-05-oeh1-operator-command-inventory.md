# OEH1 Operator Command Inventory

> Scope: operator-facing command discovery for the local toolkit.

## 한 줄 결론

The local operator now has a goal-based command inventory for quality, trust, source, workflow, retriever, progress, and operator-hardening tasks.

## Commands

| Goal | Command | Report | Safety Note |
|---|---|---|---|
| quality_rag | `python scripts\rag_quality_final_gate.py --format text` | `docs/reports/2026-07-05-rag-quality-refresh-close-report.md` | read-only eval gate; does not change runtime default |
| trust_surface | `python scripts\product_trust_quality_gate.py --format text` | `docs/reports/2026-07-05-product-trust-quality-close-report.md` | public-safe report gate |
| controlled_source_lane | `python scripts\controlled_lane_close_gate.py --format text` | `docs/reports/2026-07-05-source-body-ingestion-controlled-lane-close-report.md` | synthetic-only controlled lane; no live body fetch |
| workflow_coverage | `python scripts\workflow_coverage_close_gate.py --format text` | `docs/reports/2026-07-05-workflow-coverage-expansion-close-report.md` | uses public-safe workflow evidence |
| retriever_promotion | `python scripts\runtime_retriever_promotion_close_gate.py --format text` | `docs/reports/2026-07-05-runtime-retriever-promotion-gate-close-report.md` | close result is defer; command does not promote runtime default |
| progress_position | `python scripts\accounting_intelligence_progress_map.py --format text --write` | `docs/reports/2026-07-05-accounting-intelligence-progress-map.md` | writes public progress map only |
| weakness_queue | `python scripts\product_weakness_horizon_candidates.py --format text --write` | `docs/reports/2026-07-05-product-weakness-horizon-candidates.md` | writes public horizon queue only |
| operator_hardening | `python scripts\operator_command_inventory.py --format text --write` | `docs/reports/2026-07-05-oeh1-operator-command-inventory.md` | command inventory; no protected data inspection |

## Checks

| Check | OK |
|---|---|
| all_required_goals_present | True |
| commands_present | True |
| reports_present | True |
| safety_notes_present | True |
| protected_data_not_required | True |

## Errors

- none

## Machine Result

```json
{
  "title": "OEH1 Operator Command Inventory",
  "ok": true,
  "horizon": "operator-experience-hardening",
  "completed_milestone": "OEH1",
  "commands": [
    {
      "goal": "quality_rag",
      "command": "python scripts\\rag_quality_final_gate.py --format text",
      "report": "docs/reports/2026-07-05-rag-quality-refresh-close-report.md",
      "safety_note": "read-only eval gate; does not change runtime default"
    },
    {
      "goal": "trust_surface",
      "command": "python scripts\\product_trust_quality_gate.py --format text",
      "report": "docs/reports/2026-07-05-product-trust-quality-close-report.md",
      "safety_note": "public-safe report gate"
    },
    {
      "goal": "controlled_source_lane",
      "command": "python scripts\\controlled_lane_close_gate.py --format text",
      "report": "docs/reports/2026-07-05-source-body-ingestion-controlled-lane-close-report.md",
      "safety_note": "synthetic-only controlled lane; no live body fetch"
    },
    {
      "goal": "workflow_coverage",
      "command": "python scripts\\workflow_coverage_close_gate.py --format text",
      "report": "docs/reports/2026-07-05-workflow-coverage-expansion-close-report.md",
      "safety_note": "uses public-safe workflow evidence"
    },
    {
      "goal": "retriever_promotion",
      "command": "python scripts\\runtime_retriever_promotion_close_gate.py --format text",
      "report": "docs/reports/2026-07-05-runtime-retriever-promotion-gate-close-report.md",
      "safety_note": "close result is defer; command does not promote runtime default"
    },
    {
      "goal": "progress_position",
      "command": "python scripts\\accounting_intelligence_progress_map.py --format text --write",
      "report": "docs/reports/2026-07-05-accounting-intelligence-progress-map.md",
      "safety_note": "writes public progress map only"
    },
    {
      "goal": "weakness_queue",
      "command": "python scripts\\product_weakness_horizon_candidates.py --format text --write",
      "report": "docs/reports/2026-07-05-product-weakness-horizon-candidates.md",
      "safety_note": "writes public horizon queue only"
    },
    {
      "goal": "operator_hardening",
      "command": "python scripts\\operator_command_inventory.py --format text --write",
      "report": "docs/reports/2026-07-05-oeh1-operator-command-inventory.md",
      "safety_note": "command inventory; no protected data inspection"
    }
  ],
  "required_goals": [
    "controlled_source_lane",
    "operator_hardening",
    "progress_position",
    "quality_rag",
    "retriever_promotion",
    "trust_surface",
    "weakness_queue",
    "workflow_coverage"
  ],
  "missing_goals": [],
  "checks": {
    "all_required_goals_present": true,
    "commands_present": true,
    "reports_present": true,
    "safety_notes_present": true,
    "protected_data_not_required": true
  },
  "errors": [],
  "next_gate": "run_doctor_and_environment_checks",
  "report_path": "docs/reports/2026-07-05-oeh1-operator-command-inventory.md"
}
```
