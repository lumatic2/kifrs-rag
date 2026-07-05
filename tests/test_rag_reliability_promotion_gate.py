from __future__ import annotations

from functools import lru_cache

from scripts.rag_reliability_promotion_gate import build_promotion_gate, render_markdown


@lru_cache(maxsize=1)
def _gate() -> dict:
    return build_promotion_gate()


def test_rr5_promotion_gate_closes_without_default_promotion() -> None:
    gate = _gate()

    assert gate["ok"], gate["errors"]
    assert gate["milestone"] == "RR5"
    assert gate["default_promotion"] is False
    assert gate["promotion_decision"] == "defer"
    assert gate["next_horizon"] == "non-ifrs-source-dataization"
    assert gate["handoff_ready"] is True
    assert gate["default_guard_snapshot"]["default_mode"] == "hybrid"
    assert gate["default_guard_snapshot"]["target_retriever_exposed_in_mcp"] is False
    assert all(row["exists"] for row in gate["required_reports"])


def test_rr5_promotion_gate_markdown_is_public_safe_and_actionable() -> None:
    rendered = render_markdown(_gate())

    assert "RR5 RAG Promotion Gate" in rendered
    assert "Default promotion: False" in rendered
    assert "Regression Commands For Next Horizon" in rendered
    assert "quality_preflight.py" in rendered
    assert "rag_quality_final_gate.py" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
