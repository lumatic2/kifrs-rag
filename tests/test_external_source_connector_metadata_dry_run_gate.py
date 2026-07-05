from __future__ import annotations

from scripts.external_source_connector_metadata_dry_run_gate import (
    _find_forbidden_fields,
    _validate_manifest_payload,
    build_metadata_dry_run_manifest,
    check_metadata_dry_run_gate,
    render_report,
)


def test_metadata_dry_run_gate_creates_two_public_safe_records() -> None:
    result = check_metadata_dry_run_gate()

    assert result["ok"], result["errors"]
    assert result["connector_id"] == "kasb-fss-interpretive-catalog"
    assert result["record_count"] == 2
    assert result["manifest_validation"]["ok"] is True
    assert result["live_fetch_performed"] is False
    assert result["body_text_committed"] is False
    assert result["body_cache_created"] is False
    assert result["chunks_created"] is False
    assert result["embeddings_created"] is False
    assert {record["source_id"] for record in result["dry_run_records"]} == {
        "kasb-interpretation-material",
        "fss-accounting-inquiry",
    }
    assert all(record["body_storage_policy"] == "public_metadata_only" for record in result["dry_run_records"])
    assert all(record["chunk_strategy"] == "metadata_only" for record in result["dry_run_records"])


def test_metadata_dry_run_manifest_rejects_forbidden_field_regression() -> None:
    manifest = build_metadata_dry_run_manifest()
    manifest["records"][0]["body"] = "copied external source text"

    forbidden_paths = _find_forbidden_fields(manifest)
    validation = _validate_manifest_payload(manifest)

    assert "$.records[0].body" in forbidden_paths
    assert not validation["ok"]
    assert any("forbidden manifest field" in error for error in validation["errors"])


def test_metadata_dry_run_manifest_validation_rejects_non_public_storage() -> None:
    manifest = build_metadata_dry_run_manifest()
    manifest["records"][0]["body_storage_policy"] = "local_private_body"

    validation = _validate_manifest_payload(manifest)

    assert not validation["ok"]
    assert any("not public-manifest safe" in error for error in validation["errors"])


def test_metadata_dry_run_report_names_next_leaf_and_boundary() -> None:
    markdown = render_report(check_metadata_dry_run_gate())

    assert "ESMD1 External Source Connector Metadata Dry-Run Gate" in markdown
    assert "kasb-fss-interpretive-catalog" in markdown
    assert "external source connector metadata close gate" in markdown
    assert "live fetch performed: False" in markdown
    assert "body text committed: False" in markdown
