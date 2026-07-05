from __future__ import annotations

from scripts.external_source_connector_live_metadata_report_close_gate import (
    check_live_metadata_report_close_gate,
    render_report,
)


def test_live_metadata_report_close_gate_closes_fixture_lane() -> None:
    result = check_live_metadata_report_close_gate()

    assert result["ok"], result["errors"]
    assert result["connector_id"] == "kasb-fss-interpretive-catalog"
    assert result["report_fixture"]["ok"] is True
    assert result["report_fixture"]["record_count"] == 2
    assert result["report_fixture"]["network_checked"] is False
    assert result["report_fixture"]["body_text_stored"] is False
    assert result["report_fixture"]["body_cache_created"] is False
    assert result["report_fixture"]["chunks_created"] is False
    assert result["report_fixture"]["embeddings_created"] is False
    assert result["report_fixture"]["index_created"] is False
    assert result["report_fixture"]["answer_time_body_use_enabled"] is False
    assert "live-metadata report fixture" in result["closed_scope"]


def test_live_metadata_report_close_gate_quality_preflight_can_run() -> None:
    result = check_live_metadata_report_close_gate(run_quality_preflight=True)

    assert result["ok"], result["errors"]
    assert result["quality_preflight"]["ran"] is True
    assert result["quality_preflight"]["ok"] is True
    assert result["quality_preflight"]["public_safe"] is True


def test_live_metadata_report_close_gate_report_names_boundary_and_next_leaf() -> None:
    markdown = render_report(check_live_metadata_report_close_gate())

    assert "ESLRC1 External Source Connector Live-Metadata Report Close Gate" in markdown
    assert "live-metadata report fixture level" in markdown
    assert "source body fetching/crawling" in markdown
    assert "external source connector demo-index bridge" in markdown
    assert "body text stored: False" in markdown
