# E2E2 Scenario Contract

> Scope: stage-level contract for the end-to-end public-safe firm demo.

## 한 줄 결론

The toolkit can walk a public-safe accounting decision-prep demo from local intake boundary to operator recovery.

## Contract

- Scenario: `public_safe_firm_demo_v1`
- Audience: Accounting Advisory / Financial Statement support operator

## Non-Claims

- It does not replace final accounting judgment.
- It does not prove production deployment readiness.
- It does not expose protected local data.

## Stages

| Stage | Input | Evidence | Output | Review Checkpoint | Failure Boundary |
|---|---|---|---|---|---|
| parser | Local-safe accounting document fixture or extracted structured facts | `docs/reports/2026-07-05-real-local-parser-prototype-close-report.md` | Structured facts and deletion/leak-check evidence | Confirm no protected local payload is displayed in the demo output. | If local fixture evidence is missing, stop before claiming real-file parser readiness. |
| source_lane | Authorized synthetic interpretive source record | `docs/reports/2026-07-05-source-body-ingestion-controlled-lane-close-report.md` | Controlled source policy, chunking, and retrieval gate evidence | Confirm source use is authorized and synthetic/public-safe. | If source authorization is absent, do not run ingestion or retrieval claims. |
| workflow | Provision workflow fixture and authority-separated evidence | `docs/reports/2026-07-05-workflow-coverage-expansion-close-report.md` | Conditional decision-prep adapter output and coverage metric update | Confirm output is review-ready draft material, not final accounting judgment. | If required evidence is incomplete, label the workflow partial and route to human review. |
| retriever | Opt-in repair retriever evaluation and rollback evidence | `docs/reports/2026-07-05-runtime-retriever-promotion-gate-close-report.md` | Promotion result, regression/latency status, and rollback policy | Confirm default promotion remains deferred without explicit authorization. | If regression or rollback evidence is weak, keep current default retriever. |
| operator | Command inventory, run doctor, report manifest, and recovery playbook | `docs/reports/2026-07-05-operator-experience-hardening-close-report.md` | Run, diagnose, navigate, and recover operator path | Confirm the operator can recover from missing reports with explicit rerun commands. | If commands or reports are not discoverable, demo packet is not ready. |

## Operator Commands

| Stage | Command |
|---|---|
| parser | `python scripts\parser_prototype_asset_inventory.py --format text` |
| source_lane | `python scripts\controlled_lane_close_gate.py --format text` |
| workflow | `python scripts\workflow_coverage_close_gate.py --format text` |
| retriever | `python scripts\runtime_retriever_promotion_close_gate.py --format text` |
| operator | `python scripts\operator_experience_close_gate.py --format text` |

## Checks

| Check | OK |
|---|---|
| all_stages_have_required_keys | True |
| all_evidence_exists | True |
| all_review_checkpoints_present | True |
| all_failure_boundaries_present | True |
| all_operator_commands_present | True |
| final_judgment_boundary_present | True |
| authorization_boundary_present | True |

## Errors

- none

## Next Leaf

- `E2E3_demo_packet_builder`

## Machine Result

```json
{
  "title": "E2E2 Scenario Contract",
  "ok": true,
  "horizon": "end-to-end-demo-scenario",
  "completed_milestone": "E2E2",
  "contract": {
    "scenario_id": "public_safe_firm_demo_v1",
    "audience": "Accounting Advisory / Financial Statement support operator",
    "claim": "The toolkit can walk a public-safe accounting decision-prep demo from local intake boundary to operator recovery.",
    "non_claims": [
      "It does not replace final accounting judgment.",
      "It does not prove production deployment readiness.",
      "It does not expose protected local data."
    ]
  },
  "stages": [
    {
      "stage_id": "parser",
      "input_signal": "Local-safe accounting document fixture or extracted structured facts",
      "evidence": "docs/reports/2026-07-05-real-local-parser-prototype-close-report.md",
      "evidence_exists": true,
      "output": "Structured facts and deletion/leak-check evidence",
      "review_checkpoint": "Confirm no protected local payload is displayed in the demo output.",
      "operator_command": "python scripts\\parser_prototype_asset_inventory.py --format text",
      "failure_boundary": "If local fixture evidence is missing, stop before claiming real-file parser readiness."
    },
    {
      "stage_id": "source_lane",
      "input_signal": "Authorized synthetic interpretive source record",
      "evidence": "docs/reports/2026-07-05-source-body-ingestion-controlled-lane-close-report.md",
      "evidence_exists": true,
      "output": "Controlled source policy, chunking, and retrieval gate evidence",
      "review_checkpoint": "Confirm source use is authorized and synthetic/public-safe.",
      "operator_command": "python scripts\\controlled_lane_close_gate.py --format text",
      "failure_boundary": "If source authorization is absent, do not run ingestion or retrieval claims."
    },
    {
      "stage_id": "workflow",
      "input_signal": "Provision workflow fixture and authority-separated evidence",
      "evidence": "docs/reports/2026-07-05-workflow-coverage-expansion-close-report.md",
      "evidence_exists": true,
      "output": "Conditional decision-prep adapter output and coverage metric update",
      "review_checkpoint": "Confirm output is review-ready draft material, not final accounting judgment.",
      "operator_command": "python scripts\\workflow_coverage_close_gate.py --format text",
      "failure_boundary": "If required evidence is incomplete, label the workflow partial and route to human review."
    },
    {
      "stage_id": "retriever",
      "input_signal": "Opt-in repair retriever evaluation and rollback evidence",
      "evidence": "docs/reports/2026-07-05-runtime-retriever-promotion-gate-close-report.md",
      "evidence_exists": true,
      "output": "Promotion result, regression/latency status, and rollback policy",
      "review_checkpoint": "Confirm default promotion remains deferred without explicit authorization.",
      "operator_command": "python scripts\\runtime_retriever_promotion_close_gate.py --format text",
      "failure_boundary": "If regression or rollback evidence is weak, keep current default retriever."
    },
    {
      "stage_id": "operator",
      "input_signal": "Command inventory, run doctor, report manifest, and recovery playbook",
      "evidence": "docs/reports/2026-07-05-operator-experience-hardening-close-report.md",
      "evidence_exists": true,
      "output": "Run, diagnose, navigate, and recover operator path",
      "review_checkpoint": "Confirm the operator can recover from missing reports with explicit rerun commands.",
      "operator_command": "python scripts\\operator_experience_close_gate.py --format text",
      "failure_boundary": "If commands or reports are not discoverable, demo packet is not ready."
    }
  ],
  "checks": {
    "all_stages_have_required_keys": true,
    "all_evidence_exists": true,
    "all_review_checkpoints_present": true,
    "all_failure_boundaries_present": true,
    "all_operator_commands_present": true,
    "final_judgment_boundary_present": true,
    "authorization_boundary_present": true
  },
  "errors": [],
  "next_leaf": "E2E3_demo_packet_builder",
  "report_path": "docs/reports/2026-07-05-e2e2-scenario-contract.md"
}
```
