from __future__ import annotations

import shutil

from scripts.accounting_intelligence_decision_queue import (
    DEFAULT_OUTREACH_LEDGER,
    DEFAULT_SESSION_MANIFEST,
    _reviewer_invite_decision,
    build_decision_queue,
    render_markdown,
)
from scripts.real_accountant_outreach_update import upsert_outreach


def test_decision_queue_parks_external_feedback_by_default() -> None:
    queue = build_decision_queue()

    assert queue["ok"], queue["errors"]
    assert queue["mode"] == "cached_reports"
    assert queue["open_decision_count"] == 4
    assert queue["operator_action_required_count"] == 0
    assert queue["recommended_next_decision"] is None

    decisions = {decision["id"]: decision for decision in queue["decisions"]}
    assert decisions["external_accountant_feedback"]["priority"] == 1
    assert decisions["external_accountant_feedback"]["status"] == "parked_by_user_request"
    assert decisions["external_accountant_feedback"]["operator_action_required"] is False
    assert "excluded until the user explicitly asks" in decisions["external_accountant_feedback"]["user_decision"]
    assert decisions["approve_external_body_authorization_record"]["status"] == "parked_until_explicit_authorization"
    assert decisions["approve_external_body_authorization_record"]["current_blocker"] == "authorized_by is required"
    assert decisions["approve_local_private_parser_adapter"]["status"] == "waiting_on_eval_evidence"
    assert decisions["approve_default_retriever_promotion"]["status"] == "waiting_on_eval_evidence"


def test_decision_queue_markdown_is_action_oriented_and_public_safe() -> None:
    rendered = render_markdown(build_decision_queue())

    assert "What User Decides" in rendered
    assert "external_accountant_feedback" in rendered
    assert "approve_external_body_authorization_record" in rendered
    assert "parked_by_user_request" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered


def test_reviewer_decision_transitions_after_invite_is_sent() -> None:
    decision = _reviewer_invite_decision(
        _session_with_counts(
            {
                "not_sent": 0,
                "sent": 1,
                "responded": 0,
                "scheduled": 0,
                "declined": 0,
                "completed": 0,
            }
        )
    )

    assert decision["status"] == "waiting_on_reviewer_reply"
    assert decision["operator_action_required"] is True
    assert "follow up, schedule" in decision["user_decision"]
    assert "real_accountant_response_packet.py" in decision["next_command"]
    assert "real_accountant_invite_send_receipt.py" in decision["receipt_command"]
    assert "--require-sent" in decision["receipt_command"]
    assert "real_accountant_response_packet.py" in decision["after_command"]
    assert "--expected-status sent" in decision["verify_command"]


def test_decision_queue_accepts_explicit_outreach_ledger(tmp_path) -> None:
    copied_ledger = tmp_path / "outreach.jsonl"
    shutil.copyfile(DEFAULT_OUTREACH_LEDGER, copied_ledger)
    upsert_outreach(
        copied_ledger,
        reviewer_alias="reviewer-001",
        status="sent",
        channel="manual",
        contacted_at="2026-07-05",
        follow_up_by="2026-07-08",
        notes="invite sent",
    )

    queue = build_decision_queue(
        manifest=DEFAULT_SESSION_MANIFEST,
        outreach_ledger=copied_ledger,
    )

    decisions = {decision["id"]: decision for decision in queue["decisions"]}
    assert queue["recommended_next_decision"] is None
    assert decisions["external_accountant_feedback"]["status"] == "parked_by_user_request"
    assert decisions["external_accountant_feedback"]["next_command"] == "none"


def test_reviewer_decision_transitions_after_session_is_scheduled() -> None:
    decision = _reviewer_invite_decision(
        _session_with_counts(
            {
                "not_sent": 0,
                "sent": 0,
                "responded": 0,
                "scheduled": 1,
                "declined": 0,
                "completed": 0,
            }
        )
    )

    assert decision["status"] == "session_scheduled"
    assert decision["operator_action_required"] is True
    assert "run the scheduled session" in decision["user_decision"]
    assert "real_accountant_run_sheet.py" in decision["next_command"]
    assert "real_accountant_notes_scaffold.py" in decision["after_command"]
    assert "--expected-status scheduled" in decision["verify_command"]


def test_reviewer_decision_transitions_after_session_completed() -> None:
    decision = _reviewer_invite_decision(
        _session_with_counts(
            {
                "not_sent": 0,
                "sent": 0,
                "responded": 0,
                "scheduled": 0,
                "declined": 0,
                "completed": 1,
            }
        )
    )

    assert decision["status"] == "needs_notes_capture"
    assert decision["operator_action_required"] is True
    assert "convert actual public-safe notes" in decision["user_decision"]
    assert "real_accountant_post_session_final_gate.py" in decision["next_command"]
    assert "real_accountant_capture.py" in decision["after_command"]
    assert "--expected-status completed" in decision["verify_command"]


def _session_with_counts(counts: dict[str, int]) -> dict[str, object]:
    return {
        "outreach_counts": counts,
        "close_ready": False,
        "blocked_by": ["test blocker"],
    }
