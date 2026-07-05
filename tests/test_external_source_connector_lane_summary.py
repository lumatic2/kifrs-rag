from __future__ import annotations

from scripts.external_source_connector_lane_summary import (
    build_external_connector_lane_summary,
    render_report,
)


def test_external_connector_lane_summary_covers_all_closed_steps() -> None:
    result = build_external_connector_lane_summary()

    assert result["ok"], result["errors"]
    assert result["connector_id"] == "kasb-fss-interpretive-catalog"
    assert result["lane_status"] == "metadata_and_demo_bridge_closed"
    assert [step["step_id"] for step in result["lane_steps"]] == ["ESCP1", "ESMC1", "ESLC1", "ESLRC1", "ESDIBC1"]
    assert all(step["ok"] is True for step in result["lane_steps"])
    assert result["body_text_stored"] is False
    assert result["body_cache_created"] is False
    assert result["chunks_created"] is False
    assert result["embeddings_created"] is False
    assert result["index_created"] is False
    assert result["answer_time_body_use_enabled"] is False


def test_external_connector_lane_summary_names_closed_and_not_implemented_scope() -> None:
    result = build_external_connector_lane_summary()

    joined_closed = " ".join(result["closed_capabilities"])
    joined_missing = " ".join(result["still_not_implemented"])
    assert "connector-specific policy record" in joined_closed
    assert "demo and field-feedback entry point bridge" in joined_closed
    assert "source body fetching/crawling" in joined_missing
    assert "external source body index namespace" in joined_missing


def test_external_connector_lane_summary_report_is_reviewer_readable() -> None:
    markdown = render_report(build_external_connector_lane_summary())

    assert "ESLS1 External Source Connector Lane Summary" in markdown
    assert "metadata-only policy" in markdown
    assert "not a source-body RAG connector yet" in markdown
    assert "ESDIBC1" in markdown
    assert "external source connector lane close gate" in markdown
