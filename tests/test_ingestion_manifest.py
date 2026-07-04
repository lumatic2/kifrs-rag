from __future__ import annotations

import json

from kifrs.ingestion.manifest import validate_manifest


def test_default_ingestion_manifest_is_valid() -> None:
    result = validate_manifest()

    assert result["ok"], result["errors"]
    assert result["total"] == 3


def test_ingestion_manifest_rejects_forbidden_body_field(tmp_path) -> None:
    manifest = _minimal_manifest()
    manifest["records"][0]["body"] = "copied source body must not be committed"
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    result = validate_manifest(manifest_path)

    assert not result["ok"]
    assert any("forbidden manifest field" in error for error in result["errors"])


def test_ingestion_manifest_rejects_unknown_source_id(tmp_path) -> None:
    manifest = _minimal_manifest()
    manifest["records"][0]["source_id"] = "unknown-source"
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    result = validate_manifest(manifest_path)

    assert not result["ok"]
    assert "records[0]: unknown source_id unknown-source" in result["errors"]


def _minimal_manifest() -> dict[str, object]:
    return {
        "version": 1,
        "policy": {
            "public_manifest_safe": True,
            "body_text_committed": False,
            "forbidden_fields_rejected": True,
        },
        "records": [
            {
                "record_type": "document_metadata",
                "connector_id": "kasb-fss-interpretive-catalog",
                "connector_version": "0.1.0",
                "source_id": "kasb-interpretation-material",
                "source_class": "interpretive_accounting_material",
                "namespace": "external.kasb_fss",
                "body_storage_policy": "public_metadata_only",
                "citation_role": "supporting_interpretation",
                "locator": {"type": "url", "url": "https://www.kasb.or.kr/"},
                "retrieved_at": "2026-07-05T04:21:00+09:00",
                "public_manifest_safe": True,
                "provenance": {"produced_by": "test"},
                "document_id": "kasb-interpretation-material-test",
                "title": "KASB interpretation material test",
                "publisher": "KASB",
                "document_type": "interpretive_material",
                "publication_date": None,
                "effective_date": None,
                "related_standards": [],
                "topics": ["interpretation"],
                "chunk_strategy": "metadata_only",
                "allowed_use": "supporting_interpretation",
            }
        ],
    }

