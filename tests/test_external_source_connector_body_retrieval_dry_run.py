from __future__ import annotations

from scripts.external_source_connector_body_retrieval_dry_run import build_retrieval_dry_run, render_markdown


def test_external_source_connector_body_retrieval_dry_run_ranks_expected_chunks() -> None:
    result = build_retrieval_dry_run()

    assert result["ok"] is True
    assert result["horizon"] == "external-source-body-connector-expansion"
    assert result["completed_milestone"] == "ESB3"
    assert len(result["chunks"]) == 3
    assert all(chunk["contains_copied_payload"] is False for chunk in result["chunks"])
    assert all(row["top_chunk_id"] == row["expected_chunk"] for row in result["retrieval_results"])
    assert result["checks"]["no_body_payload_in_results"] is True
    assert result["next_leaf"] == "ESB4_connector_leak_and_policy_gate"


def test_external_source_connector_body_retrieval_dry_run_markdown_is_public_safe() -> None:
    rendered = render_markdown(build_retrieval_dry_run())

    assert "ESB3 Chunking And Retrieval Dry Run" in rendered
    assert "Synthetic chunks can be ranked" in rendered
    assert "Payload Rendered" in rendered
    assert "api_key" not in rendered
    assert "secret" not in rendered
    assert "password" not in rendered
    assert "kifrs.db" not in rendered
    assert "source_body" not in rendered
