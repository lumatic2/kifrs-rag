# LPIP1 Local Parser Real-Adapter Implementation Plan

> Scope: implementation plan required before any real local-only private-file parser adapter coding.

## 한 줄 결론

Real adapter coding is still not authorized. This plan only defines the safe implementation order for a future local-only parser after actual accountant feedback evidence and explicit user authorization exist.

## Preconditions

- actual accountant feedback evidence exists and has passed the public-safe capture gate.
- explicit user authorization is recorded for real local private-file parser work.
- `python scripts\client_private_local_parser_operator_runbook.py --format text --write` passes.
- `python scripts\client_private_local_parser_real_adapter_decision_gate.py --authorize-real-adapter --implementation-plan docs\reports\2026-07-05-local-parser-real-adapter-implementation-plan.md` returns `allowed_to_implement: True`.

## Implementation Slices

1. Local quarantine path preflight
   - Accept only local ephemeral quarantine paths that are already gitignored.
   - Reject cloud paths, network shares, and repo-tracked paths.
   - no raw private file in public artifacts.
2. Parser adapter input envelope
   - Read from the local quarantine path only inside the authorized local run.
   - Convert the private input into structured facts only.
   - Keep raw content out of reports, JSONL, logs, tests, and commits.
3. Optional OCR boundary
   - OCR can run only inside the local quarantine flow if explicitly authorized.
   - no OCR text in public artifacts.
   - OCR output must be discarded or reduced to reviewed structured facts before report write.
4. Review-pack handoff
   - Reuse the existing `LocalPrivateParserPrototypeInput` and redaction route.
   - Route only reviewed structured facts into review-pack candidates.
   - Do not allow answer-time use of private document body.
5. Deletion attestation
   - delete quarantined files before report write.
   - Record deletion status and operator check without source text.
   - Fail close gates if raw, parsed, OCR, or embedding artifacts remain.
6. Public-safe gates and rollback
   - Run focused parser tests, `quality_preflight`, and gap audit before commit.
   - manual rollback is deletion of quarantine files plus removal of derived structured facts from the run output.

## Explicit Non-Goals

- No cloud upload.
- No private document persistence.
- no private embeddings before a separate namespace gate.
- No answer-time use of private source body.
- No commit of raw files, parsed bodies, OCR text, customer identifiers, or private embeddings.

## Verification Commands

```powershell
python scripts\client_private_local_parser_real_adapter_implementation_plan.py --format text --write
python scripts\client_private_local_parser_real_adapter_decision_gate.py --format text --write
python -m pytest tests\test_client_private_local_parser_real_adapter_implementation_plan.py tests\test_client_private_local_parser_real_adapter_decision_gate.py -q
python scripts\accounting_intelligence_gap_audit.py --format text --write
python scripts\quality_preflight.py --format text
```

## Next Leaf

real-accountant-session RS2/RS3 evidence capture, then explicit authorization before real adapter coding

## Machine Result

```json
{
  "ok": true,
  "errors": [],
  "plan_id": "lpip1-local-parser-real-adapter-implementation-plan",
  "plan_path": "docs/reports/2026-07-05-local-parser-real-adapter-implementation-plan.md",
  "operator_runbook_ok": true,
  "required_preconditions": [
    "actual accountant feedback evidence",
    "explicit user authorization",
    "passing local parser operator runbook",
    "public-safe implementation plan"
  ],
  "implementation_slices": [
    "local quarantine path preflight",
    "parser adapter input envelope",
    "structured facts extraction handoff",
    "redaction and review-pack routing",
    "deletion attestation",
    "public-safe gates and rollback"
  ],
  "forbidden_until_separate_gate": [
    "cloud upload",
    "private embeddings",
    "answer-time use of private document body",
    "committing raw files or parsed bodies"
  ],
  "next_leaf": "real-accountant-session RS2/RS3 evidence capture, then explicit authorization before real adapter coding"
}
```
