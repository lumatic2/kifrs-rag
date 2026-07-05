from __future__ import annotations

from scripts.rag_reliability_baseline_inventory import build_inventory, render_markdown


def test_rr1_inventory_lists_commands_and_retriever_state() -> None:
    inventory = build_inventory()

    assert inventory["ok"], inventory["retriever_state"]["promotion_blockers"]
    assert inventory["milestone"] == "RR1"
    assert inventory["retriever_state"]["default_mode"] == "hybrid"
    assert inventory["retriever_state"]["target_retriever"] == "ifrs1109_classification_hybrid"
    assert inventory["retriever_state"]["target_retriever_exposed_in_mcp"] is False
    assert inventory["retriever_state"]["promotion_decision"] == "defer"
    public_names = {command["name"] for command in inventory["public_safe_commands"]}
    assert "focused_pytest" in public_names
    assert "local_rag_threshold_gate" in public_names
    local_names = {command["name"] for command in inventory["local_data_commands"]}
    assert "full_retrieval_goldset_gate" in local_names
    assert any(report["name"] == "rag_quality_refresh_close" and report["present"] for report in inventory["evidence_reports"])


def test_rr1_inventory_markdown_is_public_safe() -> None:
    rendered = render_markdown(build_inventory())

    assert "RR1 RAG Baseline Inventory" in rendered
    assert "Public-Safe Commands" in rendered
    assert "Local Data / Protected Boundary Commands" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
