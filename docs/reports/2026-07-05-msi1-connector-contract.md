# MSI1 Connector Contract and Source Manifest

> Horizon: `multi-source-ingestion-pipeline`
> Step: MSI1 — Connector Contract and Source Manifest
> Date: 2026-07-05

## 한 줄 결론

첫 ingestion pipeline은 두 record type만 정식 지원한다:

1. `document_metadata` — KASB/FSS 해석자료, 법령 locator 같은 문서형 source를 body 없이 등록한다.
2. `structured_fact` — OpenDART/XBRL/재무제표 line item 같은 수치형 source를 structured fact로 등록한다.

법령 locator는 별도 pipeline으로 분리하지 않고 MSI2에서는 `document_metadata`의 locator subtype으로 다룬다.
client-private intake와 audit standards body ingestion은 이번 horizon 밖으로 둔다.

## Contract Principles

1. Public repo에는 metadata, schema, synthetic fixture만 둔다.
2. Connector output에는 protected body를 암시하는 field를 넣지 않는다.
3. 모든 record는 `source_id`, `body_storage_policy`, `citation_role`, `locator`를 가진다.
4. `source_id`는 `docs/authority/sources.json`에 등록된 id여야 한다.
5. K-IFRS 문단 DB는 계속 primary evidence이고, 외부 source는 supporting/boundary/fact evidence로 분리한다.

## Common Connector Envelope

모든 connector record는 아래 envelope를 가져야 한다.

| Field | Required | Meaning |
|---|---:|---|
| `record_type` | yes | `document_metadata` or `structured_fact` |
| `connector_id` | yes | connector implementation id, for example `kasb-fss-interpretive-catalog` |
| `connector_version` | yes | contract-compatible connector version |
| `source_id` | yes | existing authority source registry id |
| `source_class` | yes | source class from AS3/AS4, for example `interpretive_accounting_material` |
| `namespace` | yes | retrieval/index namespace, for example `external.kasb_fss` |
| `body_storage_policy` | yes | one AS3 storage policy label |
| `citation_role` | yes | allowed evidence role for downstream answer composer |
| `locator` | yes | URL, registry id, filing id, article locator, or local-private label |
| `retrieved_at` | yes | connector run timestamp or fixture generation timestamp |
| `public_manifest_safe` | yes | must be `true` for committed manifest examples |
| `provenance` | yes | who produced the record and from which source metadata |
| `warnings` | no | machine-readable caveats, never source body |

Allowed `body_storage_policy` values:

- `public_metadata_only`
- `local_private_body`
- `local_private_structured_data`
- `public_synthetic_fixture`
- `no_store_link_only`
- `no_store_handoff`

Allowed `citation_role` values for MSI2/MSI3:

- `supporting_interpretation`
- `legal_boundary`
- `collection_seed`
- `fact_evidence`

`fact_evidence` is new for ingestion manifests. It should not be added to `source_pack` authority use cases yet,
because it is evidence about company facts, not accounting authority.

## Record Type 1: `document_metadata`

Use for KASB/FSS interpretive catalog entries, law/regulation locators, audit standard metadata, and other document
sources where body text is not committed.

Required fields:

| Field | Meaning |
|---|---|
| `document_id` | stable id inside the connector namespace |
| `title` | document title or registry title |
| `publisher` | source publisher |
| `document_type` | `interpretive_material`, `law_locator`, `audit_standard_metadata`, or `supporting_material` |
| `publication_date` | publication date if known, otherwise `null` |
| `effective_date` | effective date if relevant, otherwise `null` |
| `related_standards` | K-IFRS standard ids if known; empty list is allowed |
| `topics` | short author-written topic tags |
| `chunk_strategy` | `metadata_only`, `private_qna_item`, `private_section`, or `law_article_locator` |
| `allowed_use` | `supporting_interpretation`, `legal_boundary`, or `collection_seed` |

MSI2 public fixtures must use:

- `body_storage_policy`: `public_metadata_only` or `no_store_link_only`
- `chunk_strategy`: `metadata_only` or `law_article_locator`
- no body/cache/path fields beyond public locator labels

## Record Type 2: `structured_fact`

Use for OpenDART-like facts, XBRL-derived line items, synthetic financial statement samples, and audit analytical
inputs.

Required fields:

| Field | Meaning |
|---|---|
| `fact_id` | stable fact id |
| `company_id` | corp code, ticker, or synthetic company id |
| `filing_id` | filing/report id or synthetic filing id |
| `period` | reporting period |
| `statement_type` | for example `financial_position`, `profit_or_loss`, `cash_flows` |
| `line_item` | normalized line item name |
| `value` | numeric value |
| `unit` | currency/unit |
| `dimensions` | optional structured dimensions, empty object allowed |
| `filing_locator` | official filing locator or synthetic locator |
| `quality_flags` | list of parser/fixture caveats |

MSI3 public fixtures must use:

- `body_storage_policy`: `public_synthetic_fixture`
- synthetic company/filing ids unless a later review marks real public metadata as safe
- no raw XML/XBRL dump, filing body, downloaded document body, API key, token, or credential

## Public Manifest Proposal

MSI2 should introduce the first public-safe manifest example at:

- `docs/ingestion/source_manifest.example.json`

Suggested top-level shape:

```json
{
  "version": 1,
  "policy": {
    "public_manifest_safe": true,
    "body_text_committed": false,
    "forbidden_fields_rejected": true
  },
  "records": []
}
```

The validator should live behind:

- `kifrs/ingestion/manifest.py`
- `scripts/validate_ingestion_manifest.py`

## Validator Rules for MSI2/MSI3

The ingestion manifest validator should reject:

- missing common envelope fields;
- unknown `record_type`;
- unknown `source_id`;
- `body_storage_policy` outside AS3 labels;
- `citation_role` outside MSI allowed roles;
- lane-specific missing fields;
- any forbidden field name recursively:
  - `body`
  - `text`
  - `content`
  - `full_text`
  - `source_body`
  - `excerpt`
  - `quote`
  - `embedding`
  - `raw_xml`
  - `xbrl_dump`
  - `pdf_bytes`
  - `api_key`
  - `token`
  - `credential`

The validator should accept short author-written `notes` or `warnings`, but those fields must be treated as metadata,
not copied source body.

## MSI2 Fixture Scope

MSI2 should implement only `document_metadata`:

- 2-3 metadata-only records;
- at least one KASB/FSS-style interpretive source;
- optionally one law locator record;
- all records body-free and public-safe;
- unit tests proving a body-like field is rejected.

## MSI3 Fixture Scope

MSI3 should implement only `structured_fact`:

- synthetic OpenDART-like facts;
- no external API call;
- no real raw filing body;
- fact-level citation locator;
- tests proving raw dump/API-key fields are rejected.

## Decision Log

| Decision | Result |
|---|---|
| First implementation record types | `document_metadata` and `structured_fact` only |
| Law connector shape | locator subtype under `document_metadata` for now |
| Body ingestion | out of scope for this horizon |
| External API calls | out of scope until synthetic fixtures and validators pass |
| Public manifest path | `docs/ingestion/source_manifest.example.json` starting MSI2 |

