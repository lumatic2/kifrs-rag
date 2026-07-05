# NIS4 Chunking and Embedding Policy

> Scope: source-lane chunking, indexing, and vector policy for non-IFRS dataization.

## One-Line Conclusion

Each non-IFRS source lane now has an explicit chunk/index/vector policy that keeps protected material out of the public repo.

## Policy

- Policy path: `docs/ingestion/non_ifrs_chunking_policy.json`
- Total lanes: 4

| Lane | Chunk | Index | Vector Scope | Runtime Lookup |
|---|---|---|---|---|
| `document_metadata` | `metadata_card` | `metadata_keyword_plus_optional_metadata_vector` | `author_written_metadata_only` | `metadata_search` |
| `law_locator` | `locator_card` | `keyword_locator_lookup` | `none_for_public_fixture` | `official_locator_lookup` |
| `structured_fact` | `fact_row` | `structured_lookup` | `none_for_public_fixture` | `fact_filter_and_aggregate` |
| `client_private_fact` | `local_private_fact_card` | `local_only_lookup` | `local_only_after_operator_policy` | `local_private_namespace` |

## Next Leaf

NIS5_dataization_gate_and_runtime_handoff

## Machine Result

```json
{
  "ok": true,
  "title": "NIS4 Chunking and Embedding Policy",
  "milestone": "NIS4",
  "policy_path": "docs/ingestion/non_ifrs_chunking_policy.json",
  "total_lanes": 4,
  "lanes": {
    "document_metadata": {
      "chunk_strategy": "metadata_card",
      "index_strategy": "metadata_keyword_plus_optional_metadata_vector",
      "vector_scope": "author_written_metadata_only",
      "runtime_lookup": "metadata_search"
    },
    "law_locator": {
      "chunk_strategy": "locator_card",
      "index_strategy": "keyword_locator_lookup",
      "vector_scope": "none_for_public_fixture",
      "runtime_lookup": "official_locator_lookup"
    },
    "structured_fact": {
      "chunk_strategy": "fact_row",
      "index_strategy": "structured_lookup",
      "vector_scope": "none_for_public_fixture",
      "runtime_lookup": "fact_filter_and_aggregate"
    },
    "client_private_fact": {
      "chunk_strategy": "local_private_fact_card",
      "index_strategy": "local_only_lookup",
      "vector_scope": "local_only_after_operator_policy",
      "runtime_lookup": "local_private_namespace"
    }
  },
  "next_leaf": "NIS5_dataization_gate_and_runtime_handoff",
  "errors": [],
  "report_path": "docs/reports/2026-07-05-nis4-chunking-embedding-policy.md"
}
```
