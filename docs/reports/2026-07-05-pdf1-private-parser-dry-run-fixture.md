# PDF1 Private Parser Dry-Run Fixture

> Scope: synthetic, public-safe parser input/output contract for future client-private parser work.

## 한 줄 결론

A future private parser now has a dry-run fixture contract: it may output redacted structured facts that route to a review-pack candidate, but it still may not store raw files, OCR text, parsed bodies, identifiers, or embeddings.

## Fixture

### Client-Private Parser Dry-Run Fixture - pdf1-synthetic-lease-contract-dry-run

- Parser mode: structured_facts_only
- Document type: contract
- Source stub: local-private://dry-run/synthetic-lease-contract
- Expected domain: KIFRS1116
- Allowed output level: review_pack_summary
- Redaction status: reviewed_public_safe
- Reviewer original-document check: True
- Deletion attestation: synthetic dry-run raw file deleted before report write

## Structured Facts

| Field | Value |
|---|---|
| lease_term | 5 years |
| party | lessee |
| payment_schedule | monthly fixed payments |

## Boundary

- This fixture does not contain raw file content, OCR text, parsed source body, customer identifiers, or embeddings.
- It models the public-safe output contract a future local parser must satisfy.
- It must remain synthetic and repo-safe.

## Route Result

- Route: kifrs1116_review_pack
- Status: candidate
- Missing facts: []

## What This Enables

- A future local parser can be tested against a known output contract before touching private files.
- The review-pack routing bridge can be checked from parser-shaped structured facts.
- The public repo keeps only synthetic fixture metadata and redacted output.

## Still Not Implemented

- file upload UI
- OCR
- real private document parser
- local deletion attestation automation
- private embedding/index namespace

## Next Leaf

real-accountant-session RS2/RS3 evidence capture, or local deletion attestation gate

## Machine Result

```json
{
  "ok": true,
  "errors": [],
  "policy_id": "cpu1-local-upload-parser-storage-policy",
  "fixture": {
    "fixture_id": "pdf1-synthetic-lease-contract-dry-run",
    "parser_mode": "structured_facts_only",
    "document_type": "contract",
    "source_stub": "local-private://dry-run/synthetic-lease-contract",
    "expected_domain": "KIFRS1116",
    "structured_facts": {
      "party": "lessee",
      "lease_term": "5 years",
      "payment_schedule": "monthly fixed payments"
    },
    "allowed_output_level": "review_pack_summary",
    "redaction_status": "reviewed_public_safe",
    "reviewer_original_document_check": true,
    "deletion_attestation": "synthetic dry-run raw file deleted before report write"
  },
  "redacted_summary": {
    "case_id": "pdf1-synthetic-lease-contract-dry-run",
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
    "case_id": "pdf1-synthetic-lease-contract-dry-run",
    "domain": "KIFRS1116",
    "route": "kifrs1116_review_pack",
    "status": "candidate",
    "reason": "minimum structured facts are present for a review-pack draft candidate",
    "missing_facts": []
  },
  "report_path": "docs\\reports\\2026-07-05-pdf1-private-parser-dry-run-fixture.md",
  "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or local deletion attestation gate"
}
```
