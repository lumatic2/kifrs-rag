from __future__ import annotations

from scripts.rag_quality_baseline_snapshot import build_baseline_snapshot, render_markdown


def test_rag_quality_baseline_snapshot_records_missing_numeric_eval_without_faking_it() -> None:
    snapshot = build_baseline_snapshot()

    assert snapshot["ok"] is True
    assert snapshot["horizon"] == "rag-quality-fresh-validation"
    assert snapshot["completed_milestone"] == "RQF2"
    assert snapshot["baseline"]["default_change_allowed"] is False
    assert snapshot["baseline"]["fresh_numeric_eval_available_in_public_report"] is False
    assert len(snapshot["baseline"]["missing_local_evidence"]) >= 3
    assert all(item["exists"] for item in snapshot["evidence"])
    assert snapshot["next_leaf"] == "RQF3_opt_in_retriever_regression_matrix"


def test_rag_quality_baseline_snapshot_markdown_is_public_safe() -> None:
    rendered = render_markdown(build_baseline_snapshot())

    assert "RQF2 Current Retriever Baseline Snapshot" in rendered
    assert "fresh numeric local eval evidence is not present" in rendered
    assert "Default change allowed: False" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "kifrs.db" not in rendered
    assert "source_body" not in rendered
