from __future__ import annotations

from scripts.external_source_connector_demo_index_close_gate import (
    check_demo_index_close_gate,
    render_report,
)


def test_demo_index_close_gate_closes_bridge_lane() -> None:
    result = check_demo_index_close_gate()

    assert result["ok"], result["errors"]
    assert result["connector_id"] == "kasb-fss-interpretive-catalog"
    assert result["demo_index_bridge"]["ok"] is True
    assert result["demo_index_bridge"]["target_count"] == 4
    assert result["demo_index_bridge"]["body_text_stored"] is False
    assert result["demo_index_bridge"]["body_cache_created"] is False
    assert result["demo_index_bridge"]["chunks_created"] is False
    assert result["demo_index_bridge"]["embeddings_created"] is False
    assert result["demo_index_bridge"]["index_created"] is False
    assert result["demo_index_bridge"]["answer_time_body_use_enabled"] is False
    assert "demo index connector evidence bridge" in result["closed_scope"]
    assert "real accountant session packet connector evidence bridge" in result["closed_scope"]


def test_demo_index_close_gate_quality_preflight_can_run() -> None:
    result = check_demo_index_close_gate(run_quality_preflight=True)

    assert result["ok"], result["errors"]
    assert result["quality_preflight"]["ran"] is True
    assert result["quality_preflight"]["ok"] is True
    assert result["quality_preflight"]["public_safe"] is True


def test_demo_index_close_gate_report_names_boundary_and_next_leaf() -> None:
    markdown = render_report(check_demo_index_close_gate())

    assert "ESDIBC1 External Source Connector Demo-Index Close Gate" in markdown
    assert "demo-index bridge level" in markdown
    assert "source body fetching/crawling" in markdown
    assert "external source connector lane summary" in markdown
    assert "body text stored: False" in markdown
