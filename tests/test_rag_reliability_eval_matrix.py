from __future__ import annotations

from scripts.rag_reliability_eval_matrix import build_eval_matrix, render_markdown


def test_rr2_eval_matrix_summarizes_goldset_without_protected_fields() -> None:
    matrix = build_eval_matrix()

    assert matrix["milestone"] == "RR2"
    assert matrix["item_count"] >= 20
    assert "rag-evaluation-metrics" in matrix["methodology_nodes"]
    assert "judgment_paragraph_combination" in matrix["bucket_counts"]
    assert "term_bridge_or_exam_convention_dependent" in matrix["bucket_counts"]
    first = matrix["public_safe_matrix"][0]
    assert "id" in first
    assert "question" not in first
    assert "source_ref" not in first
    assert "notes" not in first
    assert "raw answer body" in matrix["protected_fields_excluded"]


def test_rr2_eval_matrix_markdown_is_public_safe() -> None:
    rendered = render_markdown(build_eval_matrix())

    assert "RR2 Eval Matrix and Seed Coverage" in rendered
    assert "Knowledge-graph nodes used" in rendered
    assert "Public-Safe Item Matrix" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
