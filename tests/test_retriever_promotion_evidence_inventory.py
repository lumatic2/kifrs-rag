from __future__ import annotations

from scripts.retriever_promotion_evidence_inventory import (
    build_retriever_promotion_evidence_inventory,
    render_markdown,
)


def test_retriever_promotion_inventory_classifies_evidence() -> None:
    result = build_retriever_promotion_evidence_inventory()

    assert result["ok"], result["errors"]
    assert result["horizon"] == "runtime-retriever-promotion-gate"
    assert result["completed_milestone"] == "RPG1"
    assert result["target_retriever"] == "ifrs1109_classification_hybrid"
    assert result["current_default"] == "hybrid"
    assert result["promotion_decision_now"] == "defer"
    assert result["promotion_supporting"]
    assert result["promotion_blocking"]
    assert result["advisory"]
    assert result["missing_evidence"]
    assert result["checks"]["supporting_evidence_present"] is True
    assert result["checks"]["blocking_evidence_present"] is True
    assert result["checks"]["missing_evidence_recorded"] is True


def test_retriever_promotion_inventory_report_is_public_safe() -> None:
    rendered = render_markdown(build_retriever_promotion_evidence_inventory())

    assert "RPG1 Promotion Evidence Inventory" in rendered
    assert "Promotion-Supporting Evidence" in rendered
    assert "Promotion-Blocking Evidence" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
