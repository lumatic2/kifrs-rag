from __future__ import annotations

from scripts.operator_experience_close_gate import build_operator_experience_close_gate, render_markdown


def test_operator_experience_close_gate_closes_queue() -> None:
    result = build_operator_experience_close_gate()

    assert result["ok"], result["errors"]
    assert result["horizon"] == "operator-experience-hardening"
    assert result["completed_milestone"] == "OEH5"
    assert result["close_status"] == "closed"
    assert result["product_weakness_queue_status"] == "closed"
    assert result["next_horizon"] == "none"
    assert result["checks"]["command_discovery_ok"] is True
    assert result["checks"]["run_doctor_ok"] is True
    assert result["checks"]["report_manifest_ok"] is True
    assert result["checks"]["error_recovery_ok"] is True
    assert result["checks"]["protected_boundary_carried"] is True


def test_operator_experience_close_gate_report_is_public_safe() -> None:
    rendered = render_markdown(build_operator_experience_close_gate())

    assert "Operator Experience Hardening Close Gate" in rendered
    assert "product weakness queue" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
