from __future__ import annotations

from scripts.external_source_synthetic_parser_chunker_close_gate import (
    check_synthetic_parser_chunker_close_gate,
    render_report,
)


def test_synthetic_parser_chunker_close_gate_passes_without_live_ingestion() -> None:
    result = check_synthetic_parser_chunker_close_gate()

    assert result["ok"], result["errors"]
    assert result["dry_run"]["ok"] is True
    assert result["dry_run"]["chunk_count"] == 3
    assert result["dry_run"]["live_fetch_performed"] is False
    assert result["dry_run"]["body_text_stored"] is False
    assert result["dry_run"]["embedding_created"] is False
    assert result["authorization_gate"]["allowed_to_implement"] is False
    assert "synthetic parser/chunker metadata-only dry-run" in result["closed_scope"]
    assert "source body cache" in result["still_not_implemented"]


def test_synthetic_parser_chunker_close_gate_can_run_quality_preflight() -> None:
    result = check_synthetic_parser_chunker_close_gate(run_quality_preflight=True)

    assert result["ok"], result["errors"]
    assert result["quality_preflight"]["ran"] is True
    assert result["quality_preflight"]["ok"] is True
    assert result["quality_preflight"]["public_safe"] is True


def test_synthetic_parser_chunker_close_report_summarizes_boundary() -> None:
    rendered = render_report(check_synthetic_parser_chunker_close_gate())

    assert "Synthetic Parser/Chunker Close Gate" in rendered
    assert "public-safe dry-run level" in rendered
    assert "live ingestion allowed: False" in rendered
    assert "Still Not Implemented" in rendered
    assert "external body embeddings" in rendered
