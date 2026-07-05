# ESLP1 External Source Connector Live-Metadata Probe Scaffold

> Scope: scaffold live metadata probes for the KASB/FSS interpretive connector.

## 한 줄 결론

`kasb-fss-interpretive-catalog` now has a live-metadata probe scaffold. It can check locator/status/final URL/content type metadata, while source body fetch, body cache, chunking, embeddings, indexing, and answer-time body use remain disabled.

## Scaffold Result

- ok: True
- connector id: `kasb-fss-interpretive-catalog`
- allow network: False
- probe record count: 2
- body text stored: False
- body cache created: False
- chunks created: False
- embeddings created: False
- index created: False
- answer-time body use enabled: False

## Probe Records

| Item | Publisher | Network | Status | Final URL | Body Stored |
|---|---|---:|---:|---|---|
| kasb-implementation-material-index | KASB | False | None | https://www.kasb.or.kr/ | False |
| fss-accounting-inquiry-index | Financial Supervisory Service | False | None | https://www.fss.or.kr/ | False |

## Boundary

- This scaffold stores metadata fields only.
- It must not store source body, copied excerpts, raw HTML, chunks, embeddings, or external body indexes.
- K-IFRS paragraph DB remains the primary accounting evidence source.

## Next Leaf

real-accountant-session RS2/RS3 evidence capture, or external source connector live-metadata close gate

## Machine Result

```json
{
  "ok": true,
  "errors": [],
  "scaffold_id": "eslp1-external-source-connector-live-metadata-probe-scaffold",
  "connector_id": "kasb-fss-interpretive-catalog",
  "allow_network": false,
  "record_count": 2,
  "body_text_stored": false,
  "body_cache_created": false,
  "chunks_created": false,
  "embeddings_created": false,
  "index_created": false,
  "answer_time_body_use_enabled": false,
  "decision_gate": {
    "ok": true,
    "report_path": "docs\\reports\\2026-07-05-eslm1-external-source-connector-live-metadata-decision-gate.md",
    "decision": "allow_live_metadata_probe_scaffold"
  },
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
  "probe_records": [
    {
      "item_id": "kasb-implementation-material-index",
      "source_id": "kasb-interpretation-material",
      "publisher": "KASB",
      "allowed_use": "supporting_interpretation",
      "url": "https://www.kasb.or.kr/",
      "status_code": null,
      "final_url": "",
      "content_type": "",
      "network_checked": false,
      "checked_at": "2026-07-05T01:26:57.216321+00:00",
      "body_text_stored": false
    },
    {
      "item_id": "fss-accounting-inquiry-index",
      "source_id": "fss-accounting-inquiry",
      "publisher": "Financial Supervisory Service",
      "allowed_use": "supporting_interpretation",
      "url": "https://www.fss.or.kr/",
      "status_code": null,
      "final_url": "",
      "content_type": "",
      "network_checked": false,
      "checked_at": "2026-07-05T01:26:57.216321+00:00",
      "body_text_stored": false
    }
  ],
  "report_path": "docs\\reports\\2026-07-05-eslp1-external-source-connector-live-metadata-probe-scaffold.md",
  "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or external source connector live-metadata close gate"
}
```
