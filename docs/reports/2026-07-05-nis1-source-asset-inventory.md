# NIS1 Source Asset Inventory

> Scope: classify existing source-map, ingestion, connector, parser, and policy assets for non-IFRS source dataization.

## One-Line Conclusion

Reuse the existing authority/MSI/client-private assets, then add a stricter source record contract in NIS2.

## Lane Inventory

### document_metadata

KASB/FSS/FSC interpretive catalog entries and supporting document metadata without committed body text.

| Reusable Asset | Exists |
|---|---|
| `docs/reports/2026-07-05-non-ifrs-source-map.md` | True |
| `docs/reports/2026-07-05-as1-source-taxonomy.md` | True |
| `docs/reports/2026-07-05-as2-authority-citation-policy.md` | True |
| `docs/reports/2026-07-05-msi1-connector-contract.md` | True |
| `docs/reports/2026-07-05-msi2-metadata-catalog-prototype.md` | True |
| `docs/ingestion/source_manifest.example.json` | True |
| `kifrs/ingestion/manifest.py` | True |
| `scripts/validate_ingestion_manifest.py` | True |
| `tests/test_ingestion_manifest.py` | True |

Build next:
- NIS2 source record wrapper around document_metadata
- NIS3 non_ifrs_source_records fixture entries for KASB/FSS-style metadata

Excluded from active implementation:
- KASB/FSS/FSC document body fetch
- copied interpretation text or excerpts

### law_locator

Law/regulation references as locators and legal-boundary evidence, not copied article text.

| Reusable Asset | Exists |
|---|---|
| `docs/reports/2026-07-05-non-ifrs-source-map.md` | True |
| `docs/reports/2026-07-05-msi1-connector-contract.md` | True |
| `docs/ingestion/source_manifest.example.json` | True |
| `kifrs/ingestion/manifest.py` | True |

Build next:
- NIS2 explicit law locator record type or subtype policy
- NIS3 public-safe law locator fixture

Excluded from active implementation:
- law article body copy
- full legal database ingestion

### structured_fact

OpenDART/XBRL-like company facts as structured values, separate from document RAG.

| Reusable Asset | Exists |
|---|---|
| `docs/reports/2026-07-05-msi1-connector-contract.md` | True |
| `docs/reports/2026-07-05-msi5-ingestion-gate-close-report.md` | True |
| `docs/ingestion/source_manifest.example.json` | True |
| `kifrs/ingestion/manifest.py` | True |
| `tests/test_ingestion_manifest.py` | True |

Build next:
- NIS2 structured_fact contract with authority/storage/retrieval lane fields
- NIS3 synthetic OpenDART-like facts in non_ifrs_source_records.example.json

Excluded from active implementation:
- live OpenDART API call
- raw XML/XBRL dump
- external secret handling

### client_private

Local-only case facts from contracts, TB, accounting policies, and workpapers.

| Reusable Asset | Exists |
|---|---|
| `docs/reports/2026-07-05-local-parser-real-adapter-implementation-plan.md` | True |
| `docs/reports/2026-07-05-lpa1-local-parser-adapter-contract.md` | True |
| `docs/reports/2026-07-05-lpas1-local-parser-adapter-scaffold.md` | True |
| `docs/reports/2026-07-05-lpad1-local-parser-adapter-dry-run-gate.md` | True |
| `kifrs/feedback/local_parser.py` | True |

Build next:
- NIS2 client_private placeholder contract
- NIS3 local-only placeholder fixture without private content

Excluded from active implementation:
- real client file upload
- OCR output body
- private document excerpts

### policy_and_gate

Cross-lane source taxonomy, storage policy, evidence manifest, and public-safe gates.

