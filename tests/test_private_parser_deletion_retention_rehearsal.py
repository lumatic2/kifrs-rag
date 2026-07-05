from __future__ import annotations

from scripts.private_parser_deletion_retention_rehearsal import build_deletion_retention_rehearsal, render_markdown


def test_private_parser_deletion_retention_rehearsal_tracks_lifecycle() -> None:
    rehearsal = build_deletion_retention_rehearsal()

    assert rehearsal["ok"] is True
    assert rehearsal["horizon"] == "private-parser-realism-hardening"
    assert rehearsal["completed_milestone"] == "PPR3"
    assert rehearsal["next_leaf"] == "PPR4_parser_leak_and_public_report_gate"
    assert all(item["exists"] for item in rehearsal["evidence"])
    assert any(item["state"] == "deleted" for item in rehearsal["lifecycle"])
    assert all(item["public_payload"] is False for item in rehearsal["lifecycle"])


def test_private_parser_deletion_retention_rehearsal_markdown_is_public_safe() -> None:
    rendered = render_markdown(build_deletion_retention_rehearsal())

    assert "PPR3 Deletion And Retention Rehearsal" in rendered
    assert "Raw local fixtures end deleted" in rendered
    assert "structured facts" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "kifrs.db" not in rendered
    assert "source_body" not in rendered
