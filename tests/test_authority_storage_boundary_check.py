from __future__ import annotations

from scripts.authority_storage_boundary_check import check_storage_boundary


def test_as3_storage_boundary_matches_ingestion_policy() -> None:
    result = check_storage_boundary()

    assert result["ok"], result["errors"]
    assert result["missing_source_classes"] == []
    assert result["missing_storage_labels"] == []
    assert result["manifest_ok"] is True


def test_as3_storage_boundary_detects_missing_label(tmp_path) -> None:
    report = tmp_path / "as3.md"
    report.write_text(
        """
# AS3 Copyright and Storage Boundary

`primary_accounting_standard`
`interpretive_accounting_material`
`primary_audit_standard`
`law_regulation`
`filing_data`
`client_private`
`supporting_material`

`public_metadata_only`
`local_private_body`
`local_private_structured_data`
`public_synthetic_fixture`
`no_store_link_only`

Public reports must not include
Ingestion Boundary
source remains `collection_seed`
""",
        encoding="utf-8",
    )

    result = check_storage_boundary(report)

    assert not result["ok"]
    assert result["missing_storage_labels"] == ["no_store_handoff"]
