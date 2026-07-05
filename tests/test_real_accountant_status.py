from __future__ import annotations

import json

from scripts.real_accountant_status import render_text, summarize_status


def test_status_reports_current_repo_next_action() -> None:
    status = summarize_status(
        root=__import__("pathlib").Path.cwd(),
        manifest=__import__("pathlib").Path("docs/reports/real-accountant-session/session_manifest.json"),
        outreach_ledger=__import__("pathlib").Path("docs/reports/real-accountant-session/outreach-log.sample.jsonl"),
    )

    assert status["session_mode"] == "ready_to_schedule"
    assert status["close_ready"] is False
    assert status["next_action"] == "Send reviewer invite and update outreach ledger to sent."


def test_status_moves_to_session_when_invite_sent(tmp_path) -> None:
    manifest = tmp_path / "session_manifest.json"
    manifest.write_text(json.dumps({"actual_feedback_evidence": False}), encoding="utf-8")
    outreach = tmp_path / "outreach.jsonl"
    outreach.write_text(
        json.dumps(
            {
                "reviewer_alias": "reviewer-001",
                "status": "sent",
                "invite_sent": True,
                "channel": "manual",
                "contacted_at": "2026-07-05",
                "follow_up_by": "2026-07-08",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    status = summarize_status(root=tmp_path, manifest=manifest, outreach_ledger=outreach)

    assert status["next_action"] == "Schedule the reviewer session or update outreach ledger."
    assert "reviewer invite has not been sent" not in status["blocked_by"]


def test_status_reflects_declined_reviewer_without_claiming_unsent(tmp_path) -> None:
    manifest = tmp_path / "session_manifest.json"
    manifest.write_text(json.dumps({"actual_feedback_evidence": False}), encoding="utf-8")
    outreach = tmp_path / "outreach.jsonl"
    outreach.write_text(
        json.dumps(
            {
                "reviewer_alias": "reviewer-001",
                "status": "declined",
                "invite_sent": True,
                "channel": "manual",
                "contacted_at": "2026-07-05",
                "follow_up_by": "2026-07-08",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    status = summarize_status(root=tmp_path, manifest=manifest, outreach_ledger=outreach)

    assert status["next_action"] == "Record decline outcome, then invite another reviewer or pause RS2."
    assert "reviewer declined; no scheduled or completed reviewer session" in status["blocked_by"]
    assert "reviewer invite has not been sent" not in status["blocked_by"]


def test_render_text_includes_next_action(tmp_path) -> None:
    manifest = tmp_path / "session_manifest.json"
    manifest.write_text(json.dumps({"actual_feedback_evidence": False}), encoding="utf-8")
    outreach = tmp_path / "outreach.jsonl"
    outreach.write_text("", encoding="utf-8")
    status = summarize_status(root=tmp_path, manifest=manifest, outreach_ledger=outreach)

    rendered = render_text(status)

    assert "Real Accountant Session Status" in rendered
    assert "Next action: Send reviewer invite" in rendered
