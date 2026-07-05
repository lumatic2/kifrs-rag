from __future__ import annotations

from scripts.external_source_connector_live_metadata_close_gate import (
    check_live_metadata_close_gate,
    render_report,
)


def test_live_metadata_close_gate_closes_scaffold_lane() -> None:
    result = check_live_metadata_close_gate()

    assert result["ok"], result["errors"]
    assert result["connector_id"] == "kasb-fss-interpretive-catalog"
    assert result["decision_gate"]["ok"] is True
    assert result["decision_gate"]["decision"] == "allow_live_metadata_probe_scaffold"
    assert result["decision_gate"]["live_metadata_probe_allowed"] is True
    assert result["decision_gate"]["live_body_fetch_allowed"] is False
    assert result["decision_gate"]["body_cache_allowed"] is False
    assert result["decision_gate"]["chunking_allowed"] is False
    assert result["decision_gate"]["embedding_allowed"] is False
    assert result["decision_gate"]["indexing_allowed"] is False
    assert result["decision_gate"]["answer_time_body_use_allowed"] is False
    assert result["probe_scaffold"]["ok"] is True
    assert result["probe_scaffold"]["record_count"] == 2
    assert result["probe_scaffold"]["body_text_stored"] is False
    assert result["probe_scaffold"]["body_cache_created"] is False
    assert result["probe_scaffold"]["chunks_created"] is False
    assert result["probe_scaffold"]["embeddings_created"] is False
    assert result["probe_scaffold"]["index_created"] is False


def test_live_metadata_close_gate_quality_preflight_can_run() -> None:
    result = check_live_metadata_close_gate(run_quality_preflight=True)

    assert result["ok"], result["errors"]
    assert result["quality_preflight"]["ran"] is True
    assert result["quality_preflight"]["ok"] is True
    assert result["quality_preflight"]["public_safe"] is True


def test_live_metadata_close_report_names_boundary_and_next_leaf() -> None:
    markdown = render_report(check_live_metadata_close_gate())

    assert "ESLC1 External Source Connector Live-Metadata Close Gate" in markdown
    assert "live-metadata scaffold level" in markdown
    assert "source body fetching/crawling" in markdown
    assert "external source connector live-metadata report fixture" in markdown
    assert "body text stored: False" in markdown
