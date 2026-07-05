from __future__ import annotations

from scripts.real_accountant_external_action_boundary_gate import (
    check_external_action_boundary_gate,
    render_report,
)


def test_external_action_boundary_gate_freezes_ready_but_external_state() -> None:
    result = check_external_action_boundary_gate()

    assert result["ok"], result["errors"]
    assert result["boundary_type"] == "external_action_required"
    assert result["internal_readiness_complete"] is True
    assert result["ready_item_count"] == result["total_item_count"]
    assert result["session_mode"] == "ready_to_schedule"
    assert result["close_ready"] is False
    assert result["outreach_counts"] == {
        "completed": 0,
        "declined": 0,
        "not_sent": 1,
        "responded": 0,
        "scheduled": 0,
        "sent": 0,
    }
    assert result["next_action"] == "Send reviewer invite and update outreach ledger to sent."
    assert "manual reviewer invite send" in result["repo_side_recommendation"]
    assert "Do not add another readiness gate" in result["repo_side_recommendation"]


def test_external_action_boundary_report_is_public_safe_and_actionable() -> None:
    report = render_report(check_external_action_boundary_gate())

    assert "not another readiness gate" in report
    assert "manual reviewer invite send" in report
    assert "Do not close the real-accountant-session horizon yet." in report
    assert "Do not mark actual_feedback_evidence true" in report
    assert "2026-07-05-operator-execution-brief.md" in report
    assert "source_body" not in report
    assert "api_key" not in report
    assert "token" not in report
    assert "customer_name" not in report
