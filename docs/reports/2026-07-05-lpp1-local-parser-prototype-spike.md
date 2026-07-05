# LPP1 Local Parser Prototype Spike

> Scope: first synthetic local parser prototype that converts parser-shaped input into public-safe structured facts.

## 한 줄 결론

A first local parser prototype now exists at the synthetic contract level: it accepts parser-shaped structured input, produces a redacted client-private summary, routes it to a KIFRS1116 review-pack candidate, and emits deletion attestation. It still does not read real files, run OCR, parse source bodies, delete files, or create private embeddings.

## Prototype Result

### Local Parser Prototype Result - lpp1-synthetic-lease-parser-prototype

- Route: kifrs1116_review_pack
- Route status: candidate
- Deletion status: deleted
- Deleted before report write: True

## Structured Fact Keys

- lease_term
- party
- payment_schedule

## Boundary

- This prototype does not read files, run OCR, store source bodies, or create embeddings.
- It only converts synthetic parser-shaped input into redacted structured facts and a review-pack route candidate.
- Real private file handling remains outside this repo until a separate local-only implementation gate exists.

## What This Enables

- The next implementation can replace synthetic extracted fields with a local-only parser adapter.
- Review-pack routing can be tested from parser-shaped output without touching private source documents.
- Public artifacts can prove the parser contract without storing raw payloads.

## Still Not Implemented

- real file upload UI
- OCR
- real private document parsing
- real file deletion automation
- private embedding/index namespace

## Next Leaf

real-accountant-session RS2/RS3 evidence capture, or local parser prototype close gate

## Machine Result

```json
{
  "ok": true,
  "errors": [],
  "policy_id": "cpu1-local-upload-parser-storage-policy",
  "parser_input": {
    "parser_run_id": "lpp1-synthetic-lease-parser-prototype",
    "source_stub": "local-private://dry-run/synthetic-lease-parser-prototype",
    "document_type": "contract",
    "expected_domain": "KIFRS1116",
    "extracted_fields": {
      "party": "lessee",
      "lease_term": "5 years",
      "payment_schedule": "monthly fixed payments"
    },
    "parser_mode": "structured_facts_only",
    "allowed_output_level": "review_pack_summary",
    "redaction_status": "reviewed_public_safe",
    "reviewer_original_document_check": true,
    "raw_file_present": false,
    "parsed_body_present": false,
    "ocr_text_present": false,
    "embedding_present": false
  },
  "prototype_result": {
    "parser_run_id": "lpp1-synthetic-lease-parser-prototype",
    "fixture": {
      "fixture_id": "lpp1-synthetic-lease-parser-prototype",
      "parser_mode": "structured_facts_only",
      "document_type": "contract",
      "source_stub": "local-private://dry-run/synthetic-lease-parser-prototype",
      "expected_domain": "KIFRS1116",
      "structured_facts": {
        "party": "lessee",
        "lease_term": "5 years",
        "payment_schedule": "monthly fixed payments"
      },
      "allowed_output_level": "review_pack_summary",
      "redaction_status": "reviewed_public_safe",
      "reviewer_original_document_check": true,
      "deletion_attestation": "synthetic parser prototype source deleted before report write"
    },
    "redacted_summary": {
      "case_id": "lpp1-synthetic-lease-parser-prototype",
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
        "lease_term": "5 years",
        "party": "lessee",
        "payment_schedule": "monthly fixed payments"
      }
    },
    "route": {
      "case_id": "lpp1-synthetic-lease-parser-prototype",
      "domain": "KIFRS1116",
      "route": "kifrs1116_review_pack",
      "status": "candidate",
      "reason": "minimum structured facts are present for a review-pack draft candidate",
      "missing_facts": []
    },
    "deletion_attestation": {
      "attestation_id": "lpp1-synthetic-lease-parser-prototype-deletion-attestation",
      "fixture_id": "lpp1-synthetic-lease-parser-prototype",
      "source_stub": "local-private://dry-run/synthetic-lease-parser-prototype",
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
  "route": {
    "case_id": "lpp1-synthetic-lease-parser-prototype",
    "domain": "KIFRS1116",
    "route": "kifrs1116_review_pack",
    "status": "candidate",
    "reason": "minimum structured facts are present for a review-pack draft candidate",
    "missing_facts": []
  },
  "report_path": "docs\\reports\\2026-07-05-lpp1-local-parser-prototype-spike.md",
  "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or local parser prototype close gate"
}
```
