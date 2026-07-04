from __future__ import annotations

from scripts.authority_connector_recommendation_check import check_connector_recommendation


def test_as5_connector_recommendation_is_complete() -> None:
    result = check_connector_recommendation()

    assert result["ok"], result["errors"]
    assert result["missing_recommended_connectors"] == []
    assert result["missing_deferred_connectors"] == []
    assert result["missing_next_milestones"] == []


def test_as5_connector_recommendation_detects_missing_recommendation(tmp_path) -> None:
    report = tmp_path / "as5.md"
    report.write_text(
        """
# AS5 First Connector Recommendation

`kasb-fss-interpretive-catalog`
`opendart-structured-financials`

`audit-standards-namespace`
`client-private-case-intake`
`firm-public-guides`

MSI1 MSI2 MSI3 MSI4 MSI5
`multi-source-ingestion-pipeline`
`supporting_interpretation`
`fact_evidence`
`legal_boundary`
no body ingestion
no external API call
""",
        encoding="utf-8",
    )

    result = check_connector_recommendation(report)

    assert not result["ok"]
    assert result["missing_recommended_connectors"] == ["law-regulation-locator"]
