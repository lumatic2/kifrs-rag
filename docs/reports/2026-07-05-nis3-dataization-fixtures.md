# NIS3 Dataization Fixtures

> Scope: public-safe non-IFRS source record fixture and validator.

## One-Line Conclusion

The four source lanes now have a single public-safe fixture validated by the NIS2 source record contract.

## Fixture

- Records path: `docs/ingestion/non_ifrs_source_records.example.json`
- Total records: 4

## Record Type Coverage

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
  "milestone": "NIS3",
  "records_path": "docs/ingestion/non_ifrs_source_records.example.json",
  "total": 4,
  "by_type": {
    "client_private_fact": 1,
    "document_metadata": 1,
    "law_locator": 1,
    "structured_fact": 1
  },
  "errors": [],
  "next_leaf": "NIS4_chunking_and_embedding_policy",
  "report_path": "docs/reports/2026-07-05-nis3-dataization-fixtures.md"
}
```
