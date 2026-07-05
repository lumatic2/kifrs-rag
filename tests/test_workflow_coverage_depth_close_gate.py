from __future__ import annotations

from scripts.workflow_coverage_depth_close_gate import build_close_gate, render_markdown


def test_workflow_coverage_depth_close_gate_closes_horizon() -> None:
    result = build_close_gate()

    assert result["ok"] is True
    assert result["horizon"] == "workflow-coverage-depth-expansion"
    assert result["completed_milestone"] == "WCD5"
    assert result["close_result"] == "coverage_depth_expanded"
    assert result["new_workflow"] == "audit_disclosure_tie_out"
    assert result["next_horizon"] == "demo-rehearsal-quality-loop"
    assert result["checks"]["all_evidence_exists"] is True
    assert result["checks"]["metric_not_field_validation"] is True


def test_workflow_coverage_depth_close_gate_markdown_is_public_safe() -> None:
    rendered = render_markdown(build_close_gate())

    assert "Workflow Coverage Depth Expansion Close Report" in rendered
    assert "coverage_depth_expanded" in rendered
    assert "demo-rehearsal-quality-loop" in rendered
    assert "api_key" not in rendered
    assert "secret" not in rendered
    assert "source_body" not in rendered
    assert "packaging" not in rendered.lower()
