from __future__ import annotations

from scripts.external_source_body_ingestion_policy_plan_check import FORBIDDEN_PUBLIC_FIELDS
from scripts.external_source_synthetic_parser_chunker_dry_run import (
    render_report,
    run_synthetic_parser_chunker_dry_run,
)


def test_synthetic_parser_chunker_dry_run_emits_metadata_only_chunks() -> None:
    result = run_synthetic_parser_chunker_dry_run()

    assert result["ok"], result["errors"]
    assert result["fixture_kind"] == "author_written_synthetic_external_source"
    assert result["chunk_count"] == 3
    assert result["live_fetch_performed"] is False
    assert result["body_text_stored"] is False
    assert result["embedding_created"] is False
    assert result["authorization_gate"]["allowed_to_implement"] is False

    for chunk in result["chunks"]:
        assert set(FORBIDDEN_PUBLIC_FIELDS).isdisjoint({key.lower() for key in chunk})
        assert chunk["body_text_stored"] is False
        assert chunk["embedding_created"] is False
        assert chunk["locator"].startswith("synthetic://")
        assert chunk["citation_role"] == "supporting_interpretation"


def test_synthetic_parser_chunker_dry_run_extracts_expected_chunk_headings() -> None:
    result = run_synthetic_parser_chunker_dry_run()
    headings = [chunk["heading"] for chunk in result["chunks"]]

    assert headings == ["Issue", "Analysis", "Evidence Role"]
    assert "setup_fee" in result["chunks"][0]["topic_tags"]
    assert "distinct_service" in result["chunks"][1]["topic_tags"]
    assert "evidence_priority" in result["chunks"][2]["topic_tags"]


def test_synthetic_parser_chunker_report_states_boundary() -> None:
    rendered = render_report(run_synthetic_parser_chunker_dry_run())

    assert "Synthetic Parser/Chunker Dry-Run" in rendered
    assert "does not fetch or crawl" in rendered
    assert "does not write source text" in rendered
    assert "embedding created: False" in rendered
    assert "K-IFRS primary evidence priority is unchanged" in rendered
