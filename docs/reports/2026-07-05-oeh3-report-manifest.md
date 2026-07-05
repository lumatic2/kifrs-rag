# OEH3 Report Manifest

> Scope: ordered public report navigation surface for local operators.

## 한 줄 결론

The operator can now start from progress, then queue, commands, doctor, and the latest close reports without reading ROADMAP internals.

## Manifest

| Order | Goal | Question | Report | Exists | Hint |
|---:|---|---|---|---|---|
| 1 | position | Where am I? | `docs/reports/2026-07-05-accounting-intelligence-progress-map.md` | True | `rerun producing command from OEH1 inventory if missing` |
| 2 | queue | What product weakness horizon is active? | `docs/reports/2026-07-05-product-weakness-horizon-candidates.md` | True | `rerun producing command from OEH1 inventory if missing` |
| 3 | commands | What can I run? | `docs/reports/2026-07-05-oeh1-operator-command-inventory.md` | True | `rerun producing command from OEH1 inventory if missing` |
| 4 | doctor | Is the local operator surface healthy? | `docs/reports/2026-07-05-oeh2-run-doctor.md` | True | `rerun producing command from OEH1 inventory if missing` |
| 5 | retriever | Why is retriever promotion deferred? | `docs/reports/2026-07-05-runtime-retriever-promotion-gate-close-report.md` | True | `rerun producing command from OEH1 inventory if missing` |
| 6 | workflow | What new accounting workflow was added? | `docs/reports/2026-07-05-workflow-coverage-expansion-close-report.md` | True | `rerun producing command from OEH1 inventory if missing` |
| 7 | source | What non-IFRS source lane exists? | `docs/reports/2026-07-05-source-body-ingestion-controlled-lane-close-report.md` | True | `rerun producing command from OEH1 inventory if missing` |

## Checks

| Check | OK |
|---|---|
| entries_ordered | True |
| all_entries_have_goal | True |
| all_entries_have_path | True |
| missing_hints_present | True |
| protected_paths_absent | True |

## Errors

- none

## Machine Result

```json
{
  "title": "OEH3 Report Manifest",
  "ok": true,
  "horizon": "operator-experience-hardening",
  "completed_milestone": "OEH3",
  "entries": [
    {
      "order": 1,
      "goal": "position",
      "question": "Where am I?",
      "path": "docs/reports/2026-07-05-accounting-intelligence-progress-map.md",
      "exists": true,
      "hint": "rerun producing command from OEH1 inventory if missing"
    },
    {
      "order": 2,
      "goal": "queue",
      "question": "What product weakness horizon is active?",
      "path": "docs/reports/2026-07-05-product-weakness-horizon-candidates.md",
      "exists": true,
      "hint": "rerun producing command from OEH1 inventory if missing"
    },
    {
      "order": 3,
      "goal": "commands",
      "question": "What can I run?",
      "path": "docs/reports/2026-07-05-oeh1-operator-command-inventory.md",
      "exists": true,
      "hint": "rerun producing command from OEH1 inventory if missing"
    },
    {
      "order": 4,
      "goal": "doctor",
      "question": "Is the local operator surface healthy?",
      "path": "docs/reports/2026-07-05-oeh2-run-doctor.md",
      "exists": true,
      "hint": "rerun producing command from OEH1 inventory if missing"
    },
    {
      "order": 5,
      "goal": "retriever",
      "question": "Why is retriever promotion deferred?",
      "path": "docs/reports/2026-07-05-runtime-retriever-promotion-gate-close-report.md",
      "exists": true,
      "hint": "rerun producing command from OEH1 inventory if missing"
    },
    {
      "order": 6,
      "goal": "workflow",
      "question": "What new accounting workflow was added?",
      "path": "docs/reports/2026-07-05-workflow-coverage-expansion-close-report.md",
      "exists": true,
      "hint": "rerun producing command from OEH1 inventory if missing"
    },
    {
      "order": 7,
      "goal": "source",
      "question": "What non-IFRS source lane exists?",
      "path": "docs/reports/2026-07-05-source-body-ingestion-controlled-lane-close-report.md",
      "exists": true,
      "hint": "rerun producing command from OEH1 inventory if missing"
    }
  ],
  "checks": {
    "entries_ordered": true,
    "all_entries_have_goal": true,
    "all_entries_have_path": true,
    "missing_hints_present": true,
    "protected_paths_absent": true
  },
  "errors": [],
  "next_gate": "error_recovery_playbook",
  "report_path": "docs/reports/2026-07-05-oeh3-report-manifest.md"
}
```
