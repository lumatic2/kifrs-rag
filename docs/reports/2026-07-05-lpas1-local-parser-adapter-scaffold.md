# LPAS1 Local Parser Adapter Scaffold

> Scope: adapter entrypoint scaffold for structured-facts-only local parser work before real file/OCR parsing exists.

## 한 줄 결론

A local parser adapter scaffold now exists. It accepts structured facts only, refuses raw file paths/OCR/source-body parsing/source persistence/private embeddings, and hands public-safe facts into the existing KIFRS1116 review-pack route. It is not a real private-file parser.

## Scaffold Run

### Local Parser Adapter Scaffold Run - lpas1-local-parser-adapter-scaffold

- Contract: lpa1-synthetic-local-parser-adapter-contract
- OK: True
- Real adapter implemented: False
- Source kind: synthetic_fixture
- Source stub: local-private://dry-run/lpas1-structured-facts-adapter-scaffold

## Route

- Route: kifrs1116_review_pack
- Route status: candidate
- Deletion status: deleted

## Boundary

- This scaffold accepts structured facts only.
- It refuses raw file paths, OCR, source-body parsing, source-body persistence, and private embeddings.
- It is an adapter entrypoint scaffold, not a real private-file parser.

## What This Enables

- Future real local-only parser work has a stable entrypoint and refusal behavior.
- Operator-facing tooling can call one scaffold instead of reaching directly into prototype internals.
- Gap audit can distinguish scaffold readiness from actual parser implementation.

## Still Not Implemented

- real file upload UI
- OCR
- real private document parsing
- real file deletion automation
- private embedding/index namespace

## Next Leaf

real-accountant-session RS2/RS3 evidence capture, or local parser operator runbook

## Machine Result

```json
{
  "ok": true,
  "errors": [],
  "policy_id": "cpu1-local-upload-parser-storage-policy",
  "contract_id": "lpa1-synthetic-local-parser-adapter-contract",
  "scaffold_run": {
    "scaffold_id": "lpas1-local-parser-adapter-scaffold",
    "contract_id": "lpa1-synthetic-local-parser-adapter-contract",
    "request": {
      "scaffold_run_id": "lpas1-structured-facts-adapter-scaffold",
      "source_kind": "synthetic_fixture",
      "source_stub": "local-private://dry-run/lpas1-structured-facts-adapter-scaffold",
      "document_type": "contract",
      "expected_domain": "KIFRS1116",
      "extracted_fields": {
        "party": "lessee",
        "lease_term": "4 years",
        "payment_schedule": "quarterly fixed payments"
      },
      "operator_ack": "structured-facts-only-public-safe",
      "raw_file_path": "",
      "ocr_enabled": false,
      "parse_source_body": false,
      "persist_source_body": false,
      "create_private_embedding": false
    },
    "prototype_result": {
      "parser_run_id": "lpas1-structured-facts-adapter-scaffold",
      "fixture": {
        "fixture_id": "lpas1-structured-facts-adapter-scaffold",
        "parser_mode": "structured_facts_only",
        "document_type": "contract",
        "source_stub": "local-private://dry-run/lpas1-structured-facts-adapter-scaffold",
        "expected_domain": "KIFRS1116",
        "structured_facts": {
          "party": "lessee",
          "lease_term": "4 years",
          "payment_schedule": "quarterly fixed payments"
        },
        "allowed_output_level": "review_pack_summary",
        "redaction_status": "reviewed_public_safe",
        "reviewer_original_document_check": true,
        "deletion_attestation": "synthetic parser prototype source deleted before report write"
      },
      "redacted_summary": {
        "case_id": "lpas1-structured-facts-adapter-scaffold",
        "document_type": "contract",
        "redaction_status": "reviewed_public_safe",
        "allowed_output_level": "review_pack_summary",
        "reviewer_original_document_check": true,
        "structured_fact_keys": [
          "lease_term",
          "party",
          "payment_schedule"
        ],
        "structured_facts": {
          "lease_term": "4 years",
          "party": "lessee",
          "payment_schedule": "quarterly fixed payments"
        }
      },
      "route": {
        "case_id": "lpas1-structured-facts-adapter-scaffold",
        "domain": "KIFRS1116",
        "route": "kifrs1116_review_pack",
        "status": "candidate",
        "reason": "minimum structured facts are present for a review-pack draft candidate",
        "missing_facts": []
      },
      "deletion_attestation": {
        "attestation_id": "lpas1-structured-facts-adapter-scaffold-deletion-attestation",
        "fixture_id": "lpas1-structured-facts-adapter-scaffold",
        "source_stub": "local-private://dry-run/lpas1-structured-facts-adapter-scaffold",
        "deletion_status": "deleted",
        "deletion_mode": "manual_before_commit",
        "operator_check": "operator verified gitignored local-only paths and checked the synthetic parser prototype source was deleted before report write",
        "allowed_public_artifact": "deletion attestation",
        "deleted_before_report_write": true,
        "raw_file_present": false,
        "parsed_body_present": false,
        "ocr_text_present": false,
        "embedding_present": false
      }
    },
    "errors": [],
    "real_adapter_implemented": false,
    "ok": true
  },
  "report_path": "docs\\reports\\2026-07-05-lpas1-local-parser-adapter-scaffold.md",
  "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or local parser operator runbook"
}
```
