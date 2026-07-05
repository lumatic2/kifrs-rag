from __future__ import annotations

from scripts.external_source_connector_lane_close_gate import (
    REQUIRED_STEP_IDS,
    check_external_connector_lane_close_gate,
    render_report,
)


def test_external_connector_lane_close_gate_closes_summary_lane() -> None:
    result = check_external_connector_lane_close_gate()

    assert result["ok"], result["errors"]
    assert result["connector_id"] == "kasb-fss-interpretive-catalog"
    assert result["lane_summary"]["ok"] is True
    assert result["lane_summary"]["lane_status"] == "metadata_and_demo_bridge_closed"
    assert result["lane_summary"]["step_ids"] == REQUIRED_STEP_IDS
    assert result["lane_summary"]["body_text_stored"] is False
    assert result["lane_summary"]["body_cache_created"] is False
    assert result["lane_summary"]["chunks_created"] is False
    assert result["lane_summary"]["embeddings_created"] is False
    assert result["lane_summary"]["index_created"] is False
    assert result["lane_summary"]["answer_time_body_use_enabled"] is False
    assert "lane summary" in result["closed_scope"]


def test_external_connector_lane_close_gate_quality_preflight_can_run() -> None:
    result = check_external_connector_lane_close_gate(run_quality_preflight=True)

    assert result["ok"], result["errors"]
    assert result["quality_preflight"]["ran"] is True
    assert result["quality_preflight"]["ok"] is True
    assert result["quality_preflight"]["public_safe"] is True


def test_external_connector_lane_close_gate_report_names_boundary_and_next_leaf() -> None:
    markdown = render_report(check_external_connector_lane_close_gate())

    assert "ESLSC1 External Source Connector Lane Close Gate" in markdown
    assert "metadata-only external connector lane" in markdown
    assert "external source body RAG remains intentionally unimplemented" in markdown
    assert "external source connector post-close demo packet note" in markdown
    assert "body text stored: False" in markdown
