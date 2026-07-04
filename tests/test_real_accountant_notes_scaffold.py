from __future__ import annotations

from scripts.real_accountant_notes_check import check_actual_notes
from scripts.real_accountant_notes_scaffold import render_notes_scaffold


def test_notes_scaffold_renders_required_sections() -> None:
    text = render_notes_scaffold(
        date="2026-07-05",
        reviewer_role="CPA reviewer",
        reviewer_service_line="F-ACC",
        reviewer_experience_context="reviewed accounting advisory workpapers",
        session_mode="async review",
    )

    assert "## Session Metadata" in text
    assert "- Reviewer role: CPA reviewer" in text
    assert "## Safe Correction Candidates" in text
    assert "## Boundary Confirmation" in text


def test_notes_scaffold_fails_checker_until_completed(tmp_path) -> None:
    path = tmp_path / "actual-feedback-notes.md"
    path.write_text(
        render_notes_scaffold(
            date="2026-07-05",
            reviewer_role="CPA reviewer",
            reviewer_service_line="F-ACC",
            reviewer_experience_context="reviewed accounting advisory workpapers",
            session_mode="async review",
        ),
        encoding="utf-8",
    )

    ok, errors = check_actual_notes(path)

    assert ok is False
    assert "actual feedback evidence marker still false" in errors
    assert any(error.startswith("boundary checkbox not confirmed") for error in errors)
