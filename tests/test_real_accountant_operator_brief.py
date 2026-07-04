from __future__ import annotations

import json

from scripts.real_accountant_operator_brief import build_operator_brief, render_markdown


def test_build_operator_brief_combines_status_invite_and_run_sheet() -> None:
    brief = build_operator_brief(
        root=__import__("pathlib").Path.cwd(),
        manifest=__import__("pathlib").Path("docs/reports/real-accountant-session/session_manifest.json"),
        outreach_ledger=__import__("pathlib").Path("docs/reports/real-accountant-session/outreach-log.sample.jsonl"),
    )

    assert brief["session_mode"] == "ready_to_schedule"
    assert brief["next_action"] == "Send reviewer invite and update outreach ledger to sent."
    assert "post_send_update_command" in brief["send_now"]
    assert "docs/reports/firm-facing-poc/2026-07-05-one-page-brief.md" in brief["open_files"]
    assert "capture" in brief["commands"]


def test_operator_brief_reflects_sent_invite_next_action(tmp_path) -> None:
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

    brief = build_operator_brief(root=tmp_path, manifest=manifest, outreach_ledger=outreach)

    assert brief["next_action"] == "Schedule the reviewer session or update outreach ledger."
    assert "reviewer invite has not been sent" not in brief["blocked_by"]


def test_render_markdown_includes_send_now_and_boundaries() -> None:
    rendered = render_markdown(build_operator_brief(root=__import__("pathlib").Path.cwd()))

    assert "# Real Accountant Session Operator Brief" in rendered
    assert "## Send Now" in rendered
    assert "real_accountant_outreach_update.py" in rendered
    assert "real_accountant_capture.py" in rendered
    assert "Do not store reviewer real name" in rendered
