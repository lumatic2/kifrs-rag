from __future__ import annotations

from scripts.real_accountant_invite_dispatch_gate import (
    check_invite_dispatch_gate,
    render_report,
)


def test_invite_dispatch_gate_is_ready_before_manual_send() -> None:
    result = check_invite_dispatch_gate()

    assert result["ok"], result["errors"]
    assert result["reviewer_alias"] == "reviewer-001"
    assert result["current_outreach_counts"]["not_sent"] >= 1
    assert result["current_outreach_counts"]["sent"] == 0
    assert result["post_send_simulation"]["ok"] is True
    assert result["post_send_simulation"]["counts"]["sent"] == 1
    assert result["post_send_simulation"]["row"]["invite_sent"] is True
    assert "real_accountant_outreach_update.py" in result["post_send_update_command"]
    assert "C:/" not in result["post_send_update_command"]
    assert "docs/reports/real-accountant-session/outreach-log.sample.jsonl" in result["post_send_update_command"]


def test_invite_dispatch_gate_report_keeps_manual_send_boundary() -> None:
    rendered = render_report(check_invite_dispatch_gate())

    assert "RS2 Invite Dispatch Gate" in rendered
    assert "does not send the invite" in rendered
    assert "operator actually sends the invite" in rendered
    assert "customer_name" not in rendered
    assert "source_body" not in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
