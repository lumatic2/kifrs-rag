from __future__ import annotations

from scripts.retriever_regression_latency_gate import (
    build_retriever_regression_latency_gate,
    render_markdown,
)


def test_retriever_regression_latency_gate_defers_without_runtime_evidence() -> None:
    result = build_retriever_regression_latency_gate()

    assert result["ok"], result["errors"]
    assert result["horizon"] == "runtime-retriever-promotion-gate"
    assert result["completed_milestone"] == "RPG2"
    assert result["target_retriever"] == "ifrs1109_classification_hybrid"
    assert result["current_default"] == "hybrid"
    assert result["promotion_gate_result"] == "defer"
    assert result["checks"]["recall_support_present"] is True
    assert result["checks"]["citation_miss_support_present"] is True
    assert result["checks"]["default_guard_blocks_accidental_promotion"] is True
    assert result["checks"]["latency_cost_measured"] is False
    assert "latency_cost_measured" in result["blocking_reasons"]
    assert "rollback_policy_present" in result["blocking_reasons"]


def test_retriever_regression_latency_gate_report_is_public_safe() -> None:
    rendered = render_markdown(build_retriever_regression_latency_gate())

    assert "RPG2 Regression And Latency Gate" in rendered
    assert "promotion remains `defer`" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
