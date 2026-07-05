from __future__ import annotations

from scripts.rag_quality_validation_contract import build_validation_contract, render_markdown


def test_rag_quality_validation_contract_defines_commands_metrics_and_blockers() -> None:
    contract = build_validation_contract()

    assert contract["ok"] is True
    assert contract["horizon"] == "rag-quality-fresh-validation"
    assert contract["completed_milestone"] == "RQF1"
    assert contract["next_leaf"] == "RQF2_current_retriever_baseline_snapshot"
    assert contract["contract"]["default_change_allowed"] is False
    assert all(command["evidence_exists"] for command in contract["commands"])
    assert {metric["name"] for metric in contract["metrics"]} >= {
        "recall_at_20",
        "regression_count",
        "latency_budget_seconds",
        "rollback_available",
    }
    assert "explicit authorization missing" in contract["promotion_blockers"]


def test_rag_quality_validation_contract_markdown_is_public_safe() -> None:
    rendered = render_markdown(build_validation_contract())

    assert "RQF1 Validation Corpus And Acceptance Contract" in rendered
    assert "Default change allowed in RQF1: False" in rendered
    assert "python scripts\\default_retriever_guard.py --format text" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "kifrs.db" not in rendered
    assert "source_body" not in rendered
