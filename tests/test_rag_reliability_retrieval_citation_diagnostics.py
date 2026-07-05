from __future__ import annotations

from scripts.rag_reliability_retrieval_citation_diagnostics import build_diagnostics, render_markdown


def test_rr3_diagnostics_compares_default_and_target_retrievers() -> None:
    diagnostics = build_diagnostics()

    assert diagnostics["ok"], diagnostics["errors"]
    assert diagnostics["milestone"] == "RR3"
    assert diagnostics["retrievers"] == ["hybrid", "ifrs1109_classification_hybrid"]
    assert diagnostics["retrieval_aggregate"]["ifrs1109_classification_hybrid"]["recall@20"] == 1.0
    assert diagnostics["target_misses"] == []
    assert diagnostics["bucket_summary"]
    assert "judgment_paragraph_combination" in diagnostics["bucket_summary"]
    assert diagnostics["protected_fields_excluded"]


def test_rr3_diagnostics_markdown_is_public_safe() -> None:
    rendered = render_markdown(build_diagnostics())

    assert "RR3 Retrieval and Citation Diagnostics" in rendered
    assert "Bucket Diagnostics" in rendered
    assert "Failure Taxonomy" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
