from __future__ import annotations

import json

from kifrs.ingestion.evidence import validate_evidence_manifest


def test_default_ingestion_evidence_manifest_is_valid() -> None:
    result = validate_evidence_manifest()

    assert result["ok"], result["errors"]
    assert result["total"] == 3


def test_evidence_manifest_rejects_unknown_record(tmp_path) -> None:
    manifest = _minimal_evidence_manifest()
    manifest["evidence"][0]["record_id"] = "missing-record"
    path = tmp_path / "evidence.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")

    result = validate_evidence_manifest(path)

    assert not result["ok"]
    assert any("unknown source manifest record" in error for error in result["errors"])


def test_evidence_manifest_rejects_role_mismatch(tmp_path) -> None:
    manifest = _minimal_evidence_manifest()
    manifest["evidence"][0]["citation_role"] = "legal_boundary"
    path = tmp_path / "evidence.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")

    result = validate_evidence_manifest(path)

    assert not result["ok"]
    assert any("citation_role legal_boundary does not match source record" in error for error in result["errors"])


def test_evidence_manifest_rejects_copied_quote_field(tmp_path) -> None:
    manifest = _minimal_evidence_manifest()
    manifest["evidence"][0]["quote"] = "copied source quote"
    path = tmp_path / "evidence.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")

    result = validate_evidence_manifest(path)

    assert not result["ok"]
    assert any("forbidden evidence field" in error for error in result["errors"])


def _minimal_evidence_manifest() -> dict[str, object]:
    return {
        "version": 1,
        "policy": {
            "public_manifest_safe": True,
            "body_text_committed": False,
            "source_manifest": "docs/ingestion/source_manifest.example.json",
        },
        "evidence": [
            {
                "evidence_id": "ev-kasb-test",
                "record_type": "document_metadata",
                "record_id": "kasb-interpretation-material-catalog-seed",
                "source_id": "kasb-interpretation-material",
                "citation_role": "supporting_interpretation",
                "body_storage_policy": "public_metadata_only",
                "locator": {"type": "url", "url": "https://www.kasb.or.kr/"},
                "evidence_label": "KASB metadata catalog seed",
                "allowed_output_level": "metadata_locator_only",
            }
        ],
    }

