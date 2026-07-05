from __future__ import annotations

from scripts.external_source_connector_body_leak_policy_gate import build_leak_policy_gate, render_markdown


def test_external_source_connector_body_leak_policy_gate_scans_reports_safely() -> None:
    result = build_leak_policy_gate()

    assert result["ok"] is True
    assert result["horizon"] == "external-source-body-connector-expansion"
    assert result["completed_milestone"] == "ESB4"
    assert result["hit_count"] == 0
    assert result["blocked_marker_count"] >= 5
    assert result["checks"]["scanned_reports_exist"] is True
    assert result["checks"]["no_blocked_markers_in_scanned_reports"] is True
    assert all(case["real_payload"] is False for case in result["negative_cases"])
    assert all(case["marker_rendered"] is False for case in result["negative_cases"])
    assert result["next_leaf"] == "ESB5_horizon_close_and_workflow_coverage_handoff"


def test_external_source_connector_body_leak_policy_gate_markdown_is_public_safe() -> None:
    rendered = render_markdown(build_leak_policy_gate())

    assert "ESB4 Connector Leak And Policy Gate" in rendered
    assert "blocked marker count" in rendered
    assert "hit count: 0" in rendered
    assert "api_key" not in rendered
    assert "secret" not in rendered
    assert "password" not in rendered
    assert "kifrs.db" not in rendered
    assert "source_body" not in rendered
