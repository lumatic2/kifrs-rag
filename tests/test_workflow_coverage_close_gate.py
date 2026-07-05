from __future__ import annotations

from scripts.workflow_coverage_close_gate import build_workflow_coverage_close_gate, render_markdown


def test_workflow_coverage_close_gate_passes_and_routes_next_horizon() -> None:
    result = build_workflow_coverage_close_gate()

    assert result["ok"], result["errors"]
    assert result["horizon"] == "workflow-coverage-expansion"
    assert result["completed_milestone"] == "WCE5"
    assert result["close_status"] == "closed"
    assert result["new_workflow"] == "1037_provisions"
    assert result["coverage_status"] == "conditional_decision_prep_adapter"
    assert result["checks"]["wce1_ranking_ok"] is True
    assert result["checks"]["wce2_contract_ok"] is True
    assert result["checks"]["wce3_adapter_ok"] is True
    assert result["checks"]["wce4_metric_ok"] is True
    assert result["checks"]["recommended_candidate_carried"] is True
    assert result["checks"]["product_trust_carried"] is True
    assert result["checks"]["controlled_lane_carried"] is True
    assert result["next_horizon"] == "runtime-retriever-promotion-gate"


def test_workflow_coverage_close_gate_report_is_public_safe() -> None:
    rendered = render_markdown(build_workflow_coverage_close_gate())

    assert "Workflow Coverage Expansion Close Gate" in rendered
    assert "1037_provisions" in rendered
    assert "runtime-retriever-promotion-gate" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
