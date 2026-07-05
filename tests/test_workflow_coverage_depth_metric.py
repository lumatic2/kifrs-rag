from __future__ import annotations

from scripts.workflow_coverage_depth_metric import build_metric_update, render_markdown


def test_workflow_coverage_depth_metric_records_new_adapter_without_overclaim() -> None:
    result = build_metric_update()

    assert result["ok"] is True
    assert result["horizon"] == "workflow-coverage-depth-expansion"
    assert result["completed_milestone"] == "WCD4"
    assert result["metric"]["new_workflow_added"] == "audit_disclosure_tie_out"
    assert result["metric"]["workflow_surfaces_with_adapter_evidence"] >= 4
    assert result["metric"]["service_lines_with_adapter_evidence"] <= result["metric"]["service_lines_total"]
    assert result["metric"]["not_a_field_validation_rate"] is True
    assert "F-AUD" in result["touched_service_lines"]
    assert result["next_leaf"] == "WCD5_horizon_close_and_demo_rehearsal_handoff"


def test_workflow_coverage_depth_metric_markdown_is_public_safe() -> None:
    rendered = render_markdown(build_metric_update())

    assert "WCD4 Coverage Depth Metric Update" in rendered
    assert "not a field validation rate: True" in rendered
    assert "api_key" not in rendered
    assert "secret" not in rendered
    assert "source_body" not in rendered
    assert "packaging" not in rendered.lower()
