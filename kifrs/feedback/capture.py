"""Public-safe field feedback notes capture.

The capture layer records session metadata and converts only sanitized
correction candidates into queue records. It is not a private workpaper store.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import re
from typing import Any, Mapping

from .case_intake import (
    CaseIntake,
    ReviewerCorrection,
    ValidationIssue,
    validate_reviewer_correction,
)
from .queue import FeedbackQueueRecord, make_queue_record, render_queue_report


FORBIDDEN_KEYS = {
    "body",
    "text",
    "content",
    "full_text",
    "source_body",
    "raw_contract",
    "contract_body",
    "customer_name",
    "client_name",
    "company_name",
    "business_registration_number",
    "resident_registration_number",
    "personal_id",
    "account_number",
    "raw_filing",
}

IDENTIFIER_PATTERNS = [
    re.compile(r"\b\d{3}-\d{2}-\d{5}\b"),
    re.compile(r"\b\d{6}-[1-4]\d{6}\b"),
]


@dataclass(frozen=True)
class CapturedCorrection:
    case_id: str
    issue: str
    severity: str
    suggested_fix: str
    disposition: str
    affected_outputs: list[str] = field(default_factory=list)
    missing_evidence: list[str] = field(default_factory=list)

    def to_reviewer_correction(self) -> ReviewerCorrection:
        return ReviewerCorrection(
            case_id=self.case_id,
            issue=self.issue,
            severity=self.severity,
            suggested_fix=self.suggested_fix,
            missing_evidence=list(self.missing_evidence),
            disposition=self.disposition,
            affected_outputs=list(self.affected_outputs),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class FeedbackSessionNotes:
    session_id: str
    reviewer_role: str
    service_line: str
    source: str
    scores: dict[str, int] = field(default_factory=dict)
    top_positive: str = ""
    top_risk: str = ""
    required_input_additions: list[str] = field(default_factory=list)
    review_question_additions: list[str] = field(default_factory=list)
    corrections: list[CapturedCorrection] = field(default_factory=list)
    boundary_notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class FeedbackCapturePackage:
    notes: FeedbackSessionNotes
    queue_records: list[FeedbackQueueRecord]
    notes_markdown: str
    capture_report_markdown: str
    queue_report_markdown: str


def validate_feedback_notes(notes: FeedbackSessionNotes) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if not notes.session_id:
        issues.append(ValidationIssue("session_id", "session_id is required"))
    if not notes.reviewer_role:
        issues.append(ValidationIssue("reviewer_role", "reviewer_role is required"))
    if not notes.service_line:
        issues.append(ValidationIssue("service_line", "service_line is required"))
    if notes.source not in {"sample", "field_session"}:
        issues.append(ValidationIssue("source", "source must be sample or field_session"))

    for key, value in notes.scores.items():
        if not 1 <= value <= 5:
            issues.append(ValidationIssue(f"scores.{key}", "score must be 1..5"))

    issues.extend(_public_safe_issues(notes.to_dict()))
    for index, correction in enumerate(notes.corrections):
        correction_issues = validate_reviewer_correction(correction.to_reviewer_correction())
        issues.extend(
            ValidationIssue(f"corrections[{index}].{issue.path}", issue.message)
            for issue in correction_issues
        )
    return issues


def capture_notes_to_queue_records(
    notes: FeedbackSessionNotes,
    cases: Mapping[str, CaseIntake],
    *,
    source: str = "field-feedback-capture",
) -> list[FeedbackQueueRecord]:
    issues = validate_feedback_notes(notes)
    if issues:
        raise ValueError("; ".join(f"{issue.path}: {issue.message}" for issue in issues))

    records: list[FeedbackQueueRecord] = []
    for correction in notes.corrections:
        if correction.case_id not in cases:
            raise ValueError(f"missing case for correction: {correction.case_id}")
        records.append(
            make_queue_record(
                cases[correction.case_id],
                correction.to_reviewer_correction(),
                source=source,
            )
        )
    return records


def build_feedback_capture_package(
    notes: FeedbackSessionNotes,
    cases: Mapping[str, CaseIntake],
    *,
    source: str = "field-feedback-capture",
) -> FeedbackCapturePackage:
    records = capture_notes_to_queue_records(notes, cases, source=source)
    return FeedbackCapturePackage(
        notes=notes,
        queue_records=records,
        notes_markdown=render_feedback_notes_markdown(notes),
        capture_report_markdown=render_capture_report(notes, records),
        queue_report_markdown=render_queue_report(records, title="Field Feedback Capture Queue Report"),
    )


def render_feedback_notes_markdown(notes: FeedbackSessionNotes) -> str:
    lines = [
        f"# Field Feedback Notes - {notes.session_id}",
        "",
        f"- Source: {notes.source}",
        f"- Reviewer role: {notes.reviewer_role}",
        f"- Service-line: {notes.service_line}",
        "",
        "## Scores",
        "",
    ]
    if notes.scores:
        lines.extend(f"- {key}: {value}" for key, value in sorted(notes.scores.items()))
    else:
        lines.append("- none")

    lines.extend([
        "",
        "## Top Positive",
        "",
        notes.top_positive or "none",
        "",
        "## Top Risk",
        "",
        notes.top_risk or "none",
        "",
        "## Required Input Additions",
        "",
    ])
    lines.extend(f"- {item}" for item in notes.required_input_additions) if notes.required_input_additions else lines.append("- none")

    lines.extend(["", "## Review Question Additions", ""])
    lines.extend(f"- {item}" for item in notes.review_question_additions) if notes.review_question_additions else lines.append("- none")

    lines.extend(["", "## Correction Candidates", ""])
    if notes.corrections:
        lines.extend(
            f"- {item.case_id}: {item.issue} ({item.disposition}, {item.severity})"
            for item in notes.corrections
        )
    else:
        lines.append("- none")

    lines.extend(["", "## Boundary", ""])
    if notes.boundary_notes:
        lines.extend(f"- {item}" for item in notes.boundary_notes)
    lines.extend([
        "- This note stores summarized feedback and correction candidates only.",
        "- It does not store raw contracts, customer identifiers, copied source bodies, private filings, parsed standards, embeddings, or workpaper payloads.",
    ])
    return "\n".join(lines) + "\n"


def render_capture_report(notes: FeedbackSessionNotes, records: list[FeedbackQueueRecord]) -> str:
    lines = [
        f"# Field Feedback Capture Report - {notes.session_id}",
        "",
        "> Public-safe capture report. This is not raw session transcript storage.",
        "",
        "## Summary",
        "",
        f"- Source: {notes.source}",
        f"- Reviewer role: {notes.reviewer_role}",
        f"- Service-line: {notes.service_line}",
        f"- Correction candidates: {len(notes.corrections)}",
        f"- Queue records generated: {len(records)}",
        "",
        "## Queue Records",
        "",
    ]
    if records:
        lines.extend(f"- {record.record_id}: {record.disposition} / {record.severity}" for record in records)
    else:
        lines.append("- none")

    lines.extend([
        "",
        "## Next Actions",
        "",
        "- Review generated queue records before merging into a canonical feedback queue.",
        "- Regenerate incorporation report after accepted queue records are appended.",
        "- Do not treat sample notes as actual accountant review evidence.",
        "",
        "## Boundary",
        "",
        "- Capture stores structured feedback only.",
        "- Protected payloads are rejected before queue conversion.",
    ])
    return "\n".join(lines) + "\n"


def _public_safe_issues(data: Any) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    def visit(value: Any, path: str) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                key_path = f"{path}.{key}" if path else str(key)
                if str(key) in FORBIDDEN_KEYS:
                    issues.append(ValidationIssue(key_path, "forbidden protected-data field"))
                visit(child, key_path)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                visit(child, f"{path}[{index}]")
        elif isinstance(value, str):
            if value in FORBIDDEN_KEYS:
                issues.append(ValidationIssue(path, "forbidden protected-data marker"))
            for pattern in IDENTIFIER_PATTERNS:
                if pattern.search(value):
                    issues.append(ValidationIssue(path, "possible customer identifier"))

    visit(data, "")
    return issues
