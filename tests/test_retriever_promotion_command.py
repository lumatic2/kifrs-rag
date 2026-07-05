from __future__ import annotations

from scripts.retriever_promotion_command import build_retriever_promotion_command, render_markdown


def test_retriever_promotion_command_is_dry_run_and_visible() -> None:
    result = build_retriever_promotion_command()
    output = result["command_output"]

    assert result["ok"], result["errors"]
    assert result["horizon"] == "runtime-retriever-promotion-gate"
    assert result["completed_milestone"] == "RPG4"
    assert output["decision"] == "defer"
    assert output["mutates_runtime"] is False
    assert output["target_retriever"] == "ifrs1109_classification_hybrid"
    assert output["current_default"] == "hybrid"
    assert output["safe_fallback"] == "hybrid"
    assert output["required_before_promote"]
    assert result["checks"]["dry_run_only"] is True
    assert result["next_gate"] == "promotion_gate_close_report"


def test_retriever_promotion_command_report_is_public_safe() -> None:
    rendered = render_markdown(build_retriever_promotion_command())

    assert "RPG4 Operator Promotion Command" in rendered
    assert "does not mutate runtime defaults" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
