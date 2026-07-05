# SBI1 Source Class Selection

> Scope: choose the first controlled non-IFRS source-body lane and document its authorization boundary.

## 한 줄 결론

Select `interpretive_accounting_material` as the first controlled source-body lane. Because body-level authorization is absent, implementation remains synthetic-body-only until a source-specific authorization record exists.

## Selected Lane

- source class: `interpretive_accounting_material`
- source ids: kasb-interpretation-material, fss-accounting-inquiry
- lane type: `document_body_controlled_lane`
- authorization status: `not_authorized_for_body`
- implementation mode: `synthetic_body_only`
- fallback plan: Use synthetic_body_only until explicit source-specific authorization exists; keep K-IFRS primary evidence unchanged.

## Candidate Comparison

| Source Class | Source IDs | Lane Type | Score | Authorization | Mode | Rationale |
|---|---|---|---|---|---|---|
| interpretive_accounting_material | kasb-interpretation-material, fss-accounting-inquiry | `document_body_controlled_lane` | 10 | `not_authorized_for_body` | `synthetic_body_only` | Highest fit for controlled source-body ingestion: KASB/FSS-style guidance is useful as supporting interpretation but cannot be copied without authorization. |
| law_regulation | commercial-act-capital | `law_locator` | 5 | `not_authorized_for_body` | `locator_or_synthetic_body_only` | Useful legal boundary evidence, but locator-first handling is safer than body chunking. |
| filing_data | opendart-structured-financials | `structured_fact` | 3 | `metadata_or_api_contract_only` | `structured_fact_only` | Valuable for company facts, but not a source-body ingestion lane. |
| client_private | client-private-local | `local_private_case_facts` | 5 | `user_owned_local_only` | `structured_facts_only` | Important product path, but just closed under the local parser prototype horizon. |

## Allowed Fields

- source_id
- title
- issuer
- publication_date
- url_or_locator
- topic_tags
- synthetic_body
- citation_role
- authority_level

## Forbidden Fields

- copied external document text
- full article text
- PDF body cache
- embedding dump
- API secret
- client-private payload

## Boundary

- SBI1 does not fetch, scrape, cache, chunk, or embed external body text.
- SBI1 selects the controlled lane and authorization boundary only.
- K-IFRS paragraph evidence remains primary.

## Next Leaf

SBI2_source_policy_record

## Machine Result

```json
{
  "title": "SBI1 Source Class Selection",
  "ok": true,
  "selected_source_class": "interpretive_accounting_material",
  "selected_source_ids": [
    "kasb-interpretation-material",
    "fss-accounting-inquiry"
  ],
  "selected_lane_type": "document_body_controlled_lane",
  "authorization_status": "not_authorized_for_body",
  "implementation_mode": "synthetic_body_only",
  "allowed_fields": [
    "source_id",
    "title",
    "issuer",
    "publication_date",
    "url_or_locator",
    "topic_tags",
    "synthetic_body",
    "citation_role",
    "authority_level"
  ],
  "forbidden_fields": [
    "copied external document text",
    "full article text",
    "PDF body cache",
    "embedding dump",
    "API secret",
    "client-private payload"
  ],
  "fallback_plan": "Use synthetic_body_only until explicit source-specific authorization exists; keep K-IFRS primary evidence unchanged.",
  "candidates": [
    {
      "source_class": "interpretive_accounting_material",
      "source_ids": [
        "kasb-interpretation-material",
        "fss-accounting-inquiry"
      ],
      "lane_type": "document_body_controlled_lane",
      "product_value": 5,
      "body_lane_fit": 5,
      "authorization_status": "not_authorized_for_body",
      "implementation_mode": "synthetic_body_only",
      "rationale": "Highest fit for controlled source-body ingestion: KASB/FSS-style guidance is useful as supporting interpretation but cannot be copied without authorization.",
      "score": 10
    },
    {
      "source_class": "law_regulation",
      "source_ids": [
        "commercial-act-capital"
      ],
      "lane_type": "law_locator",
      "product_value": 4,
      "body_lane_fit": 3,
      "authorization_status": "not_authorized_for_body",
      "implementation_mode": "locator_or_synthetic_body_only",
      "rationale": "Useful legal boundary evidence, but locator-first handling is safer than body chunking.",
      "score": 5
    },
    {
      "source_class": "filing_data",
      "source_ids": [
        "opendart-structured-financials"
      ],
      "lane_type": "structured_fact",
      "product_value": 4,
      "body_lane_fit": 1,
      "authorization_status": "metadata_or_api_contract_only",
      "implementation_mode": "structured_fact_only",
      "rationale": "Valuable for company facts, but not a source-body ingestion lane.",
      "score": 3
    },
    {
      "source_class": "client_private",
      "source_ids": [
        "client-private-local"
      ],
      "lane_type": "local_private_case_facts",
      "product_value": 5,
      "body_lane_fit": 2,
      "authorization_status": "user_owned_local_only",
      "implementation_mode": "structured_facts_only",
      "rationale": "Important product path, but just closed under the local parser prototype horizon.",
      "score": 5
    }
  ],
  "missing_source_ids": [],
  "completed_milestone": "SBI1",
  "next_leaf": "SBI2_source_policy_record",
  "report_path": "docs/reports/2026-07-05-sbi1-source-class-selection.md"
}
```
