from __future__ import annotations

from scripts.accounting_intelligence_decision_queue import build_decision_queue, render_markdown


def test_decision_queue_prioritizes_reviewer_invite() -> None:
    queue = build_decision_queue()

    assert queue["ok"], queue["errors"]
    assert queue["open_decision_count"] == 4
    assert queue["operator_action_required_count"] == 2
    assert queue["recommended_next_decision"] == "send_reviewer_invite"

    decisions = {decision["id"]: decision for decision in queue["decisions"]}
    assert decisions["send_reviewer_invite"]["priority"] == 1
    assert decisions["send_reviewer_invite"]["status"] == "needs_user_action"
    assert "reviewer invite" in decisions["send_reviewer_invite"]["current_blocker"]
    assert decisions["approve_external_body_authorization_record"]["status"] == "needs_user_action"
    assert decisions["approve_external_body_authorization_record"]["current_blocker"] == "authorized_by is required"
    assert decisions["approve_local_private_parser_adapter"]["status"] == "waiting_on_accountant_evidence"
    assert decisions["approve_default_retriever_promotion"]["status"] == "waiting_on_accountant_evidence"


def test_decision_queue_markdown_is_action_oriented_and_public_safe() -> None:
    rendered = render_markdown(build_decision_queue())

    assert "What User Decides" in rendered
    assert "send_reviewer_invite" in rendered
    assert "approve_external_body_authorization_record" in rendered
    assert "reviewer invite" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
