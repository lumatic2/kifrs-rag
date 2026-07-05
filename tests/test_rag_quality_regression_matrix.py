from __future__ import annotations

from scripts.rag_quality_regression_matrix import build_regression_matrix, render_markdown


def test_rag_quality_regression_matrix_defers_without_fresh_comparison() -> None:
    matrix = build_regression_matrix()

    assert matrix["ok"] is True
    assert matrix["horizon"] == "rag-quality-fresh-validation"
    assert matrix["completed_milestone"] == "RQF3"
    assert matrix["matrix_result"] == "defer_until_fresh_comparison"
    assert matrix["next_leaf"] == "RQF4_promotion_decision_gate"
    assert all(item["exists"] for item in matrix["evidence"])
    failed_axes = {item["axis"] for item in matrix["comparisons"] if item["pass"] is False}
    assert {"fresh_numeric_eval", "known_regressions", "latency"} <= failed_axes


def test_rag_quality_regression_matrix_markdown_is_public_safe() -> None:
    rendered = render_markdown(build_regression_matrix())

    assert "RQF3 Opt-In Retriever Regression Matrix" in rendered
    assert "defer_until_fresh_comparison" in rendered
    assert "fresh local reruns" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "kifrs.db" not in rendered
    assert "source_body" not in rendered
