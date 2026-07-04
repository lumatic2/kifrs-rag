from __future__ import annotations

import pytest

from kifrs.feedback import CaseIntake
from kifrs.feedback.capture import (
    CapturedCorrection,
    FeedbackSessionNotes,
    build_feedback_capture_package,
    capture_notes_to_queue_records,
    validate_feedback_notes,
)


def _case() -> CaseIntake:
    return CaseIntake(
        case_id="anon-lease-poc-001",
        domain_hint="KIFRS1116",
        anonymized_title="Anonymized office lease",
        fact_pattern_summary="Sanitized office lease facts prepared as a structured PoC card.",
        structured_facts={
            "party": "lessee",
            "lease_term": "4 years",
            "payment_schedule": "annual arrears",
        },
        requested_outputs=["review_pack", "human_review_questions"],
    )


def _notes() -> FeedbackSessionNotes:
    return FeedbackSessionNotes(
        session_id="sample-session-001",
        reviewer_role="Accounting advisory reviewer",
        service_line="F-ACC",
        source="sample",
        scores={
            "workflow_fit": 4,
            "evidence_boundary_clarity": 4,
            "human_review_boundary": 5,
        },
        top_positive="Review pack order is close to a real workpaper.",
        top_risk="Lease term evidence can be under-specified.",
        required_input_additions=["lease term approval evidence"],
        review_question_additions=["Ask whether lease term approval evidence supports the stated term."],
        corrections=[
            CapturedCorrection(
                case_id="anon-lease-poc-001",
                issue="Lease term approval evidence should be requested explicitly",
                severity="medium",
                suggested_fix="Add a required reviewer question for lease term approval evidence.",
                disposition="eval_seed_candidate",
                affected_outputs=["human_review_questions", "review_pack"],
                missing_evidence=["lease term approval evidence"],
            )
        ],
        boundary_notes=["Sample notes only; not actual accountant review evidence."],
    )


def test_validate_feedback_notes_accepts_public_safe_sample() -> None:
    assert validate_feedback_notes(_notes()) == []


def test_validate_feedback_notes_rejects_protected_payload() -> None:
    notes = FeedbackSessionNotes(
        session_id="bad",
        reviewer_role="Reviewer",
        service_line="F-ACC",
        source="field_session",
        top_risk="Customer identifier 123-45-67890 appeared.",
        corrections=[],
    )

    issues = validate_feedback_notes(notes)

    assert any(issue.message == "possible customer identifier" for issue in issues)


def test_capture_notes_to_queue_records_converts_safe_corrections() -> None:
    records = capture_notes_to_queue_records(_notes(), {"anon-lease-poc-001": _case()})

    assert len(records) == 1
    assert records[0].case_id == "anon-lease-poc-001"
    assert records[0].route == "kifrs1116_review_pack"
    assert records[0].disposition == "candidate"


def test_capture_notes_to_queue_records_requires_case_mapping() -> None:
    with pytest.raises(ValueError, match="missing case"):
        capture_notes_to_queue_records(_notes(), {})


def test_build_feedback_capture_package_renders_reports() -> None:
    package = build_feedback_capture_package(_notes(), {"anon-lease-poc-001": _case()})

    assert "Field Feedback Notes" in package.notes_markdown
    assert "Queue records generated: 1" in package.capture_report_markdown
    assert "Field Feedback Capture Queue Report" in package.queue_report_markdown
