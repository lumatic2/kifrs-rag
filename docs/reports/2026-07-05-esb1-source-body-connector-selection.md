# ESB1 Source-Body Connector Selection And Policy Gate

> Scope: source-body connector class selection before any live body ingestion.

## 한 줄 결론

Select `interpretive_accounting_material` as the first connector lane, but keep live fetching, body chunking, and embedding blocked until source-specific review and explicit authorization exist.

## Selected Lane

- Source class: `interpretive_accounting_material`
- Authority role: `supporting_interpretive_evidence`
- Implementation status: `selected_for_ESB2`
- Authorization mode: `synthetic_dry_run_now; source_specific_local_private_body_only_after_review`
- Public report mode: metadata, locator, policy, schema, synthetic snippet labels, and metrics only

## Candidate Ranking

| Source Class | Role | Status | Score |
|---|---|---|---:|
| interpretive_accounting_material | supporting_interpretive_evidence | selected_for_ESB2 | 5 |
| law_regulation | legal_supporting_evidence | defer | 3 |
| filing_disclosure | company_disclosure_evidence | defer | 2 |
| client_private_policy | client_fact_or_policy_evidence | defer | 1 |

## Public-Safe Policy

Public reports may store:
- `source_class`
- `authority_role`
- `publisher_class`
- `canonical_locator`
- `policy_status`
- `synthetic_fixture_id`
- `chunk_strategy`
- `retrieval_metadata`
- `created_by_script`

Local-only fields after source review:
- `body_cache_path`
- `chunk_store_path`
- `local_index_namespace`
- `deletion_command`

Blocked by ESB1:
- live fetching: False
- body chunking: False
- embedding: False
- blocked public field count: 9

## Checks

| Check | OK |
|---|---|
| selected_class_present | True |
| live_fetching_blocked | True |
| public_body_payload_blocked | True |
| authorization_boundary_explicit | True |
| allowed_public_fields_do_not_include_blocked_fields | True |
| next_milestone_named | True |

## Errors

- none

## Next Leaf

- `ESB2_synthetic_connector_body_fixture_contract`

## Machine Result

```json
{
  "title": "ESB1 Source-Body Connector Selection And Policy Gate",
  "ok": true,
  "horizon": "external-source-body-connector-expansion",
  "completed_milestone": "ESB1",
  "selected_source_class": {
    "source_class": "interpretive_accounting_material",
    "authority_role": "supporting_interpretive_evidence",
    "product_value": "Adds regulator or standard-setter interpretation around K-IFRS decision-prep work without replacing primary K-IFRS paragraphs.",
    "authorization_mode": "synthetic_dry_run_now; source_specific_local_private_body_only_after_review",
    "public_report_mode": "metadata, locator, policy, schema, synthetic snippet labels, and metrics only",
    "implementation_status": "selected_for_ESB2",
    "score": 5
  },
  "candidates": [
    {
      "source_class": "interpretive_accounting_material",
      "authority_role": "supporting_interpretive_evidence",
      "product_value": "Adds regulator or standard-setter interpretation around K-IFRS decision-prep work without replacing primary K-IFRS paragraphs.",
      "authorization_mode": "synthetic_dry_run_now; source_specific_local_private_body_only_after_review",
      "public_report_mode": "metadata, locator, policy, schema, synthetic snippet labels, and metrics only",
      "implementation_status": "selected_for_ESB2",
      "score": 5
    },
    {
      "source_class": "law_regulation",
      "authority_role": "legal_supporting_evidence",
      "product_value": "Useful for commercial law and disclosure boundaries but needs source-specific legal citation policy first.",
      "authorization_mode": "requires_source_specific_review",
      "public_report_mode": "metadata and locator only until policy is expanded",
      "implementation_status": "defer",
      "score": 3
    },
    {
      "source_class": "filing_disclosure",
      "authority_role": "company_disclosure_evidence",
      "product_value": "Useful for comparable disclosure review, but XBRL or filing payload storage needs separate boundary tests.",
      "authorization_mode": "requires_source_specific_review",
      "public_report_mode": "metadata, issuer class, and locator only",
      "implementation_status": "defer",
      "score": 2
    },
    {
      "source_class": "client_private_policy",
      "authority_role": "client_fact_or_policy_evidence",
      "product_value": "High product value, but belongs behind private parser authorization and deletion controls.",
      "authorization_mode": "explicit_local_private_authorization_required",
      "public_report_mode": "structured fact labels and redaction status only",
      "implementation_status": "defer",
      "score": 1
    }
  ],
  "policy": {
    "public_reports_may_store": [
      "source_class",
      "authority_role",
      "publisher_class",
      "canonical_locator",
      "policy_status",
      "synthetic_fixture_id",
      "chunk_strategy",
      "retrieval_metadata",
      "created_by_script"
    ],
    "local_only_after_source_review": [
      "body_cache_path",
      "chunk_store_path",
      "local_index_namespace",
      "deletion_command"
    ],
    "blocked_public_field_count": 9,
    "live_fetching_allowed_by_ESB1": false,
    "body_chunking_allowed_by_ESB1": false,
    "embedding_allowed_by_ESB1": false
  },
  "checks": {
    "selected_class_present": true,
    "live_fetching_blocked": true,
    "public_body_payload_blocked": true,
    "authorization_boundary_explicit": true,
    "allowed_public_fields_do_not_include_blocked_fields": true,
    "next_milestone_named": true
  },
  "errors": [],
  "next_leaf": "ESB2_synthetic_connector_body_fixture_contract",
  "report_path": "docs/reports/2026-07-05-esb1-source-body-connector-selection.md"
}
```
