from __future__ import annotations

from scripts.rag_quality_promotion_decision_gate import build_promotion_decision, render_markdown


def test_rag_quality_promotion_decision_defers_without_evidence_and_authorization() -> None:
    result = build_promotion_decision()

    assert result["ok"] is True
    assert result["horizon"] == "rag-quality-fresh-validation"
    assert result["completed_milestone"] == "RQF4"
    assert result["decision"]["result"] == "defer"
    assert result["decision"]["default_change_allowed"] is False
    assert "explicit authorization missing" in result["blockers"]
    assert all(item["exists"] for item in result["evidence"])
    assert result["next_leaf"] == "RQF5_horizon_close_and_next_gap_handoff"


def test_rag_quality_promotion_decision_markdown_is_public_safe() -> None:
    rendered = render_markdown(build_promotion_decision())

    assert "RQF4 Promotion Decision Gate" in rendered
    assert "Decision: `defer`" in rendered
    assert "Default change allowed: False" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "kifrs.db" not in rendered
    assert "source_body" not in rendered
