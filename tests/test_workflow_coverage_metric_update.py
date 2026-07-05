from __future__ import annotations

from scripts.workflow_coverage_metric_update import (
    build_workflow_coverage_metric_update,
    render_markdown,
)


def test_workflow_coverage_metric_update_records_new_candidate_without_overclaim() -> None:
    result = build_workflow_coverage_metric_update()

    assert result["ok"], result["errors"]
    assert result["horizon"] == "workflow-coverage-expansion"
    assert result["completed_milestone"] == "WCE4"
    assert result["new_workflow"]["workflow_id"] == "1037_provisions"
    assert result["new_workflow"]["coverage_status"] == "conditional_decision_prep_adapter"
    assert "fully_automated" not in result["new_workflow"]["coverage_status"]
    assert result["coverage_map"]["axis_2_scenario_completion"]["review_packs"] == 24
    assert result["coverage_map"]["axis_2_scenario_completion"]["automated_packs"] >= 20
    assert result["checks"]["no_completion_overclaim"] is True
    assert result["new_workflow"]["limits"]


def test_workflow_coverage_metric_update_report_is_public_safe() -> None:
    rendered = render_markdown(build_workflow_coverage_metric_update())

    assert "WCE4 Coverage Metric Update" in rendered
    assert "1037_provisions" in rendered
    assert "human review required" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
