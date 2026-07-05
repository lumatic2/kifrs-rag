# NIS3 Dataization Fixtures

> Scope: validate public-safe non-IFRS source record fixtures.

## One-Line Conclusion

The non-IFRS source record fixture covers all planned source lanes and is public-safe.

## Fixture

- Records path: `docs/ingestion/non_ifrs_source_records.example.json`
- Total records: 4

## Coverage

| Record Type | Count |
|---|---:|
| `client_private_fact` | 1 |
| `document_metadata` | 1 |
| `law_locator` | 1 |
| `structured_fact` | 1 |

## Next Leaf

NIS4_chunking_and_embedding_policy

## Machine Result

```json
{
  "ok": true,
  "title": "NIS3 Dataization Fixtures",
  "records_path": "docs/ingestion/non_ifrs_source_records.example.json",
  "total": 4,
  "by_type": {
    "client_private_fact": 1,
    "document_metadata": 1,
    "law_locator": 1,
    "structured_fact": 1
  },
  "required_types": [
    "client_private_fact",
    "document_metadata",
    "law_locator",
    "structured_fact"
  ],
  "next_leaf": "NIS4_chunking_and_embedding_policy",
  "errors": [],
  "report_path": "docs/reports/2026-07-05-nis3-dataization-fixtures.md"
}
```
