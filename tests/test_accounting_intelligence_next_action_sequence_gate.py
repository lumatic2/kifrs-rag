from __future__ import annotations

from scripts.accounting_intelligence_next_action_sequence_gate import check_next_action_sequence, render_markdown


def test_next_action_sequence_gate_checks_command_after_verify() -> None:
    result = check_next_action_sequence()

    assert result["ok"], result["errors"]
    assert result["next_action"]["decision"] is None
    assert result["next_action"]["command"] == "none"
    assert result["sequence_check"]["ok"] is True
    assert result["sequence_check"]["mode"] == "no_active_user_action"


def test_next_action_sequence_gate_markdown_is_public_safe() -> None:
    rendered = render_markdown(check_next_action_sequence())

    assert "Accounting Intelligence Next Action Sequence Gate" in rendered
    assert "no_active_user_action" in rendered
    assert "internal technical work can continue" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
