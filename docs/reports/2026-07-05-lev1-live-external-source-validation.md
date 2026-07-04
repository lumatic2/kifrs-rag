# LEV1 Live External Source Validation

> Scope: metadata-only live check for external authority source surfaces.

## 한 줄 결론

External source metadata now has a live validation gate. The gate checks link/API landing surfaces only and stores no source body text.

## Check Results

- ok: True
- source_pack_ok: True
- network_checked: True
- target_count: 3
- body_text_stored: False

## Live Targets

| Item | Publisher | Status | Final URL |
|---|---|---:|---|
| `kasb-implementation-material-index` | KASB | 200 | https://www.kasb.or.kr/ |
| `fss-accounting-inquiry-index` | Financial Supervisory Service | 200 | https://www.fss.or.kr/fss/main/main.do?menuNo=200000 |
| `opendart-structured-financials-seed` | OpenDART | 200 | https://opendart.fss.or.kr/ |

## Boundary

- This report does not store KASB/FSS/OpenDART body text.
- This report does not promote external sources above K-IFRS primary evidence.
- This report does not implement body ingestion, OCR, crawling, or embeddings.

## Next Leaf

real-accountant-session RS2/RS3 evidence capture, or opt-in retriever demo validation

## Machine Result

```json
{
  "ok": true,
  "errors": [],
  "source_pack_ok": true,
  "target_count": 3,
  "network_checked": true,
  "body_text_stored": false,
  "checks": [
    {
      "item_id": "kasb-implementation-material-index",
      "source_id": "kasb-interpretation-material",
      "publisher": "KASB",
      "allowed_use": "supporting_interpretation",
      "url": "https://www.kasb.or.kr/",
      "network_checked": true,
      "body_text_stored": false,
      "ok": true,
      "status_code": 200,
      "final_url": "https://www.kasb.or.kr/",
      "content_type": "text/html;charset=UTF-8",
      "error": ""
    },
    {
      "item_id": "fss-accounting-inquiry-index",
      "source_id": "fss-accounting-inquiry",
      "publisher": "Financial Supervisory Service",
      "allowed_use": "supporting_interpretation",
      "url": "https://www.fss.or.kr/",
      "network_checked": true,
      "body_text_stored": false,
      "ok": true,
      "status_code": 200,
      "final_url": "https://www.fss.or.kr/fss/main/main.do?menuNo=200000",
      "content_type": "text/html; charset=utf-8",
      "error": ""
    },
    {
      "item_id": "opendart-structured-financials-seed",
      "source_id": "opendart-structured-financials",
      "publisher": "OpenDART",
      "allowed_use": "collection_seed",
      "url": "https://opendart.fss.or.kr/",
      "network_checked": true,
      "body_text_stored": false,
      "ok": true,
      "status_code": 200,
      "final_url": "https://opendart.fss.or.kr/",
      "content_type": "text/html; charset=UTF-8",
      "error": ""
    }
  ],
  "report_path": "docs\\reports\\2026-07-05-lev1-live-external-source-validation.md",
  "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or opt-in retriever demo validation"
}
```
