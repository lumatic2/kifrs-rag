from __future__ import annotations

from scripts.accounting_intelligence_next_action import build_next_action, render_markdown


def test_next_action_uses_cached_decision_queue_and_recommends_invite() -> None:
    action = build_next_action()

    assert action["ok"], action["errors"]
    assert action["mode"] == "cached_reports"
    assert action["recommended_next_decision"] == "send_reviewer_invite"
    assert action["status"] == "needs_user_action"
    assert action["operator_action_required"] is True
    assert "Which reviewer" in action["user_decision"]
    assert "reviewer invite" in action["current_blocker"]
    assert "real_accountant_invite_packet.py" in action["next_command"]
    assert action["open_decision_count"] == 4
    assert action["operator_action_required_count"] == 2


def test_next_action_markdown_is_public_safe_and_actionable() -> None:
    rendered = render_markdown(build_next_action())

    assert "Accounting Intelligence Next Action" in rendered
    assert "Which reviewer" in rendered
    assert "real_accountant_invite_packet.py" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
