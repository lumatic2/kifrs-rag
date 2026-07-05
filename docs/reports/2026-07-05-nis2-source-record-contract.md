# NIS2 Source Record Contract

> Scope: canonical record contract for non-IFRS source dataization.

## One-Line Conclusion

Non-IFRS dataization now has one source record contract across document metadata, law locators, structured facts, and client-private placeholders.

## Record Types

| Type | Retrieval Lane | Authority Level | Storage | Purpose |
|---|---|---|---|---|
| `document_metadata` | `document_metadata` | `supporting` | `public_metadata_only` | KASB/FSS/FSC-style supporting document metadata without committed body text. |
| `law_locator` | `law_locator` | `legal_boundary` | `no_store_link_only` | Law/regulation locator and legal-boundary evidence without article body copy. |
| `structured_fact` | `structured_fact` | `fact` | `public_synthetic_fixture` | OpenDART/XBRL-like facts as normalized structured values. |
| `client_private_fact` | `local_private_fact` | `client_private` | `no_store_handoff` | Local-only client fact placeholder that never commits private content. |

## Contract Files

- Module: `kifrs/ingestion/source_record.py`
- Tests: `tests/test_source_record_contract.py`

## Next Leaf

NIS3_dataization_fixtures_and_validators

## Machine Result

```json
{
  "ok": true,
  "title": "NIS2 Source Record Contract",
  "milestone": "NIS2",
  "record_types": {
    "document_metadata": {
      "purpose": "KASB/FSS/FSC-style supporting document metadata without committed body text.",
      "retrieval_lane": "document_metadata",
      "authority_level": "supporting",
      "storage": "public_metadata_only"
    },
    "law_locator": {
      "purpose": "Law/regulation locator and legal-boundary evidence without article body copy.",
      "retrieval_lane": "law_locator",
      "authority_level": "legal_boundary",
      "storage": "no_store_link_only"
    },
    "structured_fact": {
      "purpose": "OpenDART/XBRL-like facts as normalized structured values.",
      "retrieval_lane": "structured_fact",
      "authority_level": "fact",
      "storage": "public_synthetic_fixture"
    },
    "client_private_fact": {
      "purpose": "Local-only client fact placeholder that never commits private content.",
      "retrieval_lane": "local_private_fact",
      "authority_level": "client_private",
      "storage": "no_store_handoff"
    }
  },
  "allowed_authority_levels": [
    "client_private",
    "fact",
    "legal_boundary",
    "primary",
    "supporting"
  ],
  "allowed_retrieval_lanes": [
    "document_metadata",
    "law_locator",
    "local_private_fact",
    "structured_fact"
  ],
  "contract_module": "kifrs/ingestion/source_record.py",
  "test_path": "tests/test_source_record_contract.py",
  "next_leaf": "NIS3_dataization_fixtures_and_validators",
  "errors": [],
  "report_path": "docs/reports/2026-07-05-nis2-source-record-contract.md"
}
```
