"""Public-safe intake and correction contracts for real-case feedback.

The objects in this module are intentionally metadata/structure only. They do
not store raw contracts, customer identifiers, copied source bodies, private
filings, parsed standards, embeddings, or workpaper payloads.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import re
from typing import Any


SUPPORTED_DOMAINS = {"KIFRS1109", "KIFRS1115", "KIFRS1116"}
OUT_OF_SCOPE_DOMAINS = {"TAX", "DEAL", "VALUATION", "KSX", "KSox", "KSOX", "AUDIT_ONLY"}
ALLOWED_OUTPUTS = {
    "review_pack",
    "journal_entry_draft",
    "disclosure_questions",
    "statement_candidate",
    "evidence_boundary",
    "human_review_questions",
}
LOCAL_PRIVATE_DOCUMENT_TYPES = {
    "contract",
    "trial_balance",
    "accounting_policy",
    "workpaper",
    "management_memo",
    "filing_support",
}
LOCAL_PRIVATE_REDACTION_STATUSES = {
    "not_started",
    "redacted",
    "reviewed_public_safe",
}
LOCAL_PRIVATE_ALLOWED_OUTPUT_LEVELS = {
    "schema_only",
    "structured_facts_only",
    "review_pack_summary",
}
CORRECTION_DISPOSITIONS = {"eval_seed_candidate", "backlog_candidate", "no_action"}
CORRECTION_SEVERITIES = {"low", "medium", "high", "blocker"}

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
    re.compile(r"\b\d{3}-\d{2}-\d{5}\b"),  # Korean business registration number.
    re.compile(r"\b\d{6}-[1-4]\d{6}\b"),  # Korean resident registration number.
]


@dataclass(frozen=True)
class ValidationIssue:
    path: str
    message: str


@dataclass(frozen=True)
class CaseIntake:
    case_id: str
    domain_hint: str
    anonymized_title: str
    fact_pattern_summary: str
    structured_facts: dict[str, Any] = field(default_factory=dict)
    requested_outputs: list[str] = field(default_factory=list)
    source_boundaries: list[str] = field(default_factory=list)
    reviewer_questions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LocalPrivateCaseIntake:
    case_id: str
    source_locator: str
    document_type: str
    redaction_status: str
    allowed_output_level: str
    structured_facts: dict[str, Any] = field(default_factory=dict)
    reviewer_original_document_check: bool = False
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ReviewerCorrection:
    case_id: str
    issue: str
    severity: str
    suggested_fix: str
    missing_evidence: list[str] = field(default_factory=list)
    disposition: str = "backlog_candidate"
    affected_outputs: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RoutingCandidate:
    case_id: str
    domain: str
    route: str
    status: str
    reason: str
    missing_facts: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def validate_case_intake(case: CaseIntake) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if not case.case_id:
        issues.append(ValidationIssue("case_id", "case_id is required"))
    if case.domain_hint not in SUPPORTED_DOMAINS and case.domain_hint.upper() not in OUT_OF_SCOPE_DOMAINS:
        issues.append(ValidationIssue("domain_hint", f"unsupported domain_hint: {case.domain_hint}"))
    if not case.anonymized_title:
        issues.append(ValidationIssue("anonymized_title", "anonymized_title is required"))
    if not case.fact_pattern_summary:
        issues.append(ValidationIssue("fact_pattern_summary", "fact_pattern_summary is required"))
    if len(case.fact_pattern_summary) > 600:
        issues.append(ValidationIssue("fact_pattern_summary", "summary must stay short and sanitized"))

    for output in case.requested_outputs:
        if output not in ALLOWED_OUTPUTS:
            issues.append(ValidationIssue("requested_outputs", f"unsupported requested output: {output}"))

    issues.extend(_public_safe_issues(case.to_dict()))
    return issues


def validate_local_private_case_intake(case: LocalPrivateCaseIntake) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if not case.case_id:
        issues.append(ValidationIssue("case_id", "case_id is required"))
    if not case.source_locator:
        issues.append(ValidationIssue("source_locator", "source_locator is required"))
    if case.document_type not in LOCAL_PRIVATE_DOCUMENT_TYPES:
        issues.append(ValidationIssue("document_type", f"unsupported document_type: {case.document_type}"))
    if case.redaction_status not in LOCAL_PRIVATE_REDACTION_STATUSES:
        issues.append(ValidationIssue("redaction_status", f"unsupported redaction_status: {case.redaction_status}"))
    if case.allowed_output_level not in LOCAL_PRIVATE_ALLOWED_OUTPUT_LEVELS:
        issues.append(
            ValidationIssue("allowed_output_level", f"unsupported allowed_output_level: {case.allowed_output_level}")
        )
    if not case.reviewer_original_document_check:
        issues.append(
            ValidationIssue(
                "reviewer_original_document_check",
                "reviewer must check original documents outside this repo",
            )
        )
    if case.redaction_status != "reviewed_public_safe" and case.allowed_output_level == "review_pack_summary":
        issues.append(
            ValidationIssue(
                "allowed_output_level",
                "review_pack_summary requires redaction_status reviewed_public_safe",
            )
        )
    issues.extend(_public_safe_issues(case.to_dict()))
    return issues


def validate_reviewer_correction(correction: ReviewerCorrection) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if not correction.case_id:
        issues.append(ValidationIssue("case_id", "case_id is required"))
    if not correction.issue:
        issues.append(ValidationIssue("issue", "issue is required"))
    if correction.severity not in CORRECTION_SEVERITIES:
        issues.append(ValidationIssue("severity", f"unsupported severity: {correction.severity}"))
    if correction.disposition not in CORRECTION_DISPOSITIONS:
        issues.append(ValidationIssue("disposition", f"unsupported disposition: {correction.disposition}"))
    if not correction.suggested_fix:
        issues.append(ValidationIssue("suggested_fix", "suggested_fix is required"))

    for output in correction.affected_outputs:
        if output not in ALLOWED_OUTPUTS:
            issues.append(ValidationIssue("affected_outputs", f"unsupported affected output: {output}"))

    issues.extend(_public_safe_issues(correction.to_dict()))
    return issues


def route_case(case: CaseIntake) -> RoutingCandidate:
    validation = validate_case_intake(case)
    if validation:
        return RoutingCandidate(
            case_id=case.case_id,
            domain=case.domain_hint,
            route="validation_failed",
            status="blocked",
            reason="; ".join(f"{item.path}: {item.message}" for item in validation),
        )

    domain = case.domain_hint.upper()
    if domain in OUT_OF_SCOPE_DOMAINS:
        return RoutingCandidate(
            case_id=case.case_id,
            domain=domain,
            route="out_of_scope",
            status="unsupported",
            reason="domain belongs outside kifrs-rag automation boundary or requires private/internal materials",
        )

    required = _required_fact_keys(domain)
    missing = [key for key in required if key not in case.structured_facts]
    if missing:
        return RoutingCandidate(
            case_id=case.case_id,
            domain=domain,
            route=f"{domain.lower()}_review_pack",
            status="needs_more_facts",
            reason="required structured facts are missing",
            missing_facts=missing,
        )

    return RoutingCandidate(
        case_id=case.case_id,
        domain=domain,
        route=f"{domain.lower()}_review_pack",
        status="candidate",
        reason="minimum structured facts are present for a review-pack draft candidate",
    )


def case_to_eval_seed_candidate(case: CaseIntake, correction: ReviewerCorrection) -> dict[str, Any]:
    case_issues = validate_case_intake(case)
    correction_issues = validate_reviewer_correction(correction)
    if case_issues or correction_issues:
        joined = "; ".join(
            [f"case.{issue.path}: {issue.message}" for issue in case_issues]
            + [f"correction.{issue.path}: {issue.message}" for issue in correction_issues]
        )
        raise ValueError(f"cannot create eval seed candidate: {joined}")
    if case.case_id != correction.case_id:
        raise ValueError("case and correction must use the same case_id")

    route = route_case(case)
    return {
        "case_id": case.case_id,
        "domain": case.domain_hint.upper(),
        "route": route.route,
        "status": "candidate" if correction.disposition == "eval_seed_candidate" else correction.disposition,
        "issue": correction.issue,
        "severity": correction.severity,
        "expected_improvement": correction.suggested_fix,
        "missing_evidence": list(correction.missing_evidence),
    }


def render_feedback_summary_markdown(
    case: CaseIntake,
    correction: ReviewerCorrection | None = None,
) -> str:
    route = route_case(case)
    lines = [
        f"# Real Case Feedback Summary - {case.case_id}",
        "",
        f"- Domain: {case.domain_hint.upper()}",
        f"- Route: {route.route}",
        f"- Route status: {route.status}",
        f"- Route reason: {route.reason}",
        "",
        "## Sanitized Case",
        "",
        f"- Title: {case.anonymized_title}",
        f"- Summary: {case.fact_pattern_summary}",
        f"- Requested outputs: {', '.join(case.requested_outputs) if case.requested_outputs else 'none'}",
        "",
        "## Source Boundary",
    ]
    if case.source_boundaries:
        lines.extend(f"- {item}" for item in case.source_boundaries)
    else:
        lines.append("- No raw source body is stored.")

    if route.missing_facts:
        lines.extend(["", "## Missing Structured Facts", ""])
        lines.extend(f"- {item}" for item in route.missing_facts)

    if correction is not None:
        lines.extend([
            "",
            "## Reviewer Correction",
            "",
            f"- Issue: {correction.issue}",
            f"- Severity: {correction.severity}",
            f"- Disposition: {correction.disposition}",
            f"- Suggested fix: {correction.suggested_fix}",
        ])
        if correction.missing_evidence:
            lines.append("- Missing evidence:")
            lines.extend(f"  - {item}" for item in correction.missing_evidence)

    lines.extend([
        "",
        "## Boundary",
        "",
        "- This summary stores structured facts and reviewer corrections only.",
        "- It does not store raw contracts, customer identifiers, copied source bodies, private filings, parsed standards, embeddings, or workpaper payloads.",
    ])
    return "\n".join(lines) + "\n"


def render_local_private_intake_card(case: LocalPrivateCaseIntake) -> str:
    issues = validate_local_private_case_intake(case)
    lines = [
        f"# Local-Only Client-Private Intake Card - {case.case_id}",
        "",
        f"- Source locator: {case.source_locator}",
        f"- Document type: {case.document_type}",
        f"- Redaction status: {case.redaction_status}",
        f"- Allowed output level: {case.allowed_output_level}",
        f"- Reviewer original-document check: {case.reviewer_original_document_check}",
        "",
        "## Structured Facts",
        "",
    ]
    if case.structured_facts:
        lines.extend(["| Field | Value |", "|---|---|"])
        for key, value in sorted(case.structured_facts.items()):
            lines.append(f"| {key} | {value} |")
    else:
        lines.append("- none")

    if case.notes:
        lines.extend(["", "## Notes", ""])
        lines.extend(f"- {note}" for note in case.notes)

    if issues:
        lines.extend(["", "## Validation Issues", ""])
        lines.extend(f"- {issue.path}: {issue.message}" for issue in issues)

    lines.extend([
        "",
        "## Boundary",
        "",
        "- This card is a local-only control record.",
        "- It does not store raw contracts, customer identifiers, copied source bodies, private filings, parsed standards, embeddings, or workpaper payloads.",
        "- The reviewer checks original documents outside this repo.",
    ])
    return "\n".join(lines) + "\n"


def _required_fact_keys(domain: str) -> list[str]:
    if domain == "KIFRS1109":
        return ["instrument_type", "business_model", "cash_flow_terms"]
    if domain == "KIFRS1115":
        return ["scenario_type", "contract_price", "payment_terms"]
    if domain == "KIFRS1116":
        return ["party", "lease_term", "payment_schedule"]
    return []


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
