# OEH4 Error Recovery Playbook

> Scope: local operator recovery cases and rerun commands.

## 한 줄 결론

Common failures now point to specific rerun or remediation commands without destructive cleanup.

## Recovery Cases

| Case | Symptom | Remediation | Rerun Command |
|---|---|---|---|
| pytest_failure | A milestone test fails. | Read the failing assertion, rerun only the named test, then rerun the milestone script with --write. | `python -m pytest <failing-test> -q` |
| missing_report | A required public report is missing from doctor or manifest. | Run the producing command from OEH1 inventory or the hint shown by OEH2 doctor. | `python scripts\operator_run_doctor.py --format text --write` |
| default_retriever_guard_failure | Default retriever guard fails or target retriever is exposed too early. | Restore default mode expectation to hybrid and keep promotion deferred until RPG close gate is updated. | `python scripts\default_retriever_guard.py --format text` |
| protected_data_warning | A report or manifest appears to reference protected private/source data. | Remove protected references from public report surfaces and rerun the relevant public-safe test. | `python -m pytest tests\test_operator_run_doctor.py tests\test_operator_report_manifest.py -q` |
| navigation_drift | Progress map or manifest points to a stale next leaf. | Regenerate progress map and report manifest, then rerun their tests. | `python scripts\accounting_intelligence_progress_map.py --format text --write` |

## Checks

| Check | OK |
|---|---|
| cases_present | True |
| rerun_commands_present | True |
| no_destructive_recovery | True |
| protected_boundary_case_present | True |
| retriever_guard_case_present | True |

## Errors

- none

## Machine Result

```json
{
  "title": "OEH4 Error Recovery Playbook",
  "ok": true,
  "horizon": "operator-experience-hardening",
  "completed_milestone": "OEH4",
  "cases": [
    {
      "case_id": "pytest_failure",
      "symptom": "A milestone test fails.",
      "remediation": "Read the failing assertion, rerun only the named test, then rerun the milestone script with --write.",
      "rerun_command": "python -m pytest <failing-test> -q"
    },
    {
      "case_id": "missing_report",
      "symptom": "A required public report is missing from doctor or manifest.",
      "remediation": "Run the producing command from OEH1 inventory or the hint shown by OEH2 doctor.",
      "rerun_command": "python scripts\\operator_run_doctor.py --format text --write"
    },
    {
      "case_id": "default_retriever_guard_failure",
      "symptom": "Default retriever guard fails or target retriever is exposed too early.",
      "remediation": "Restore default mode expectation to hybrid and keep promotion deferred until RPG close gate is updated.",
      "rerun_command": "python scripts\\default_retriever_guard.py --format text"
    },
    {
      "case_id": "protected_data_warning",
      "symptom": "A report or manifest appears to reference protected private/source data.",
      "remediation": "Remove protected references from public report surfaces and rerun the relevant public-safe test.",
      "rerun_command": "python -m pytest tests\\test_operator_run_doctor.py tests\\test_operator_report_manifest.py -q"
    },
    {
      "case_id": "navigation_drift",
      "symptom": "Progress map or manifest points to a stale next leaf.",
      "remediation": "Regenerate progress map and report manifest, then rerun their tests.",
      "rerun_command": "python scripts\\accounting_intelligence_progress_map.py --format text --write"
    }
  ],
  "checks": {
    "cases_present": true,
    "rerun_commands_present": true,
    "no_destructive_recovery": true,
    "protected_boundary_case_present": true,
    "retriever_guard_case_present": true
  },
  "errors": [],
  "next_gate": "operator_experience_close_gate",
  "report_path": "docs/reports/2026-07-05-oeh4-error-recovery-playbook.md"
}
```
