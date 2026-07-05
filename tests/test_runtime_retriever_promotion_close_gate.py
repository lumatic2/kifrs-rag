from __future__ import annotations

from scripts.runtime_retriever_promotion_close_gate import (
    build_runtime_retriever_promotion_close_gate,
    render_markdown,
)


def test_runtime_retriever_promotion_close_gate_defers_with_rollback() -> None:
    result = build_runtime_retriever_promotion_close_gate()

    assert result["ok"], result["errors"]
    assert result["horizon"] == "runtime-retriever-promotion-gate"
    assert result["completed_milestone"] == "RPG5"
    assert result["close_status"] == "closed"
    assert result["close_result"] == "defer"
    assert result["target_retriever"] == "ifrs1109_classification_hybrid"
    assert result["current_default"] == "hybrid"
    assert result["checks"]["rollback_evidence_present"] is True
    assert result["checks"]["operator_command_dry_run"] is True
    assert result["checks"]["default_not_changed"] is True
    assert result["rollback"]["safe_fallback"] == "hybrid"
    assert result["next_horizon"] == "operator-experience-hardening"


def test_runtime_retriever_promotion_close_gate_report_is_public_safe() -> None:
    rendered = render_markdown(build_runtime_retriever_promotion_close_gate())

    assert "Runtime Retriever Promotion Gate Close Report" in rendered
    assert "closes as `defer`" in rendered
    assert "operator-experience-hardening" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
