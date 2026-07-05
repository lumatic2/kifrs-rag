from __future__ import annotations

from scripts.accounting_intelligence_next_action_sequence_gate import check_next_action_sequence, render_markdown


def test_next_action_sequence_gate_checks_command_after_verify() -> None:
    result = check_next_action_sequence()

    assert result["ok"], result["errors"]
    assert result["next_action"]["decision"] == "send_reviewer_invite"
    assert "real_accountant_invite_packet.py" in result["next_action"]["command"]
    assert "real_accountant_invite_send_receipt.py" in result["next_action"]["receipt"]
    assert "--write-template" in result["next_action"]["receipt"]
    assert "real_accountant_outreach_update.py" in result["next_action"]["after"]
    assert "--status sent" in result["next_action"]["after"]
    assert "real_accountant_outreach_transition_verify.py" in result["next_action"]["verify"]
    assert "--expected-status sent" in result["next_action"]["verify"]
    assert result["post_send_simulation"]["ok"] is True
    assert result["post_send_simulation"]["next_action_status"] == "waiting_on_reviewer_reply"


def test_next_action_sequence_gate_markdown_is_public_safe() -> None:
    rendered = render_markdown(check_next_action_sequence())

    assert "Accounting Intelligence Next Action Sequence Gate" in rendered
    assert "real_accountant_invite_send_receipt.py" in rendered
    assert "post-send ledger update" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
