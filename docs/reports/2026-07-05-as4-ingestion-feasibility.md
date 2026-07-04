# AS4 Ingestion Feasibility Matrix

> Horizon: `authority-source-map`
> Step: AS4 — Ingestion Feasibility Matrix
> Date: 2026-07-05

## 한 줄 결론

다음 ingestion pipeline은 하나의 parser로 해결되지 않는다. **KASB/FSS/law/audit sources는 document RAG
lane**, **DART/OpenDART/XBRL은 structured data lane**, **client-private은 local-private lane**으로
분리해야 한다.

## Feasibility Matrix

| Source class | Storage policy | Fetch | Parse | Chunk | Embed | Index | Feasibility | Lane |
|---|---|---|---|---|---|---|---|---|
| `primary_accounting_standard` | `local_private_body` | already local/private | already parsed | paragraph-level | existing embeddings | existing DB/FTS/vector | high, existing | `document_rag` |
| `interpretive_accounting_material` | `public_metadata_only` now, `local_private_body` later | web/manual metadata first | PDF/HTML likely mixed | doc section / Q&A item | yes, private body only | source namespace | medium | `document_rag` |
| `primary_audit_standard` | `public_metadata_only` now, `local_private_body` later | manual/web metadata first | PDF/HTML likely | standard/paragraph/section | yes, private body only | F-AUD namespace | medium | `document_rag` |
| `law_regulation` | `no_store_link_only` public, `local_private_body` if approved | official law locator/API/web | article text if allowed locally | article/subarticle | optional | legal namespace | medium-high | `document_rag` or law API |
| `filing_data` | `public_synthetic_fixture` public, `local_private_structured_data` for real cache | OpenDART/API/manual filing id | XML/XBRL/table parser | line-item facts, not prose chunks | usually no | structured tables | high for structured samples | `structured_data` |
| `client_private` | `no_store_handoff` public, local private only for real cases | local upload/path only | PDF/docx/xlsx/csv parser | fact blocks / workpaper sections | yes, local-private | private case namespace | medium, security-dependent | `local_private_case_facts` |
| `supporting_material` | `no_store_link_only` | URL/manual metadata | avoid body by default | metadata note only | no by default | metadata registry | low as RAG source | `metadata_support_only` |

## Lane Definitions

### Lane A. `document_rag`

For:

- K-IFRS private DB
- KASB/FSS interpretive material
- audit standards
- law/regulation when body text is locally allowed

Minimum connector fields:

- `source_id`
- `source_class`
- `namespace`
- `document_id`
- `title`
- `publisher`
- `publication_date`
- `effective_date`
- `locator`
- `body_storage_policy`
- `citation_role`
- `chunk_strategy`

Chunk strategy:

- standards: paragraph/section
- interpretive material: Q&A item / issue-response / section
- audit standards: standard paragraph / requirement / application material
- law: article / paragraph / subparagraph

### Lane B. `structured_data`

For:

- DART/OpenDART
- XBRL
- financial statements
- audit analytical procedure inputs

Minimum connector fields:

- `source_id`
- `source_class`
- `namespace`
- `company_id`
- `filing_id`
- `period`
- `statement_type`
- `line_item`
- `value`
- `unit`
- `locator`
- `retrieved_at`
- `body_storage_policy`

Index strategy:

- relational/columnar table first
- vector embedding only for note/disclosure prose if allowed
- citation should point to filing locator + line item, not an invented paragraph

### Lane C. `local_private_case_facts`

For:

- contracts
- accounting policy docs
- TB
- workpapers
- management memo

Minimum connector fields:

- `case_id`
- `document_id`
- `document_type`
- `fact_label`
- `fact_value`
- `source_locator`
- `redaction_status`
- `body_storage_policy`
- `allowed_output_level`

Index strategy:

- local/private only
- redact before public report
- answer composer must label as `Client-provided facts`

### Lane D. `metadata_support_only`

For:

- firm public guides
- articles
- education material where body reuse is not allowed

Minimum connector fields:

- `source_id`
- `title`
- `publisher`
- `url`
- `why_supporting`
- `body_storage_policy=no_store_link_only`

Index strategy:

- do not embed body by default
- use as source discovery/background only

## Source Class Readiness

| Source class | Ready for connector design? | Reason |
|---|---|---|
| K-IFRS primary | yes | existing local DB/RAG already works |
| KASB/FSS interpretive | yes, metadata-first | high product value, but body policy must stay private |
| Law/regulation | yes, locator-first | article locator and official URL can drive a safe prototype |
| DART/OpenDART | yes, structured sample | high value for statement draft/audit analytics |
| Audit standards | later | important, but F-AUD workflows are less mature than F-ACC |
| Client-private | later with redaction | requires privacy/security UX and case intake |
| Supporting material | no connector yet | low authority, metadata only |

## Candidate Connectors for AS5

AS5 should choose from these:

| Candidate | Lane | Why |
|---|---|---|
| `kasb-fss-interpretive-catalog` | Document RAG metadata-first | directly improves accounting treatment explanations |
| `opendart-structured-financials` | Structured Data | connects statement draft and audit analytics to real company facts |
| `law-regulation-locator` | Document RAG / API locator | needed for legal boundary answers |
| `audit-standards-namespace` | Document RAG | needed before serious F-AUD workflow expansion |
| `client-private-case-intake` | Local-private | needed for real PoC but has privacy/security scope |

## Recommendation for First Implementation Horizon

The next horizon should not build all lanes at once. It should start with a connector interface that supports both:

1. metadata-only document source,
2. structured fact source.

Reason:

- KASB/FSS catalog needs metadata-only document handling.
- OpenDART needs structured fact handling.
- These two together cover the biggest product gap: accounting interpretation context + actual company data.

## AS4 Decision

AS4 is complete enough to move to AS5.

AS5 should select the first 1~3 connector candidates and define the entry point for the next horizon,
`multi-source-ingestion-pipeline`.
