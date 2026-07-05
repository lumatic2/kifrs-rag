from __future__ import annotations

from scripts.external_source_connector_body_close_gate import build_close_gate, render_markdown


def test_external_source_connector_body_close_gate_closes_horizon() -> None:
    result = build_close_gate()

    assert result["ok"] is True
    assert result["horizon"] == "external-source-body-connector-expansion"
    assert result["completed_milestone"] == "ESB5"
    assert result["close_result"] == "connector_body_lane_ready"
    assert result["next_horizon"] == "workflow-coverage-depth-expansion"
    assert result["checks"]["all_evidence_exists"] is True
    assert result["checks"]["all_required_phrases_present"] is True
    assert result["checks"]["leak_gate_passed"] is True


def test_external_source_connector_body_close_gate_markdown_is_public_safe() -> None:
    rendered = render_markdown(build_close_gate())

    assert "External Source-Body Connector Expansion Close Report" in rendered
    assert "connector_body_lane_ready" in rendered
    assert "workflow-coverage-depth-expansion" in rendered
    assert "api_key" not in rendered
    assert "secret" not in rendered
    assert "password" not in rendered
    assert "kifrs.db" not in rendered
    assert "source_body" not in rendered
