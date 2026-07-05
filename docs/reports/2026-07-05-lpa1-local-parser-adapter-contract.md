# LPA1 Local Parser Adapter Contract

> Scope: public-safe adapter contract before any real local-only file/OCR/parser implementation.

## 한 줄 결론

A local parser adapter now has a fixed public-safe contract: it may hand off structured facts into the existing local parser prototype and route a KIFRS1116 contract to a review-pack candidate, but it still cannot read real files, run OCR, persist source bodies, create private embeddings, or claim deletion automation.

## Contract

### Local Parser Adapter Contract - lpa1-synthetic-local-parser-adapter-contract

- Source kind: synthetic_fixture
- Output mode: structured_facts_only
- Handoff target: local_parser_prototype_input
- Allowed document types: contract
- Allowed domains: KIFRS1116
- Validation issues: 0

## Required Extracted Fields

- party
- lease_term
- payment_schedule

## Forbidden Public Outputs

- raw private file
- parsed private body
- OCR text
- private embedding
- source document excerpt

## Required Operator Checks

- verify local-only paths are gitignored before receiving any file
- delete quarantined raw files before close
- record deletion attestation without source body text
- run public-safe gate before committing any derived artifact

## Boundary

- This contract does not read files, run OCR, store source bodies, create embeddings, or automate deletion.
- It only defines the public-safe adapter output shape before a real local-only parser exists.
- The handoff target is LocalPrivateParserPrototypeInput for review-pack routing validation.

## Handoff Result

### Local Parser Prototype Result - lpa1-contract-handoff-1116

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

- Future local-only parser adapters have a precise output schema and safety boundary.
- Parser work can be tested through `LocalPrivateParserPrototypeInput` before private file handling exists.
- Gap audit can separate adapter-contract readiness from real upload/OCR/parser implementation.

## Still Not Implemented

- real file upload UI
- OCR
- real private document parsing
- real file deletion automation
- private embedding/index namespace

## Next Leaf

real-accountant-session RS2/RS3 evidence capture, or local parser adapter dry-run gate

## Machine Result

```json
{
  "ok": true,
  "errors": [],
  "policy_id": "cpu1-local-upload-parser-storage-policy",
  "contract": {
    "adapter_id": "lpa1-synthetic-local-parser-adapter-contract",
    "source_kind": "synthetic_fixture",
    "output_mode": "structured_facts_only",
    "handoff_target": "local_parser_prototype_input",
    "allowed_document_types": [
      "contract"
    ],
    "allowed_domains": [
      "KIFRS1116"
    ],
    "required_extracted_fields": [
      "party",
      "lease_term",
      "payment_schedule"
    ],
    "forbidden_outputs": [
      "raw private file",
      "parsed private body",
      "OCR text",
      "private embedding",
      "source document excerpt"
    ],
    "required_operator_checks": [
      "verify local-only paths are gitignored before receiving any file",
      "delete quarantined raw files before close",
      "record deletion attestation without source body text",
      "run public-safe gate before committing any derived artifact"
    ],
    "reads_real_files": false,
    "runs_ocr": false,
    "stores_source_body": false,
    "stores_private_embedding": false,
    "deletion_automation": false
  },
  "prototype_input": {
    "parser_run_id": "lpa1-contract-handoff-1116",
    "source_stub": "local-private://dry-run/lpa1-contract-handoff-1116",
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
    "parser_run_id": "lpa1-contract-handoff-1116",
    "fixture": {
      "fixture_id": "lpa1-contract-handoff-1116",
      "parser_mode": "structured_facts_only",
      "document_type": "contract",
      "source_stub": "local-private://dry-run/lpa1-contract-handoff-1116",
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
      "case_id": "lpa1-contract-handoff-1116",
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
      "case_id": "lpa1-contract-handoff-1116",
      "domain": "KIFRS1116",
      "route": "kifrs1116_review_pack",
      "status": "candidate",
      "reason": "minimum structured facts are present for a review-pack draft candidate",
      "missing_facts": []
    },
    "deletion_attestation": {
      "attestation_id": "lpa1-contract-handoff-1116-deletion-attestation",
      "fixture_id": "lpa1-contract-handoff-1116",
      "source_stub": "local-private://dry-run/lpa1-contract-handoff-1116",
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
    "case_id": "lpa1-contract-handoff-1116",
    "domain": "KIFRS1116",
    "route": "kifrs1116_review_pack",
    "status": "candidate",
    "reason": "minimum structured facts are present for a review-pack draft candidate",
    "missing_facts": []
  },
  "report_path": "docs\\reports\\2026-07-05-lpa1-local-parser-adapter-contract.md",
  "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or local parser adapter dry-run gate"
}
```
