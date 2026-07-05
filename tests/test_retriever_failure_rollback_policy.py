from __future__ import annotations

from scripts.retriever_failure_rollback_policy import (
    build_retriever_failure_rollback_policy,
    render_markdown,
)


def test_retriever_failure_rollback_policy_keeps_hybrid_fallback() -> None:
    result = build_retriever_failure_rollback_policy()
    policy = result["policy"]

    assert result["ok"], result["errors"]
    assert result["horizon"] == "runtime-retriever-promotion-gate"
    assert result["completed_milestone"] == "RPG3"
    assert policy["current_default"] == "hybrid"
    assert policy["safe_fallback"] == "hybrid"
    assert policy["target_retriever"] == "ifrs1109_classification_hybrid"
    assert {item["state"] for item in policy["states"]} == {"defer", "block", "rollback"}
    assert result["checks"]["safe_fallback_is_current_default"] is True
    assert result["checks"]["operator_remediation_present"] is True
    assert result["next_gate"] == "operator_promotion_command"


def test_retriever_failure_rollback_policy_report_is_public_safe() -> None:
    rendered = render_markdown(build_retriever_failure_rollback_policy())

    assert "RPG3 Failure And Rollback Policy" in rendered
    assert "restore `hybrid`" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
