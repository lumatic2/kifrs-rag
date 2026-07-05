# RLP2 Local Fixture Parser Adapter

> Scope: local-safe fixture adapter that converts fixture-like input into structured facts and review questions.

## 한 줄 결론

RLP2 adds a local fixture adapter path. It accepts fixture-shaped structured facts, strips extra operator-only candidates, emits the contract-required structured facts, generates review questions, and routes the case through the existing local parser prototype. It still does not read real files, copy raw text, run OCR, include source excerpts, or create private embeddings.

## Adapter Result

### Local Fixture Parser Adapter Result - rlp2-local-fixture-lease-contract

- OK: True
- Route: kifrs1116_review_pack
- Route status: candidate
- Structured fact count: 3
- Review question count: 5

## Structured Facts

| Field | Value |
|---|---|
| lease_term | 5 years with renewal option excluded from structured facts |
| party | lessee |
| payment_schedule | monthly fixed payments |

## Review Questions

- Confirm the original local document matches each structured fact before final review.
- Confirm no raw private text is needed to support the draft review-pack route.
- Confirm the lease party is correctly identified as lessee.
- Confirm the lease term evidence supports 5 years with renewal option excluded from structured facts.
- Confirm the payment schedule evidence supports monthly fixed payments.

## Boundary

- This adapter accepts fixture-shaped structured facts only.
- It does not copy raw text, run OCR, include source excerpts, or create private embeddings.
- The reviewer must confirm the original local document outside this repo before relying on the review pack.

## What Changed From RLP1

- RLP1 only inventoried reusable parser assets.
- RLP2 now proves a fixture-like input can become structured facts plus human review questions.
- The output is still public-safe and structured-facts-only.

## Still Not Implemented

- real private-file parser
- OCR
- upload UI
- private embedding/index namespace
- deletion automation beyond the existing attestation contract

## Next Leaf

RLP3_deletion_automation_simulation

## Machine Result

```json
{
  "ok": true,
  "errors": [],
  "policy_id": "cpu1-local-upload-parser-storage-policy",
  "contract_id": "lpa1-synthetic-local-parser-adapter-contract",
  "adapter_input": {
    "adapter_run_id": "rlp2-local-fixture-lease-contract",
    "source_stub": "local-private://fixture/rlp2-local-fixture-lease-contract",
    "document_type": "contract",
    "expected_domain": "KIFRS1116",
    "structured_fact_candidates": {
      "party": "lessee",
      "lease_term": "5 years with renewal option excluded from structured facts",
      "payment_schedule": "monthly fixed payments",
      "ignored_note": "operator-only note intentionally excluded from structured facts"
    },
    "operator_ack": "fixture-structured-facts-only-public-safe",
    "raw_fixture_text_present": false,
    "ocr_text_present": false,
    "source_excerpt_present": false,
    "embedding_present": false
  },
  "adapter_result": {
    "adapter_run_id": "rlp2-local-fixture-lease-contract",
    "structured_facts": {
      "party": "lessee",
      "lease_term": "5 years with renewal option excluded from structured facts",
      "payment_schedule": "monthly fixed payments"
    },
    "review_questions": [
      "Confirm the original local document matches each structured fact before final review.",
      "Confirm no raw private text is needed to support the draft review-pack route.",
      "Confirm the lease party is correctly identified as lessee.",
      "Confirm the lease term evidence supports 5 years with renewal option excluded from structured facts.",
      "Confirm the payment schedule evidence supports monthly fixed payments."
    ],
    "prototype_result": {
      "parser_run_id": "rlp2-local-fixture-lease-contract",
      "fixture": {
        "fixture_id": "rlp2-local-fixture-lease-contract",
        "parser_mode": "structured_facts_only",
        "document_type": "contract",
        "source_stub": "local-private://dry-run/rlp2-local-fixture-lease-contract",
        "expected_domain": "KIFRS1116",
        "structured_facts": {
          "party": "lessee",
          "lease_term": "5 years with renewal option excluded from structured facts",
          "payment_schedule": "monthly fixed payments"
        },
        "allowed_output_level": "review_pack_summary",
        "redaction_status": "reviewed_public_safe",
        "reviewer_original_document_check": true,
        "deletion_attestation": "synthetic parser prototype source deleted before report write"
      },
      "redacted_summary": {
        "case_id": "rlp2-local-fixture-lease-contract",
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
          "lease_term": "5 years with renewal option excluded from structured facts",
          "party": "lessee",
          "payment_schedule": "monthly fixed payments"
        }
      },
      "route": {
        "case_id": "rlp2-local-fixture-lease-contract",
        "domain": "KIFRS1116",
        "route": "kifrs1116_review_pack",
        "status": "candidate",
        "reason": "minimum structured facts are present for a review-pack draft candidate",
        "missing_facts": []
      },
      "deletion_attestation": {
        "attestation_id": "rlp2-local-fixture-lease-contract-deletion-attestation",
        "fixture_id": "rlp2-local-fixture-lease-contract",
        "source_stub": "local-private://dry-run/rlp2-local-fixture-lease-contract",
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
    "ok": true
  },
  "route": {
    "case_id": "rlp2-local-fixture-lease-contract",
    "domain": "KIFRS1116",
    "route": "kifrs1116_review_pack",
    "status": "candidate",
    "reason": "minimum structured facts are present for a review-pack draft candidate",
    "missing_facts": []
  },
  "review_questions": [
    "Confirm the original local document matches each structured fact before final review.",
    "Confirm no raw private text is needed to support the draft review-pack route.",
    "Confirm the lease party is correctly identified as lessee.",
    "Confirm the lease term evidence supports 5 years with renewal option excluded from structured facts.",
    "Confirm the payment schedule evidence supports monthly fixed payments."
  ],
  "structured_fact_keys": [
    "lease_term",
    "party",
    "payment_schedule"
  ],
  "report_path": "docs\\reports\\2026-07-05-rlp2-local-fixture-parser-adapter.md",
  "next_leaf": "RLP3_deletion_automation_simulation"
}
```
