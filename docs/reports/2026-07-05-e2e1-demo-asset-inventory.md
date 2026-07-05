# E2E1 Demo Asset Inventory And Storyboard

> Scope: public-safe inventory of the reports needed for one firm-facing end-to-end demo.

## 한 줄 결론

A firm-facing operator can show local-safe intake, controlled source evidence, decision-prep workflow output, conservative retriever promotion, and recoverable operator navigation as one demo.

## Demo Storyboard

- Audience: Accounting Advisory / Financial Statement support operator
- Boundary: public-safe reports only; no protected local data or final accounting judgment

| Order | Stage | Operator Question | Evidence | Exists | Demo Point |
|---:|---|---|---|---|---|
| 1 | Local Parser Prototype | Can the toolkit ingest local accounting files without exposing protected content? | `docs/reports/2026-07-05-real-local-parser-prototype-close-report.md` | True | A local-safe fixture parser path exists with deletion simulation and leak checks. |
| 2 | Controlled Source Lane | Can non-IFRS source material be handled as an authorized RAG lane? | `docs/reports/2026-07-05-source-body-ingestion-controlled-lane-close-report.md` | True | A controlled synthetic source lane has policy, chunking, retrieval, and close evidence. |
| 3 | Workflow Coverage Expansion | Can the system produce decision-prep output beyond the original 1109/1116 path? | `docs/reports/2026-07-05-workflow-coverage-expansion-close-report.md` | True | A 1037 provisions workflow adapter produces conditional decision-prep evidence. |
| 4 | Runtime Retriever Promotion Gate | Does the demo explain why the stronger retriever is not default yet? | `docs/reports/2026-07-05-runtime-retriever-promotion-gate-close-report.md` | True | Default promotion is deliberately deferred with regression, latency, and rollback evidence. |
| 5 | Operator Experience Hardening | Can an operator discover commands, diagnose failures, navigate reports, and recover? | `docs/reports/2026-07-05-operator-experience-hardening-close-report.md` | True | Command inventory, run doctor, report manifest, and recovery playbook are available. |

## Checks

| Check | OK |
|---|---|
| stage_ordered | True |
| stage_ids_unique | True |
| all_evidence_exists | True |
| all_operator_questions_present | True |
| all_demo_points_present | True |
| protected_paths_absent | True |

## Errors

- none

## Next Leaf

- `E2E2_scenario_contract`

## Machine Result

```json
{
  "title": "E2E1 Demo Asset Inventory And Storyboard",
  "ok": true,
  "horizon": "end-to-end-demo-scenario",
  "completed_milestone": "E2E1",
  "storyboard": {
    "one_line": "A firm-facing operator can show local-safe intake, controlled source evidence, decision-prep workflow output, conservative retriever promotion, and recoverable operator navigation as one demo.",
    "audience": "Accounting Advisory / Financial Statement support operator",
    "boundary": "public-safe reports only; no protected local data or final accounting judgment"
  },
  "stages": [
    {
      "order": 1,
      "stage_id": "parser",
      "title": "Local Parser Prototype",
      "operator_question": "Can the toolkit ingest local accounting files without exposing protected content?",
      "evidence": "docs/reports/2026-07-05-real-local-parser-prototype-close-report.md",
      "evidence_exists": true,
      "demo_point": "A local-safe fixture parser path exists with deletion simulation and leak checks.",
      "next_step": "Move parsed structured facts into authorized evidence lanes."
    },
    {
      "order": 2,
      "stage_id": "source_lane",
      "title": "Controlled Source Lane",
      "operator_question": "Can non-IFRS source material be handled as an authorized RAG lane?",
      "evidence": "docs/reports/2026-07-05-source-body-ingestion-controlled-lane-close-report.md",
      "evidence_exists": true,
      "demo_point": "A controlled synthetic source lane has policy, chunking, retrieval, and close evidence.",
      "next_step": "Use the source lane as supporting evidence for workflow output."
    },
    {
      "order": 3,
      "stage_id": "workflow",
      "title": "Workflow Coverage Expansion",
      "operator_question": "Can the system produce decision-prep output beyond the original 1109/1116 path?",
      "evidence": "docs/reports/2026-07-05-workflow-coverage-expansion-close-report.md",
      "evidence_exists": true,
      "demo_point": "A 1037 provisions workflow adapter produces conditional decision-prep evidence.",
      "next_step": "Show the output as review-ready draft material, not final accounting judgment."
    },
    {
      "order": 4,
      "stage_id": "retriever",
      "title": "Runtime Retriever Promotion Gate",
      "operator_question": "Does the demo explain why the stronger retriever is not default yet?",
      "evidence": "docs/reports/2026-07-05-runtime-retriever-promotion-gate-close-report.md",
      "evidence_exists": true,
      "demo_point": "Default promotion is deliberately deferred with regression, latency, and rollback evidence.",
      "next_step": "Keep the demo honest about quality boundaries and explicit promotion authorization."
    },
    {
      "order": 5,
      "stage_id": "operator",
      "title": "Operator Experience Hardening",
      "operator_question": "Can an operator discover commands, diagnose failures, navigate reports, and recover?",
      "evidence": "docs/reports/2026-07-05-operator-experience-hardening-close-report.md",
      "evidence_exists": true,
      "demo_point": "Command inventory, run doctor, report manifest, and recovery playbook are available.",
      "next_step": "Build one scenario contract and packet from these pieces."
    }
  ],
  "checks": {
    "stage_ordered": true,
    "stage_ids_unique": true,
    "all_evidence_exists": true,
    "all_operator_questions_present": true,
    "all_demo_points_present": true,
    "protected_paths_absent": true
  },
  "errors": [],
  "next_leaf": "E2E2_scenario_contract",
  "report_path": "docs/reports/2026-07-05-e2e1-demo-asset-inventory.md"
}
```
