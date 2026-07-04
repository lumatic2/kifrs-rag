from __future__ import annotations

import json

import pytest

from scripts.real_accountant_outreach_check import check_outreach, load_outreach
from scripts.real_accountant_outreach_update import upsert_outreach


def test_upsert_outreach_adds_public_safe_alias(tmp_path) -> None:
    path = tmp_path / "outreach.jsonl"

    row = upsert_outreach(
        path,
        reviewer_alias="reviewer-001",
        status="sent",
        channel="manual",
        contacted_at="2026-07-05",
        follow_up_by="2026-07-08",
        notes="invite sent",
    )

    assert row["invite_sent"] is True
    loaded = load_outreach(path)
    assert len(loaded) == 1
    assert loaded[0]["status"] == "sent"
    ok, errors, counts = check_outreach(path)
    assert ok is True
    assert errors == []
    assert counts["sent"] == 1


def test_upsert_outreach_updates_existing_alias(tmp_path) -> None:
    path = tmp_path / "outreach.jsonl"
    upsert_outreach(
        path,
        reviewer_alias="reviewer-001",
        status="sent",
        channel="manual",
        contacted_at="2026-07-05",
        follow_up_by="2026-07-08",
    )
    upsert_outreach(
        path,
        reviewer_alias="reviewer-001",
        status="scheduled",
        channel="manual",
        contacted_at="2026-07-05",
        follow_up_by="2026-07-08",
    )

    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]

    assert len(rows) == 1
    assert rows[0]["status"] == "scheduled"
    assert rows[0]["invite_sent"] is True


def test_upsert_outreach_rejects_non_alias_identifier(tmp_path) -> None:
    with pytest.raises(ValueError, match="public-safe alias"):
        upsert_outreach(
            tmp_path / "outreach.jsonl",
            reviewer_alias="actual-name",
            status="sent",
            channel="manual",
            contacted_at="2026-07-05",
            follow_up_by="2026-07-08",
        )


def test_upsert_outreach_not_sent_keeps_invite_false(tmp_path) -> None:
    row = upsert_outreach(
        tmp_path / "outreach.jsonl",
        reviewer_alias="reviewer-001",
        status="not_sent",
        channel="manual",
        contacted_at="2026-07-05",
        follow_up_by="2026-07-08",
    )

    assert row["invite_sent"] is False
