from __future__ import annotations

import shutil

from scripts.real_accountant_outreach_transition_verify import DEFAULT_LEDGER, verify_transition, render_markdown
from scripts.real_accountant_outreach_update import upsert_outreach


def test_verify_transition_accepts_sent_copied_ledger(tmp_path) -> None:
    copied_ledger = tmp_path / "outreach.jsonl"
    shutil.copyfile(DEFAULT_LEDGER, copied_ledger)
    upsert_outreach(
        copied_ledger,
        reviewer_alias="reviewer-001",
        status="sent",
        channel="manual",
        contacted_at="2026-07-05",
        follow_up_by="2026-07-08",
        notes="invite sent",
    )

    result = verify_transition(ledger=copied_ledger, expected_status="sent")

    assert result["ok"], result["errors"]
    assert result["outreach_counts"]["sent"] == 1
    assert result["next_action_status"] == "waiting_on_reviewer_reply"
    assert "real_accountant_response_packet.py" in result["next_action_command"]


def test_verify_transition_rejects_default_pre_send_ledger() -> None:
    result = verify_transition(expected_status="sent")

    assert result["ok"] is False
    assert "expected at least one sent outreach row" in result["errors"]


def test_verify_transition_markdown_is_public_safe(tmp_path) -> None:
    copied_ledger = tmp_path / "outreach.jsonl"
    shutil.copyfile(DEFAULT_LEDGER, copied_ledger)
    upsert_outreach(
        copied_ledger,
        reviewer_alias="reviewer-001",
        status="scheduled",
        channel="manual",
        contacted_at="2026-07-05",
        follow_up_by="2026-07-08",
        notes="session scheduled",
    )

    rendered = render_markdown(verify_transition(ledger=copied_ledger, expected_status="scheduled"))

    assert "Real Accountant Outreach Transition Verify" in rendered
    assert "real_accountant_run_sheet.py" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
