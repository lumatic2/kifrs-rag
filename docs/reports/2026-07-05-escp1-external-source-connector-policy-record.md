# ESCP1 External Source Connector Policy Record

> Scope: source-specific policy record for the first external interpretive-material connector.

## 한 줄 결론

`kasb-fss-interpretive-catalog` is ready as a metadata-only connector policy target. It can support future KASB/FSS metadata dry-runs, but live body fetch, cache, chunk, embedding, indexing, and answer-time use remain disabled.

## Connector

- connector id: `kasb-fss-interpretive-catalog`
- source class: `interpretive_accounting_material`
- lane: `document_rag_metadata_first`
- citation role: `supporting_interpretation_after_kifrs_primary_evidence`
- decision: `metadata_policy_ready_live_body_ingestion_deferred`

## Source Pack Items

| Item | Source | Publisher | Use | Status | Locator |
|---|---|---|---|---|---|
| kasb-implementation-material-index | kasb-interpretation-material | KASB | supporting_interpretation | collection_seed | https://www.kasb.or.kr/ |
| fss-accounting-inquiry-index | fss-accounting-inquiry | Financial Supervisory Service | supporting_interpretation | collection_seed | https://www.fss.or.kr/ |

## Public Boundary

- public storage policy: `public_metadata_locator_schema_and_author_written_notes_only`
- local storage policy after review: `local_private_body_cache_only_after_source_specific_review_and_explicit_authorization`
- live fetch allowed: False
- body cache allowed: False
- live chunking allowed: False
- embedding allowed: False
- answer-time use allowed: False

## Required Source Checks

- confirm publisher and canonical locator for each source pack item
- check source-specific robots, terms, and license constraints before body retrieval
- keep K-IFRS paragraph DB as primary accounting evidence
- classify KASB/FSS material as supporting interpretation, not standalone treatment authority
- verify any cache, chunks, and embeddings target gitignored local/private paths
- run forbidden-field regression before committing reports or manifests
- record explicit operator authorization before live body fetch, cache, chunk, embed, or index work

## Validation

- ok: True
- source pack ok: True
- missing reports: []
- missing source pack items: []

## Next Leaf

real-accountant-session RS2/RS3 evidence capture, or external source connector metadata dry-run gate

## Machine Result

```json
{
  "ok": true,
  "errors": [],
  "policy_record": {
    "connector_id": "kasb-fss-interpretive-catalog",
    "source_pack_item_ids": [
      "kasb-implementation-material-index",
      "fss-accounting-inquiry-index"
    ],
    "source_class": "interpretive_accounting_material",
    "lane": "document_rag_metadata_first",
    "citation_role": "supporting_interpretation_after_kifrs_primary_evidence",
    "public_storage_policy": "public_metadata_locator_schema_and_author_written_notes_only",
    "local_storage_policy_after_review": "local_private_body_cache_only_after_source_specific_review_and_explicit_authorization",
    "allowed_public_fields": [
      "connector_id",
      "source_pack_item_id",
      "publisher",
      "authority_type",
      "allowed_use",
      "priority",
      "locator",
      "status",
      "keywords",
      "notes",
      "policy_decision"
    ],
    "forbidden_public_fields": [
      "api_key",
      "body",
      "content",
      "credential",
      "embedding",
      "excerpt",
      "full_text",
      "pdf_bytes",
      "quote",
      "raw_html",
      "source_body",
      "text",
      "token"
    ],
    "required_source_checks": [
      "confirm publisher and canonical locator for each source pack item",
      "check source-specific robots, terms, and license constraints before body retrieval",
      "keep K-IFRS paragraph DB as primary accounting evidence",
      "classify KASB/FSS material as supporting interpretation, not standalone treatment authority",
      "verify any cache, chunks, and embeddings target gitignored local/private paths",
      "run forbidden-field regression before committing reports or manifests",
      "record explicit operator authorization before live body fetch, cache, chunk, embed, or index work"
    ],
    "required_prerequisite_reports": [
      "as5_first_connector_recommendation",
      "live_external_source_validation",
      "external_body_policy_plan",
      "external_body_authorization_gate",
      "external_synthetic_parser_chunker_close_gate"
    ],
    "live_fetch_allowed": false,
    "body_cache_allowed": false,
    "live_chunking_allowed": false,
    "embedding_allowed": false,
    "answer_time_use_allowed": false,
    "implementation_decision": "metadata_policy_ready_live_body_ingestion_deferred",
    "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or external source connector metadata dry-run gate"
  },
  "missing_reports": [],
  "missing_source_pack_items": [],
  "source_pack_ok": true,
  "source_pack_item_summaries": [
    {
      "id": "kasb-implementation-material-index",
      "source_id": "kasb-interpretation-material",
      "publisher": "KASB",
      "authority_type": "standard-setter_guidance",
      "allowed_use": "supporting_interpretation",
      "status": "collection_seed",
      "locator": {
        "kind": "web_index",
        "url": "https://www.kasb.or.kr/"
      }
    },
    {
      "id": "fss-accounting-inquiry-index",
      "source_id": "fss-accounting-inquiry",
      "publisher": "Financial Supervisory Service",
      "authority_type": "regulatory_guidance",
      "allowed_use": "supporting_interpretation",
      "status": "collection_seed",
      "locator": {
        "kind": "web_index",
        "url": "https://www.fss.or.kr/"
      }
    }
  ],
  "report_path": "docs\\reports\\2026-07-05-escp1-external-source-connector-policy-record.md",
  "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or external source connector metadata dry-run gate"
}
```
