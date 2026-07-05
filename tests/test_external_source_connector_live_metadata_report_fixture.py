from __future__ import annotations

from scripts.external_source_connector_live_metadata_report_fixture import (
    build_live_metadata_report_fixture,
    render_fixture_table,
    render_report,
)


def test_live_metadata_report_fixture_uses_metadata_only_records() -> None:
    result = build_live_metadata_report_fixture()

    assert result["ok"], result["errors"]
    assert result["fixture_id"] == "eslr1-external-source-connector-live-metadata-report-fixture"
    assert result["connector_id"] == "kasb-fss-interpretive-catalog"
    assert result["public_safe_report_fixture_created"] is True
    assert result["network_checked"] is False
    assert result["record_count"] == 2
    assert result["body_text_stored"] is False
    assert result["body_cache_created"] is False
    assert result["chunks_created"] is False
    assert result["embeddings_created"] is False
    assert result["index_created"] is False
    assert result["answer_time_body_use_enabled"] is False
    assert all(row["network_checked"] is False for row in result["fixture_rows"])
    assert all(row["body_text_stored"] is False for row in result["fixture_rows"])
    assert {row["item_id"] for row in result["fixture_rows"]} == {
        "kasb-implementation-material-index",
        "fss-accounting-inquiry-index",
    }


def test_live_metadata_fixture_table_is_human_readable_without_body_fields() -> None:
    result = build_live_metadata_report_fixture()
    table = render_fixture_table(result["fixture_rows"])

    assert "| Item | Publisher | Locator | Status | Network | Body Stored |" in table
    assert "kasb-implementation-material-index" in table
    assert "fss-accounting-inquiry-index" in table
    assert "raw_html" not in table
    assert "source_body" not in table
    assert "api_key" not in table
    assert "token" not in table


def test_live_metadata_report_fixture_names_boundary_and_next_leaf() -> None:
    markdown = render_report(build_live_metadata_report_fixture())

    assert "ESLR1 External Source Connector Live-Metadata Report Fixture" in markdown
    assert "human-readable report fixture" in markdown
    assert "metadata-only records" in markdown
    assert "body text stored: False" in markdown
    assert "external source connector live-metadata report close gate" in markdown
