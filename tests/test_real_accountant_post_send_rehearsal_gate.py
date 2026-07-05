from __future__ import annotations

from scripts.real_accountant_post_send_rehearsal_gate import check_post_send_rehearsal, render_markdown


def test_post_send_rehearsal_validates_receipt_and_sent_transition() -> None:
    result = check_post_send_rehearsal()

    assert result["ok"], result["errors"]
    assert result["receipt_ok"] is True
    assert result["actual_send_attested"] is False
    assert result["simulation"]["ok"] is True
    assert result["simulation"]["outreach_counts"]["sent"] == 1
    assert result["simulation"]["next_action_status"] == "waiting_on_reviewer_reply"
    assert "real_accountant_response_packet.py" in result["simulation"]["next_action_command"]


def test_post_send_rehearsal_markdown_states_boundaries() -> None:
    rendered = render_markdown(check_post_send_rehearsal())

    assert "Real Accountant Post-Send Rehearsal Gate" in rendered
    assert "does not send the invite" in rendered
    assert "does not mutate the real outreach ledger" in rendered
    assert "actual_send_attested" in rendered
    assert "api_key" not in rendered
    assert "source_body" not in rendered
