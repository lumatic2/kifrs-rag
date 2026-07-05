from __future__ import annotations

from scripts.external_source_connector_metadata_close_gate import (
    check_metadata_close_gate,
    render_report,
)


def test_metadata_close_gate_closes_metadata_only_readiness() -> None:
    result = check_metadata_close_gate()

    assert result["ok"], result["errors"]
    assert result["connector_id"] == "kasb-fss-interpretive-catalog"
    assert result["policy_record"]["ok"] is True
    assert result["metadata_dry_run"]["ok"] is True
    assert result["metadata_dry_run"]["record_count"] == 2
    assert result["metadata_dry_run"]["manifest_validation_ok"] is True
    assert result["policy_record"]["live_fetch_allowed"] is False
    assert result["policy_record"]["body_cache_allowed"] is False
    assert result["policy_record"]["live_chunking_allowed"] is False
    assert result["policy_record"]["embedding_allowed"] is False
    assert result["policy_record"]["answer_time_use_allowed"] is False
    assert result["metadata_dry_run"]["live_fetch_performed"] is False
    assert result["metadata_dry_run"]["body_cache_created"] is False
    assert result["metadata_dry_run"]["chunks_created"] is False
    assert result["metadata_dry_run"]["embeddings_created"] is False


def test_metadata_close_gate_quality_preflight_can_run() -> None:
    result = check_metadata_close_gate(run_quality_preflight=True)

    assert result["ok"], result["errors"]
    assert result["quality_preflight"]["ran"] is True
    assert result["quality_preflight"]["ok"] is True
    assert result["quality_preflight"]["public_safe"] is True


def test_metadata_close_report_names_unimplemented_live_ingestion() -> None:
    markdown = render_report(check_metadata_close_gate())

    assert "ESMC1 External Source Connector Metadata Close Gate" in markdown
    assert "metadata-only readiness" in markdown
    assert "live external body fetching/crawling" in markdown
    assert "external source connector live-metadata decision gate" in markdown
    assert "live fetch performed: False" in markdown
