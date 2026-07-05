# LPOR1 Local Parser Operator Runbook

> Scope: operator runbook for the local parser policy/contract/dry-run/scaffold chain before real private-file parsing exists.

## 한 줄 결론

The local parser operator path is now explicit: run storage policy, parser fixture, adapter contract, adapter dry-run gate, adapter scaffold, and public-safe preflight in order. This runbook still does not authorize real file upload, OCR, source-body parsing, deletion automation, or private embeddings.

## Run Order

### LPOR1-1 Confirm upload/storage policy

- Purpose: Verify local ephemeral quarantine, structured-facts-only parser mode, manual deletion, and public artifact limits.
- Command: `python scripts\client_private_upload_storage_policy_check.py --format text --write`
- Success signal: `ok: True`

### LPOR1-2 Confirm parser dry-run fixture

- Purpose: Verify synthetic private-parser fixture shape routes to a review-pack candidate without source payloads.
- Command: `python scripts\client_private_parser_dry_run_fixture_check.py --format text --write`
- Success signal: `route_status: candidate`

### LPOR1-3 Confirm adapter contract

- Purpose: Verify adapter output schema, forbidden outputs, required operator checks, and prototype handoff.
- Command: `python scripts\client_private_local_parser_adapter_contract_check.py --format text --write`
- Success signal: `route_status: candidate`

### LPOR1-4 Run adapter dry-run gate

- Purpose: Verify multiple synthetic structured-fact cases pass contract handoff and candidate routing.
- Command: `python scripts\client_private_local_parser_adapter_dry_run_gate.py --format text --write`
- Success signal: `failed: 0`

### LPOR1-5 Run adapter scaffold

- Purpose: Verify the operator-facing entrypoint refuses raw paths, OCR, source-body parsing/persistence, and private embeddings.
- Command: `python scripts\client_private_local_parser_adapter_scaffold.py --format text --write`
- Success signal: `real_adapter_implemented: False`

### LPOR1-6 Run public-safe preflight

- Purpose: Verify no protected source assets are required for the public artifact set.
- Command: `python scripts\quality_preflight.py --format text`
- Success signal: `public_safe: True`

## Current Gate Status

- OK: True
- Present reports: upload_storage_policy, parser_dry_run_fixture, adapter_contract, adapter_dry_run_gate, adapter_scaffold
- Missing reports: none

## Subchecks

- upload_storage_policy: True
- parser_dry_run_fixture: True
- adapter_contract: True
- adapter_dry_run_gate: True
- adapter_scaffold: True

## Stop Conditions

- Stop if any command above does not produce its success signal.
- Stop if any raw file path, OCR text, source body, customer identifier, or private embedding appears in a public artifact.
- Stop if the operator cannot confirm `structured-facts-only-public-safe` before running the scaffold.
- Do not mark real parser readiness from this runbook; it is a pre-parser operator gate only.

## Still Not Implemented

- real file upload UI
- OCR
- real private document parsing
- real file deletion automation
- private embedding/index namespace

## Next Leaf

real-accountant-session RS2/RS3 evidence capture, or local parser real-adapter decision gate

## Machine Result

```json
{
  "ok": true,
  "errors": [],
  "present_reports": [
    "upload_storage_policy",
    "parser_dry_run_fixture",
    "adapter_contract",
    "adapter_dry_run_gate",
    "adapter_scaffold"
  ],
  "missing_reports": [],
  "subchecks": {
    "upload_storage_policy": true,
    "parser_dry_run_fixture": true,
    "adapter_contract": true,
    "adapter_dry_run_gate": true,
    "adapter_scaffold": true
  },
  "steps": [
    {
      "step_id": "LPOR1-1",
      "title": "Confirm upload/storage policy",
      "command": "python scripts\\client_private_upload_storage_policy_check.py --format text --write",
      "purpose": "Verify local ephemeral quarantine, structured-facts-only parser mode, manual deletion, and public artifact limits.",
      "success_signal": "ok: True"
    },
    {
      "step_id": "LPOR1-2",
      "title": "Confirm parser dry-run fixture",
      "command": "python scripts\\client_private_parser_dry_run_fixture_check.py --format text --write",
      "purpose": "Verify synthetic private-parser fixture shape routes to a review-pack candidate without source payloads.",
      "success_signal": "route_status: candidate"
    },
    {
      "step_id": "LPOR1-3",
      "title": "Confirm adapter contract",
      "command": "python scripts\\client_private_local_parser_adapter_contract_check.py --format text --write",
      "purpose": "Verify adapter output schema, forbidden outputs, required operator checks, and prototype handoff.",
      "success_signal": "route_status: candidate"
    },
    {
      "step_id": "LPOR1-4",
      "title": "Run adapter dry-run gate",
      "command": "python scripts\\client_private_local_parser_adapter_dry_run_gate.py --format text --write",
      "purpose": "Verify multiple synthetic structured-fact cases pass contract handoff and candidate routing.",
      "success_signal": "failed: 0"
    },
    {
      "step_id": "LPOR1-5",
      "title": "Run adapter scaffold",
      "command": "python scripts\\client_private_local_parser_adapter_scaffold.py --format text --write",
      "purpose": "Verify the operator-facing entrypoint refuses raw paths, OCR, source-body parsing/persistence, and private embeddings.",
      "success_signal": "real_adapter_implemented: False"
    },
    {
      "step_id": "LPOR1-6",
      "title": "Run public-safe preflight",
      "command": "python scripts\\quality_preflight.py --format text",
      "purpose": "Verify no protected source assets are required for the public artifact set.",
      "success_signal": "public_safe: True"
    }
  ],
  "report_path": "docs\\reports\\2026-07-05-lpor1-local-parser-operator-runbook.md",
  "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or local parser real-adapter decision gate"
}
```
