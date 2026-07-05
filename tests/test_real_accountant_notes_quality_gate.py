from __future__ import annotations

from scripts.real_accountant_capture_readiness_gate import _synthetic_actual_notes
from scripts.real_accountant_notes_quality_gate import build_notes_quality_gate, check_notes_quality, render_report
from scripts.real_accountant_notes_scaffold import render_notes_scaffold


def test_notes_quality_gate_accepts_synthetic_actual_notes(tmp_path) -> None:
    notes = tmp_path / "actual-feedback-notes.md"
    notes.write_text(_synthetic_actual_notes(), encoding="utf-8")

    ok, errors, evidence = check_notes_quality(notes)

    assert ok, errors
    assert evidence["safe_ok"] is True
    assert evidence["score_count"] == 5
    assert evidence["missing_inputs"] >= 1
    assert evidence["review_question_additions"] >= 1
    assert evidence["correction_candidates"] == 1


def test_notes_quality_gate_rejects_scaffold_notes(tmp_path) -> None:
    notes = tmp_path / "actual-feedback-notes.md"
    notes.write_text(
        render_notes_scaffold(
            date="2026-07-05",
            reviewer_role="CPA reviewer",
            reviewer_service_line="F-ACC",
            reviewer_experience_context="reviewed accounting advisory workpapers",
            session_mode="async review",
        ),
        encoding="utf-8",
    )

    ok, errors, _evidence = check_notes_quality(notes)

    assert ok is False
    assert any(error.startswith("safety:") for error in errors)


def test_notes_quality_gate_rejects_weak_correction_candidate(tmp_path) -> None:
    notes = tmp_path / "actual-feedback-notes.md"
    notes.write_text(
        _synthetic_actual_notes().replace(
            "- Suggested fix: Add approval memo evidence to the required human-review questions.",
            "- Suggested fix: Add question.",
        ),
        encoding="utf-8",
    )

    ok, errors, _evidence = check_notes_quality(notes)

    assert ok is False
    assert "candidate 1: suggested fix is too short" in errors


def test_notes_quality_gate_default_mode_uses_synthetic_readiness_when_actual_notes_absent() -> None:
    result = build_notes_quality_gate()

    assert result["ok"], result["errors"]
    assert result["mode"] == "synthetic_readiness"
    assert result["evidence"]["synthetic_good_ok"] is True
    assert result["evidence"]["scaffold_rejected"] is True


def test_notes_quality_gate_report_is_public_safe() -> None:
    report = render_report(build_notes_quality_gate())

    assert "RS3 Notes Quality Gate" in report
    assert "structured enough to drive capture" in report
    assert "source_body" not in report
    assert "api_key" not in report
    assert "token" not in report
