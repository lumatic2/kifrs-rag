# CP2 Local Parser Runtime Contract

> Scope: CP2 runtime contract for structured-facts-only client-private parser outputs.

## Result

- ok: True
- horizon: `client-private-parser-runtime`
- milestone: `CP2`
- public safe: True
- next leaf: `CP3_client_private_evidence_adapter`

## Runtime Contract

# Runtime Client-Private Parser Contract - lpa1-contract-handoff-1116

- source label: contract:lpa1-contract-handoff-1116
- document type: contract
- expected domain: KIFRS1116
- deletion policy: manual_before_commit
- local only: True

## Structured Fact Keys

- lease_term
- party
- payment_schedule

## Review Questions

- minimum structured facts are present for a review-pack draft candidate

## Boundary

- Runtime contract carries structured facts, source label, review questions, and deletion policy only.
- It does not carry raw files, parsed private body, OCR text, private embeddings, or client identifiers.


## Boundary Meaning

- Runtime receives structured fact keys, source label, review questions, and deletion policy only.
- Runtime does not receive raw private files, parsed private body, OCR text, private embeddings, or client identifiers.
- Full structured facts remain local until CP3 converts approved fields into `client_private_fact` references.

## Machine Result

```json
{
  "title": "CP2 Local Parser Runtime Contract",
  "ok": true,
  "horizon": "client-private-parser-runtime",
  "milestone": "CP2",
  "contract": {
    "parser_run_id": "lpa1-contract-handoff-1116",
    "source_label": "contract:lpa1-contract-handoff-1116",
    "document_type": "contract",
    "expected_domain": "KIFRS1116",
    "structured_fact_keys": [
      "lease_term",
      "party",
      "payment_schedule"
    ],
    "review_questions": [
      "minimum structured facts are present for a review-pack draft candidate"
    ],
    "deletion_policy": "manual_before_commit",
    "local_only": true
  },
  "validation_errors": [],
  "public_safe": true,
  "next_leaf": "CP3_client_private_evidence_adapter",
  "report_path": "docs/reports/2026-07-05-cp2-local-parser-runtime-contract.md"
}
```
