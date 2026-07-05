from __future__ import annotations

from scripts.real_accountant_pre_send_final_gate import check_pre_send_final_gate, render_report


def test_pre_send_final_gate_confirms_ready_but_not_sent_state() -> None:
    result = check_pre_send_final_gate()

    assert result["ok"], result["errors"]
    assert result["status"]["session_mode"] == "ready_to_schedule"
    assert result["status"]["close_ready"] is False
    assert result["status"]["outreach_counts"]["not_sent"] == 1
    assert all(result["readiness_gates"].values())
    assert len(result["execution_run_order_phases"]) == 6
    assert "real_accountant_outreach_update.py" in result["post_send_update_command"]


def test_pre_send_final_gate_report_preserves_manual_send_boundary() -> None:
    report = render_report(check_pre_send_final_gate())

    assert "does not send the reviewer invite" in report
    assert "manual operator action" in report
    assert "reviewer identity, sending, scheduling, and feedback notes stay user/operator-owned" in report
    assert "source_body" not in report
    assert "api_key" not in report
    assert "token" not in report
