from __future__ import annotations

import json

from scripts.real_accountant_outreach_check import check_outreach


def test_sample_outreach_ledger_passes() -> None:
    ok, errors, counts = check_outreach(
        __import__("pathlib").Path("docs/reports/real-accountant-session/outreach-log.sample.jsonl")
    )

    assert ok is True
    assert errors == []
    assert counts["not_sent"] == 1


def test_outreach_checker_rejects_sent_without_invite_flag(tmp_path) -> None:
    path = tmp_path / "outreach.jsonl"
    row = {
        "reviewer_alias": "reviewer-001",
        "status": "sent",
        "invite_sent": False,
        "channel": "manual",
        "contacted_at": "2026-07-05",
        "follow_up_by": "2026-07-08",
    }
    path.write_text(json.dumps(row) + "\n", encoding="utf-8")

    ok, errors, _counts = check_outreach(path)

    assert ok is False
    assert errors == ["line 1: status sent requires invite_sent true"]


def test_outreach_checker_rejects_duplicate_alias(tmp_path) -> None:
    path = tmp_path / "outreach.jsonl"
    row = {
        "reviewer_alias": "reviewer-001",
        "status": "not_sent",
        "invite_sent": False,
        "channel": "manual",
        "contacted_at": "2026-07-05",
        "follow_up_by": "2026-07-08",
    }
    path.write_text(json.dumps(row) + "\n" + json.dumps(row) + "\n", encoding="utf-8")

    ok, errors, _counts = check_outreach(path)

    assert ok is False
    assert errors == ["line 2: duplicate reviewer_alias: reviewer-001"]


def test_outreach_checker_rejects_protected_marker(tmp_path) -> None:
    path = tmp_path / "outreach.jsonl"
    row = {
        "reviewer_alias": "reviewer-001",
        "status": "not_sent",
        "invite_sent": False,
        "channel": "manual",
        "contacted_at": "2026-07-05",
        "follow_up_by": "2026-07-08",
        "client_name": "Do not store",
    }
    path.write_text(json.dumps(row) + "\n", encoding="utf-8")

    ok, errors, _counts = check_outreach(path)

    assert ok is False
    assert errors == ["line 1: protected marker found"]
