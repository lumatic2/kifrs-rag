from __future__ import annotations

from scripts.opt_in_retriever_promotion_decision_gate import (
    check_promotion_decision_gate,
    render_report,
)


def test_promotion_decision_gate_defers_without_actual_evidence_or_authorization() -> None:
    result = check_promotion_decision_gate()

    assert result["ok"], result["errors"]
    assert result["decision"]["decision"] == "defer"
    assert result["decision"]["promote_to_default"] is False
    assert result["decision"]["target_retriever"] == "ifrs1109_classification_hybrid"
    assert result["decision"]["demo_validation_ok"] is True
    blockers = " ".join(result["decision"]["blockers"])
    assert "actual accountant feedback evidence" in blockers
    assert "explicit user authorization" in blockers
    assert result["demo_validation"]["target_recall20"] == 1.0
    assert result["demo_validation"]["target_buckets"]["absent"] == 0


def test_promotion_decision_gate_can_promote_when_all_preconditions_are_met() -> None:
    result = check_promotion_decision_gate(
        explicit_authorization=True,
        actual_accountant_evidence_override=True,
    )

    assert result["ok"], result["errors"]
    assert result["decision"]["decision"] == "promote"
    assert result["decision"]["promote_to_default"] is True
    assert result["decision"]["blockers"] == []
    assert result["next_leaf"] == "default retriever promotion implementation"


def test_promotion_decision_gate_report_keeps_runtime_unchanged_boundary() -> None:
    rendered = render_report(check_promotion_decision_gate())

    assert "ORPD1 Opt-In Retriever Promotion Decision Gate" in rendered
    assert "remains opt-in" in rendered
    assert "does not change runtime defaults" in rendered
    assert "current default retriever remains unchanged" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
