"""Synthetic local parser prototype for client-private workflows.

This module does not read files, run OCR, store source bodies, or create
embeddings. It only models the structured-facts output shape a future local
parser must satisfy before real private-file handling is introduced.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .case_intake import (
    ClientPrivateDeletionAttestation,
    ClientPrivateParserDryRunFixture,
    ClientPrivateUploadStoragePolicy,
    RedactedClientPrivateSummary,
    RoutingCandidate,
    ValidationIssue,
    _public_safe_issues,
    redact_local_private_case_for_public,
    route_redacted_client_private_summary,
    validate_client_private_deletion_attestation,
    validate_client_private_parser_dry_run_fixture,
    validate_client_private_upload_storage_policy,
)


@dataclass(frozen=True)
class LocalPrivateParserPrototypeInput:
    parser_run_id: str
    source_stub: str
    document_type: str
    expected_domain: str
    extracted_fields: dict[str, Any] = field(default_factory=dict)
    parser_mode: str = "structured_facts_only"
    allowed_output_level: str = "review_pack_summary"
    redaction_status: str = "reviewed_public_safe"
    reviewer_original_document_check: bool = True
    raw_file_present: bool = False
    parsed_body_present: bool = False
    ocr_text_present: bool = False
    embedding_present: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LocalPrivateParserPrototypeResult:
    parser_run_id: str
    fixture: ClientPrivateParserDryRunFixture
    redacted_summary: RedactedClientPrivateSummary
    route: RoutingCandidate
    deletion_attestation: ClientPrivateDeletionAttestation

    def to_dict(self) -> dict[str, Any]:
        return {
            "parser_run_id": self.parser_run_id,
            "fixture": self.fixture.to_dict(),
            "redacted_summary": self.redacted_summary.to_dict(),
            "route": self.route.to_dict(),
            "deletion_attestation": self.deletion_attestation.to_dict(),
        }


def validate_local_private_parser_prototype_input(
    parser_input: LocalPrivateParserPrototypeInput,
    policy: ClientPrivateUploadStoragePolicy,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    policy_issues = validate_client_private_upload_storage_policy(policy)
    issues.extend(ValidationIssue(f"policy.{issue.path}", issue.message) for issue in policy_issues)

    if not parser_input.parser_run_id:
        issues.append(ValidationIssue("parser_run_id", "parser_run_id is required"))
    if not parser_input.source_stub.startswith("local-private://dry-run/"):
        issues.append(ValidationIssue("source_stub", "source_stub must use local-private://dry-run/"))
    if parser_input.parser_mode != policy.parser_mode:
        issues.append(ValidationIssue("parser_mode", "parser mode must match upload/storage policy"))
    if parser_input.parser_mode != "structured_facts_only":
        issues.append(ValidationIssue("parser_mode", "prototype parser must use structured_facts_only"))
    if not parser_input.extracted_fields:
        issues.append(ValidationIssue("extracted_fields", "extracted_fields are required"))
    if parser_input.raw_file_present:
        issues.append(ValidationIssue("raw_file_present", "raw private file must not be present in prototype output"))
    if parser_input.parsed_body_present:
        issues.append(ValidationIssue("parsed_body_present", "parsed private body must not be present"))
    if parser_input.ocr_text_present:
        issues.append(ValidationIssue("ocr_text_present", "OCR text must not be present"))
    if parser_input.embedding_present:
        issues.append(ValidationIssue("embedding_present", "private embedding must not be present"))
    issues.extend(_public_safe_issues(parser_input.to_dict()))
    return issues


def run_local_private_parser_prototype(
    parser_input: LocalPrivateParserPrototypeInput,
    policy: ClientPrivateUploadStoragePolicy,
) -> LocalPrivateParserPrototypeResult:
    input_issues = validate_local_private_parser_prototype_input(parser_input, policy)
    if input_issues:
        joined = "; ".join(f"{issue.path}: {issue.message}" for issue in input_issues)
        raise ValueError(f"cannot run local parser prototype: {joined}")

    fixture = ClientPrivateParserDryRunFixture(
        fixture_id=parser_input.parser_run_id,
        parser_mode=parser_input.parser_mode,
        document_type=parser_input.document_type,
        source_stub=parser_input.source_stub,
        expected_domain=parser_input.expected_domain,
        structured_facts=dict(parser_input.extracted_fields),
        allowed_output_level=parser_input.allowed_output_level,
        redaction_status=parser_input.redaction_status,
        reviewer_original_document_check=parser_input.reviewer_original_document_check,
        deletion_attestation="synthetic parser prototype source deleted before report write",
    )
    fixture_issues = validate_client_private_parser_dry_run_fixture(fixture, policy)
    if fixture_issues:
        joined = "; ".join(f"{issue.path}: {issue.message}" for issue in fixture_issues)
        raise ValueError(f"local parser prototype produced invalid fixture: {joined}")

    redacted_summary = redact_local_private_case_for_public(fixture.to_local_private_case())
    route = route_redacted_client_private_summary(redacted_summary, domain_hint=fixture.expected_domain)
    deletion_attestation = ClientPrivateDeletionAttestation(
        attestation_id=f"{parser_input.parser_run_id}-deletion-attestation",
        fixture_id=fixture.fixture_id,
        source_stub=fixture.source_stub,
        deletion_status="deleted",
        deletion_mode=policy.deletion_mode,
        operator_check=(
            "operator verified gitignored local-only paths and checked the synthetic parser prototype source was "
            "deleted before report write"
        ),
        deleted_before_report_write=True,
        raw_file_present=False,
        parsed_body_present=False,
        ocr_text_present=False,
        embedding_present=False,
    )
    attestation_issues = validate_client_private_deletion_attestation(deletion_attestation, policy, fixture)
    if attestation_issues:
        joined = "; ".join(f"{issue.path}: {issue.message}" for issue in attestation_issues)
        raise ValueError(f"local parser prototype produced invalid deletion attestation: {joined}")

    return LocalPrivateParserPrototypeResult(
        parser_run_id=parser_input.parser_run_id,
        fixture=fixture,
        redacted_summary=redacted_summary,
        route=route,
        deletion_attestation=deletion_attestation,
    )


def render_local_private_parser_prototype_result(result: LocalPrivateParserPrototypeResult) -> str:
    lines = [
        f"# Local Parser Prototype Result - {result.parser_run_id}",
        "",
        f"- Route: {result.route.route}",
        f"- Route status: {result.route.status}",
        f"- Deletion status: {result.deletion_attestation.deletion_status}",
        f"- Deleted before report write: {result.deletion_attestation.deleted_before_report_write}",
        "",
        "## Structured Fact Keys",
        "",
    ]
    lines.extend(f"- {key}" for key in result.redacted_summary.structured_fact_keys)
    lines.extend([
        "",
        "## Boundary",
        "",
        "- This prototype does not read files, run OCR, store source bodies, or create embeddings.",
        "- It only converts synthetic parser-shaped input into redacted structured facts and a review-pack route candidate.",
        "- Real private file handling remains outside this repo until a separate local-only implementation gate exists.",
    ])
    return "\n".join(lines) + "\n"
