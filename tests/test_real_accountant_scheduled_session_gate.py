from __future__ import annotations

from scripts.real_accountant_scheduled_session_gate import check_scheduled_session_gate, render_report


def test_scheduled_session_gate_simulates_scheduled_state_without_actual_evidence() -> None:
    result = check_scheduled_session_gate()

    assert result["ok"], result["errors"]
    assert result["scheduled_simulation"]["counts"]["scheduled"] == 1
    assert result["scheduled_simulation"]["session_mode"] == "ready_to_schedule"
    assert "Run the scheduled accountant session" in result["scheduled_simulation"]["status_next_action"]
    assert result["scheduled_simulation"]["close_ready"] is False
    assert result["close_gate_correctly_blocked"] is True
    assert result["run_sheet_ready"]["ok"] is True


def test_scheduled_session_gate_report_names_boundary_without_protected_markers() -> None:
    report = render_report(check_scheduled_session_gate())

    assert "does not schedule the reviewer" in report
    assert "Close remains blocked" in report
    assert "actual feedback evidence" in report
    assert "source_body" not in report
    assert "api_key" not in report
    assert "token" not in report
