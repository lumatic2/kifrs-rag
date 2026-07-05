from __future__ import annotations

import shutil

from scripts.accounting_intelligence_decision_queue import DEFAULT_OUTREACH_LEDGER, DEFAULT_SESSION_MANIFEST
from scripts.accounting_intelligence_decision_queue import _reviewer_invite_decision
from scripts.accounting_intelligence_next_action import build_next_action, build_next_action_from_queue, render_markdown
from scripts.real_accountant_outreach_update import upsert_outreach


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
    assert "real_accountant_invite_send_receipt.py" in action["receipt_command"]
    assert "--write-template" in action["receipt_command"]
    assert "real_accountant_apply_invite_receipt.py" in action["after_command"]
    assert "--receipt" in action["after_command"]
    assert "real_accountant_outreach_transition_verify.py" in action["verify_command"]
    assert "--expected-status sent" in action["verify_command"]
    assert action["open_decision_count"] == 4
    assert action["operator_action_required_count"] == 2


def test_next_action_markdown_is_public_safe_and_actionable() -> None:
    rendered = render_markdown(build_next_action())

    assert "Accounting Intelligence Next Action" in rendered
    assert "Which reviewer" in rendered
    assert "real_accountant_invite_packet.py" in rendered
    assert "real_accountant_invite_send_receipt.py" in rendered
    assert "real_accountant_apply_invite_receipt.py" in rendered
    assert "real_accountant_outreach_transition_verify.py" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered


def test_next_action_tracks_after_send_state() -> None:
    action = build_next_action_from_queue(
        _queue_with_reviewer_counts(
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

    assert action["recommended_next_decision"] == "send_reviewer_invite"
    assert action["status"] == "waiting_on_reviewer_reply"
    assert "follow up, schedule" in action["user_decision"]
    assert "real_accountant_response_packet.py" in action["next_command"]
    assert "--require-sent" in action["receipt_command"]
    assert "real_accountant_response_packet.py" in action["after_command"]
    assert "--expected-status sent" in action["verify_command"]


def test_next_action_accepts_explicit_outreach_ledger(tmp_path) -> None:
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

    action = build_next_action(
        manifest=DEFAULT_SESSION_MANIFEST,
        outreach_ledger=copied_ledger,
    )

    assert action["recommended_next_decision"] == "send_reviewer_invite"
    assert action["status"] == "waiting_on_reviewer_reply"
    assert "real_accountant_response_packet.py" in action["next_command"]
    assert "--require-sent" in action["receipt_command"]
    assert "real_accountant_response_packet.py" in action["after_command"]
    assert "--expected-status sent" in action["verify_command"]


def test_next_action_tracks_scheduled_state() -> None:
    action = build_next_action_from_queue(
        _queue_with_reviewer_counts(
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

    assert action["status"] == "session_scheduled"
    assert "run the scheduled session" in action["user_decision"]
    assert "real_accountant_run_sheet.py" in action["next_command"]
    assert "real_accountant_notes_scaffold.py" in action["after_command"]
    assert "--expected-status scheduled" in action["verify_command"]


def test_next_action_tracks_completed_session_state() -> None:
    action = build_next_action_from_queue(
        _queue_with_reviewer_counts(
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

    assert action["status"] == "needs_notes_capture"
    assert "convert actual public-safe notes" in action["user_decision"]
    assert "real_accountant_post_session_final_gate.py" in action["next_command"]
    assert "real_accountant_capture.py" in action["after_command"]
    assert "--expected-status completed" in action["verify_command"]


def _queue_with_reviewer_counts(counts: dict[str, int]) -> dict[str, object]:
    decision = _reviewer_invite_decision(
        {
            "outreach_counts": counts,
            "close_ready": False,
            "blocked_by": ["test blocker"],
        }
    )
    return {
        "ok": True,
        "errors": [],
        "mode": "cached_reports",
        "recommended_next_decision": "send_reviewer_invite",
        "open_decision_count": 1,
        "operator_action_required_count": 1,
        "report_path": "docs/reports/2026-07-05-accounting-intelligence-decision-queue.md",
        "decisions": [decision],
    }
