from __future__ import annotations

from scripts.external_source_connector_demo_index_bridge import (
    BRIDGE_TARGETS,
    CONNECTOR_CLOSE_REPORT,
    check_demo_index_bridge,
    render_report,
)


def test_demo_index_bridge_links_connector_report_from_reviewer_entry_points() -> None:
    result = check_demo_index_bridge()

    assert result["ok"], result["errors"]
    assert result["connector_id"] == "kasb-fss-interpretive-catalog"
    assert result["connector_close_report"].endswith(CONNECTOR_CLOSE_REPORT)
    assert {target["name"] for target in result["bridged_targets"]} == set(BRIDGE_TARGETS)
    assert all(target["exists"] is True for target in result["bridged_targets"])
    assert all(target["has_connector_report"] is True for target in result["bridged_targets"])
    assert all(target["has_metadata_boundary"] is True for target in result["bridged_targets"])
    assert result["body_text_stored"] is False
    assert result["body_cache_created"] is False
    assert result["chunks_created"] is False
    assert result["embeddings_created"] is False
    assert result["index_created"] is False
    assert result["answer_time_body_use_enabled"] is False


def test_demo_index_bridge_report_names_boundary_and_next_leaf() -> None:
    markdown = render_report(check_demo_index_bridge())

    assert "ESDIB1 External Source Connector Demo-Index Bridge" in markdown
    assert "demo index" in markdown
    assert "metadata-only bridge" in markdown
    assert "does not fetch, store, chunk, embed, index, or answer" in markdown
    assert "external source connector demo-index close gate" in markdown