| Reusable Asset | Exists |
|---|---|
| `docs/authority/sources.json` | True |
| `docs/authority/source_pack.json` | True |
| `docs/reports/2026-07-05-authority-source-map-close-report.md` | True |
| `docs/reports/2026-07-05-msi4-provenance-citation-manifest.md` | True |
| `docs/reports/2026-07-05-msi5-ingestion-gate-close-report.md` | True |
| `docs/ingestion/evidence_manifest.example.json` | True |
| `kifrs/ingestion/evidence.py` | True |
| `scripts/validate_authority_sources.py` | True |
| `scripts/validate_authority_source_pack.py` | True |
| `scripts/validate_ingestion_evidence.py` | True |
| `tests/test_ingestion_evidence.py` | True |

Build next:
- NIS4 chunking and embedding policy
- NIS5 non_ifrs_dataization_gate

Excluded from active implementation:
- default retriever change
- multi-authority answer composition runtime

## Forbidden Scope

- source body text
- law article body
- DART raw filing/XML/XBRL dump
- embeddings or vector store files
- external secrets
- client-private document body or excerpt

## Next Leaf

NIS2_source_record_contract

## Machine Result

```json
{
  "ok": true,
  "title": "NIS1 Source Asset Inventory",
  "milestone": "NIS1",
  "lanes": {
    "document_metadata": {
      "purpose": "KASB/FSS/FSC interpretive catalog entries and supporting document metadata without committed body text.",
      "reusable_assets": [
        {
          "path": "docs/reports/2026-07-05-non-ifrs-source-map.md",
          "exists": true,
          "kind": "file"
        },
        {
          "path": "docs/reports/2026-07-05-as1-source-taxonomy.md",
          "exists": true,
          "kind": "file"
        },
        {
          "path": "docs/reports/2026-07-05-as2-authority-citation-policy.md",
          "exists": true,
          "kind": "file"
        },
        {
          "path": "docs/reports/2026-07-05-msi1-connector-contract.md",
          "exists": true,
          "kind": "file"
        },
        {
          "path": "docs/reports/2026-07-05-msi2-metadata-catalog-prototype.md",
          "exists": true,
          "kind": "file"
        },
        {
          "path": "docs/ingestion/source_manifest.example.json",
          "exists": true,
          "kind": "file"
        },
        {
          "path": "kifrs/ingestion/manifest.py",
          "exists": true,
          "kind": "file"
        },
        {
          "path": "scripts/validate_ingestion_manifest.py",
          "exists": true,
          "kind": "file"
        },
        {
          "path": "tests/test_ingestion_manifest.py",
          "exists": true,
          "kind": "file"
        }
      ],
      "build_next": [
        "NIS2 source record wrapper around document_metadata",
        "NIS3 non_ifrs_source_records fixture entries for KASB/FSS-style metadata"
      ],
      "excluded_from_active_implementation": [
        "KASB/FSS/FSC document body fetch",
        "copied interpretation text or excerpts"
      ]
    },
    "law_locator": {
      "purpose": "Law/regulation references as locators and legal-boundary evidence, not copied article text.",
      "reusable_assets": [
        {
          "path": "docs/reports/2026-07-05-non-ifrs-source-map.md",
          "exists": true,
          "kind": "file"
        },
        {
          "path": "docs/reports/2026-07-05-msi1-connector-contract.md",
          "exists": true,
          "kind": "file"
        },
        {
          "path": "docs/ingestion/source_manifest.example.json",
          "exists": true,
          "kind": "file"
        },
        {
          "path": "kifrs/ingestion/manifest.py",
          "exists": true,
          "kind": "file"
        }
      ],
      "build_next": [
        "NIS2 explicit law locator record type or subtype policy",
        "NIS3 public-safe law locator fixture"
      ],
      "excluded_from_active_implementation": [
        "law article body copy",
        "full legal database ingestion"
      ]
    },
    "structured_fact": {
      "purpose": "OpenDART/XBRL-like company facts as structured values, separate from document RAG.",
      "reusable_assets": [
        {
          "path": "docs/reports/2026-07-05-msi1-connector-contract.md",
          "exists": true,
          "kind": "file"
        },
        {
          "path": "docs/reports/2026-07-05-msi5-ingestion-gate-close-report.md",
          "exists": true,
          "kind": "file"
        },
        {
          "path": "docs/ingestion/source_manifest.example.json",
          "exists": true,
          "kind": "file"
        },
        {
          "path": "kifrs/ingestion/manifest.py",
          "exists": true,
          "kind": "file"
        },
        {
          "path": "tests/test_ingestion_manifest.py",
          "exists": true,
          "kind": "file"
        }
      ],
      "build_next": [
        "NIS2 structured_fact contract with authority/storage/retrieval lane fields",
        "NIS3 synthetic OpenDART-like facts in non_ifrs_source_records.example.json"
      ],
      "excluded_from_active_implementation": [
        "live OpenDART API call",
        "raw XML/XBRL dump",
        "external secret handling"
      ]
    },
    "client_private": {
      "purpose": "Local-only case facts from contracts, TB, accounting policies, and workpapers.",
      "reusable_assets": [
        {
          "path": "docs/reports/2026-07-05-local-parser-real-adapter-implementation-plan.md",
          "exists": true,
          "kind": "file"
        },
        {
          "path": "docs/reports/2026-07-05-lpa1-local-parser-adapter-contract.md",
          "exists": true,
          "kind": "file"
        },
        {
          "path": "docs/reports/2026-07-05-lpas1-local-parser-adapter-scaffold.md",
          "exists": true,
          "kind": "file"
        },
        {
          "path": "docs/reports/2026-07-05-lpad1-local-parser-adapter-dry-run-gate.md",
          "exists": true,
          "kind": "file"
        },
        {
          "path": "kifrs/feedback/local_parser.py",
          "exists": true,
          "kind": "file"
        }
      ],
      "build_next": [
        "NIS2 client_private placeholder contract",
        "NIS3 local-only placeholder fixture without private content"
      ],
      "excluded_from_active_implementation": [
        "real client file upload",
        "OCR output body",
        "private document excerpts"
      ]
    },
    "policy_and_gate": {
      "purpose": "Cross-lane source taxonomy, storage policy, evidence manifest, and public-safe gates.",
      "reusable_assets": [
        {
          "path": "docs/authority/sources.json",
          "exists": true,
          "kind": "file"
        },
        {
          "path": "docs/authority/source_pack.json",
          "exists": true,
          "kind": "file"
        },
        {
          "path": "docs/reports/2026-07-05-authority-source-map-close-report.md",
          "exists": true,
          "kind": "file"
        },
        {
          "path": "docs/reports/2026-07-05-msi4-provenance-citation-manifest.md",
          "exists": true,
          "kind": "file"
        },
        {
          "path": "docs/reports/2026-07-05-msi5-ingestion-gate-close-report.md",
          "exists": true,
          "kind": "file"
        },
        {
          "path": "docs/ingestion/evidence_manifest.example.json",
          "exists": true,
          "kind": "file"
        },
        {
          "path": "kifrs/ingestion/evidence.py",
          "exists": true,
          "kind": "file"
        },
        {
          "path": "scripts/validate_authority_sources.py",
          "exists": true,
          "kind": "file"
        },
        {
          "path": "scripts/validate_authority_source_pack.py",
          "exists": true,
          "kind": "file"
        },
        {
          "path": "scripts/validate_ingestion_evidence.py",
          "exists": true,
          "kind": "file"
        },
        {
          "path": "tests/test_ingestion_evidence.py",
          "exists": true,
          "kind": "file"
        }
      ],
      "build_next": [
        "NIS4 chunking and embedding policy",
        "NIS5 non_ifrs_dataization_gate"
      ],
      "excluded_from_active_implementation": [
        "default retriever change",
        "multi-authority answer composition runtime"
      ]
    }
  },
  "reusable_asset_count": 34,
  "missing_asset_count": 0,
  "forbidden_scope": [
    "source body text",
    "law article body",
    "DART raw filing/XML/XBRL dump",
    "embeddings or vector store files",
    "external secrets",
    "client-private document body or excerpt"
  ],
  "next_leaf": "NIS2_source_record_contract",
  "errors": [],
  "report_path": "docs/reports/2026-07-05-nis1-source-asset-inventory.md"
}
```
