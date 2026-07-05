# E2E3 Demo Packet Builder

> Scope: generator report for the end-to-end demo packet.

## 한 줄 결론

Open one index and walk the public-safe end-to-end demo without reading ROADMAP internals.

- Packet: `docs/reports/end-to-end-demo/INDEX.md`

## Packet Items

| Order | Section | Report | Exists |
|---:|---|---|---|
| 0 | start | `docs/reports/2026-07-05-accounting-intelligence-progress-map.md` | True |
| 1 | storyboard | `docs/reports/2026-07-05-e2e1-demo-asset-inventory.md` | True |
| 2 | contract | `docs/reports/2026-07-05-e2e2-scenario-contract.md` | True |
| 3 | parser | `docs/reports/2026-07-05-real-local-parser-prototype-close-report.md` | True |
| 4 | source | `docs/reports/2026-07-05-source-body-ingestion-controlled-lane-close-report.md` | True |
| 5 | workflow | `docs/reports/2026-07-05-workflow-coverage-expansion-close-report.md` | True |
| 6 | retriever | `docs/reports/2026-07-05-runtime-retriever-promotion-gate-close-report.md` | True |
| 7 | operator | `docs/reports/2026-07-05-operator-experience-hardening-close-report.md` | True |

## Checks

| Check | OK |
|---|---|
| packet_items_ordered | True |
| all_reports_exist | True |
| all_commands_present | True |
| all_recovery_hints_present | True |
| protected_paths_absent | True |

## Errors

- none

## Next Leaf

- `E2E4_demo_smoke_and_navigation_gate`

## Machine Result

```json
{
  "title": "E2E3 Demo Packet Builder",
  "ok": true,
  "horizon": "end-to-end-demo-scenario",
  "completed_milestone": "E2E3",
  "packet_path": "docs/reports/end-to-end-demo/INDEX.md",
  "packet_claim": "Open one index and walk the public-safe end-to-end demo without reading ROADMAP internals.",
  "items": [
    {
      "order": 0,
      "section": "start",
      "title": "Current Position",
      "report": "docs/reports/2026-07-05-accounting-intelligence-progress-map.md",
      "report_exists": true,
      "command": "python scripts\\accounting_intelligence_progress_map.py --format text --write",
      "purpose": "Orient the operator to the active horizon and next leaf.",
      "recovery": "rerun the progress map command if the position report is missing"
    },
    {
      "order": 1,
      "section": "storyboard",
      "title": "Demo Asset Inventory",
      "report": "docs/reports/2026-07-05-e2e1-demo-asset-inventory.md",
      "report_exists": true,
      "command": "python scripts\\e2e_demo_asset_inventory.py --format text --write",
      "purpose": "Show the ordered public-safe demo story.",
      "recovery": "rerun E2E1 inventory if any core report is missing"
    },
    {
      "order": 2,
      "section": "contract",
      "title": "Scenario Contract",
      "report": "docs/reports/2026-07-05-e2e2-scenario-contract.md",
      "report_exists": true,
      "command": "python scripts\\e2e_scenario_contract.py --format text --write",
      "purpose": "Fix stage inputs, evidence, outputs, review checkpoints, commands, and failure boundaries.",
      "recovery": "rerun E2E2 contract if stage boundaries are unclear"
    },
    {
      "order": 3,
      "section": "parser",
      "title": "Local Parser Evidence",
      "report": "docs/reports/2026-07-05-real-local-parser-prototype-close-report.md",
      "report_exists": true,
      "command": "python scripts\\real_local_parser_prototype_close_gate.py --format text",
      "purpose": "Explain the local-safe parser boundary.",
      "recovery": "use E2E1 inventory to identify missing parser evidence"
    },
    {
      "order": 4,
      "section": "source",
      "title": "Controlled Source Evidence",
      "report": "docs/reports/2026-07-05-source-body-ingestion-controlled-lane-close-report.md",
      "report_exists": true,
      "command": "python scripts\\controlled_lane_close_gate.py --format text",
      "purpose": "Explain authorized source lane handling.",
      "recovery": "rerun controlled lane close gate after source policy reports exist"
    },
    {
      "order": 5,
      "section": "workflow",
      "title": "Workflow Evidence",
      "report": "docs/reports/2026-07-05-workflow-coverage-expansion-close-report.md",
      "report_exists": true,
      "command": "python scripts\\workflow_coverage_close_gate.py --format text",
      "purpose": "Explain the 1037 provisions decision-prep extension.",
      "recovery": "rerun workflow coverage close gate after adapter evidence exists"
    },
    {
      "order": 6,
      "section": "retriever",
      "title": "Retriever Promotion Evidence",
      "report": "docs/reports/2026-07-05-runtime-retriever-promotion-gate-close-report.md",
      "report_exists": true,
      "command": "python scripts\\runtime_retriever_promotion_close_gate.py --format text",
      "purpose": "Explain why default retriever promotion is deferred.",
      "recovery": "rerun promotion close gate and keep default unchanged if evidence is weak"
    },
    {
      "order": 7,
      "section": "operator",
      "title": "Operator Evidence",
      "report": "docs/reports/2026-07-05-operator-experience-hardening-close-report.md",
      "report_exists": true,
      "command": "python scripts\\operator_experience_close_gate.py --format text",
      "purpose": "Show command discovery, doctor, manifest, and recovery path.",
      "recovery": "run operator doctor and follow recovery playbook hints"
    }
  ],
  "checks": {
    "packet_items_ordered": true,
    "all_reports_exist": true,
    "all_commands_present": true,
    "all_recovery_hints_present": true,
    "protected_paths_absent": true
  },
  "errors": [],
  "next_leaf": "E2E4_demo_smoke_and_navigation_gate",
  "report_path": "docs/reports/2026-07-05-e2e3-demo-packet-builder.md"
}
```
