from __future__ import annotations

from scripts.rag_quality_fresh_validation_close_gate import build_close_gate, render_markdown


def test_rag_quality_fresh_validation_close_gate_defers_and_hands_off() -> None:
    result = build_close_gate()

    assert result["ok"] is True
    assert result["horizon"] == "rag-quality-fresh-validation"
    assert result["completed_milestone"] == "RQF5"
    assert result["close_result"] == "defer"
    assert result["default_change_allowed"] is False
    assert result["next_horizon"] == "private-parser-realism-hardening"
    assert all(item["exists"] for item in result["evidence"])
    assert all(item["gate_ok"] for item in result["evidence"])


def test_rag_quality_fresh_validation_close_gate_markdown_is_public_safe() -> None:
    rendered = render_markdown(build_close_gate())

    assert "RAG Quality Fresh Validation Close Report" in rendered
    assert "Close result: `defer`" in rendered
    assert "private-parser-realism-hardening" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "kifrs.db" not in rendered
    assert "source_body" not in rendered
