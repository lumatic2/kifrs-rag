# ESLM1 External Source Connector Live-Metadata Decision Gate

> Scope: decide whether the KASB/FSS connector may implement live metadata probes.

## 한 줄 결론

`kasb-fss-interpretive-catalog` may proceed to a live-metadata probe scaffold. The decision allows checking public locator metadata only; it still forbids source body fetch, cache, chunking, embeddings, indexing, and answer-time body use.

## Decision

- ok: True
- connector id: `kasb-fss-interpretive-catalog`
- decision: `allow_live_metadata_probe_scaffold`
- live metadata probe allowed: True
- live network probe allowed: True
- live body fetch allowed: False
- body cache allowed: False
- chunking allowed: False
- embedding allowed: False
- indexing allowed: False
- answer-time body use allowed: False

## Connector Targets

| Item | Source | Publisher | URL | Body Stored |
|---|---|---|---|---|
| kasb-implementation-material-index | kasb-interpretation-material | KASB | https://www.kasb.or.kr/ | False |
| fss-accounting-inquiry-index | fss-accounting-inquiry | Financial Supervisory Service | https://www.fss.or.kr/ | False |

## Boundary

- This decision gate performs no live network request itself.
- It relies on the prior LEV1 metadata-only live validation report.
- The next implementation may check locator/status/final URL/content type metadata only.
- It must not store source body, copied excerpts, raw HTML, chunks, embeddings, or external body indexes.

## Next Leaf

real-accountant-session RS2/RS3 evidence capture, or external source connector live-metadata probe scaffold

## Machine Result

```json
{
  "ok": true,
  "errors": [],
  "decision_gate_id": "eslm1-external-source-connector-live-metadata-decision-gate",
  "connector_id": "kasb-fss-interpretive-catalog",
  "decision": "allow_live_metadata_probe_scaffold",
  "live_metadata_probe_allowed": true,
  "live_network_probe_allowed": true,
  "live_body_fetch_allowed": false,
  "body_cache_allowed": false,
  "chunking_allowed": false,
  "embedding_allowed": false,
  "indexing_allowed": false,
  "answer_time_body_use_allowed": false,
  "allowed_live_metadata_fields": [
    "item_id",
    "source_id",
    "publisher",
    "allowed_use",
    "url",
    "status_code",
    "final_url",
    "content_type",
    "network_checked",
    "checked_at",
    "body_text_stored"
  ],
  "forbidden_live_metadata_fields": [
    "api_key",
    "body",
    "content",
    "credential",
    "embedding",
    "excerpt",
    "full_text",
    "html",
    "pdf_bytes",
    "quote",
    "raw_html",
    "source_body",
    "text",
    "token"
  ],
  "metadata_close_gate": {
    "ok": true,
    "report_path": "docs\\reports\\2026-07-05-esmc1-external-source-connector-metadata-close-gate.md",
    "closed_scope": [
      "connector-specific policy record",
      "metadata-only source manifest dry-run",
      "forbidden-field regression for metadata dry-run records"
    ]
  },
  "live_contract": {
    "ok": true,
    "report_path": "docs\\reports\\2026-07-05-lev1-live-external-source-validation.md",
    "network_checked_by_this_gate": false,
    "target_count": 3,
    "body_text_stored": false,
    "connector_targets": [
      {
        "item_id": "kasb-implementation-material-index",
        "source_id": "kasb-interpretation-material",
        "publisher": "KASB",
        "allowed_use": "supporting_interpretation",
        "url": "https://www.kasb.or.kr/",
        "network_checked": false,
        "body_text_stored": false,
        "ok": null,
        "status_code": null,
        "final_url": "",
        "content_type": "",
        "error": "network_not_enabled"
      },
      {
        "item_id": "fss-accounting-inquiry-index",
        "source_id": "fss-accounting-inquiry",
        "publisher": "Financial Supervisory Service",
        "allowed_use": "supporting_interpretation",
        "url": "https://www.fss.or.kr/",
        "network_checked": false,
        "body_text_stored": false,
        "ok": null,
        "status_code": null,
        "final_url": "",
        "content_type": "",
        "error": "network_not_enabled"
      }
    ]
  },
  "required_prior_live_validation_report": "docs\\reports\\2026-07-05-lev1-live-external-source-validation.md",
  "report_path": "docs\\reports\\2026-07-05-eslm1-external-source-connector-live-metadata-decision-gate.md",
  "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or external source connector live-metadata probe scaffold"
}
```
