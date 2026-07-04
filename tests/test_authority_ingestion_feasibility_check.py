from __future__ import annotations

from scripts.authority_ingestion_feasibility_check import check_ingestion_feasibility


def test_as4_ingestion_feasibility_matrix_is_complete() -> None:
    result = check_ingestion_feasibility()

    assert result["ok"], result["errors"]
    assert result["missing_source_classes"] == []
    assert result["missing_lanes"] == []
    assert result["missing_connector_candidates"] == []


def test_as4_ingestion_feasibility_detects_missing_lane(tmp_path) -> None:
    report = tmp_path / "as4.md"
    report.write_text(
        """
# AS4 Ingestion Feasibility Matrix

`primary_accounting_standard`
`interpretive_accounting_material`
`primary_audit_standard`
`law_regulation`
`filing_data`
`client_private`
`supporting_material`

`document_rag`
`structured_data`
`local_private_case_facts`

`public_metadata_only`
`local_private_body`
`local_private_structured_data`
`public_synthetic_fixture`
`no_store_link_only`
`no_store_handoff`

`kasb-fss-interpretive-catalog`
`opendart-structured-financials`
`law-regulation-locator`

Fetch
Parse
Chunk
Embed
Index
metadata-only document source
structured fact source
""",
        encoding="utf-8",
    )

    result = check_ingestion_feasibility(report)

    assert not result["ok"]
    assert result["missing_lanes"] == ["metadata_support_only"]
