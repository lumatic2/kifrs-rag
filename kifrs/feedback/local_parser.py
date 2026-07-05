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
    LOCAL_PRIVATE_DOCUMENT_TYPES,
    RedactedClientPrivateSummary,
    RoutingCandidate,
    SUPPORTED_DOMAINS,
    ValidationIssue,
    _public_safe_issues,
    redact_local_private_case_for_public,
    route_redacted_client_private_summary,
    validate_client_private_deletion_attestation,
    validate_client_private_parser_dry_run_fixture,
    validate_client_private_upload_storage_policy,
)


LOCAL_PARSER_ADAPTER_SOURCE_KINDS = {"synthetic_fixture"}
LOCAL_PARSER_ADAPTER_OUTPUT_MODES = {"structured_facts_only"}
LOCAL_PARSER_ADAPTER_HANDOFF_TARGETS = {"local_parser_prototype_input"}
LOCAL_PARSER_ADAPTER_FORBIDDEN_OUTPUTS = {
    "raw private file",
    "parsed private body",
    "OCR text",
    "private embedding",
    "source document excerpt",
}
LOCAL_PARSER_ADAPTER_REQUIRED_CHECKS = {
    "verify local-only paths are gitignored before receiving any file",
    "delete quarantined raw files before close",
    "record deletion attestation without source body text",
    "run public-safe gate before committing any derived artifact",
}


@dataclass(frozen=True)
class LocalPrivateParserAdapterContract:
    adapter_id: str
    source_kind: str
    output_mode: str
    handoff_target: str
    allowed_document_types: list[str] = field(default_factory=list)
    allowed_domains: list[str] = field(default_factory=list)
    required_extracted_fields: list[str] = field(default_factory=list)
    forbidden_outputs: list[str] = field(default_factory=list)
    required_operator_checks: list[str] = field(default_factory=list)
    reads_real_files: bool = False
    runs_ocr: bool = False
    stores_source_body: bool = False
    stores_private_embedding: bool = False
    deletion_automation: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


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


@dataclass(frozen=True)
class LocalPrivateParserAdapterDryRunCase:
    dry_run_id: str
    source_stub: str
    document_type: str
    expected_domain: str
    extracted_fields: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LocalPrivateParserAdapterDryRunGate:
    gate_id: str
    contract_id: str
    case_count: int
    passed_case_ids: list[str] = field(default_factory=list)
    failed_case_ids: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    prototype_results: list[LocalPrivateParserPrototypeResult] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.case_count > 0 and not self.errors and len(self.passed_case_ids) == self.case_count

    def to_dict(self) -> dict[str, Any]:
        return {
            "gate_id": self.gate_id,
            "contract_id": self.contract_id,
            "case_count": self.case_count,
            "passed_case_ids": list(self.passed_case_ids),
            "failed_case_ids": list(self.failed_case_ids),
            "errors": list(self.errors),
            "prototype_results": [result.to_dict() for result in self.prototype_results],
            "ok": self.ok,
        }


@dataclass(frozen=True)
class LocalPrivateParserAdapterScaffoldRequest:
    scaffold_run_id: str
    source_kind: str
    source_stub: str
    document_type: str
    expected_domain: str
    extracted_fields: dict[str, Any] = field(default_factory=dict)
    operator_ack: str = ""
    raw_file_path: str = ""
    ocr_enabled: bool = False
    parse_source_body: bool = False
    persist_source_body: bool = False
    create_private_embedding: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LocalPrivateParserAdapterScaffoldRun:
    scaffold_id: str
    contract_id: str
    request: LocalPrivateParserAdapterScaffoldRequest
    prototype_result: LocalPrivateParserPrototypeResult | None = None
    errors: list[str] = field(default_factory=list)
    real_adapter_implemented: bool = False

    @property
    def ok(self) -> bool:
        return not self.errors and self.prototype_result is not None and self.prototype_result.route.status == "candidate"

    def to_dict(self) -> dict[str, Any]:
        return {
            "scaffold_id": self.scaffold_id,
            "contract_id": self.contract_id,
            "request": self.request.to_dict(),
            "prototype_result": self.prototype_result.to_dict() if self.prototype_result is not None else {},
            "errors": list(self.errors),
            "real_adapter_implemented": self.real_adapter_implemented,
            "ok": self.ok,
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


def validate_local_private_parser_adapter_contract(
    contract: LocalPrivateParserAdapterContract,
    policy: ClientPrivateUploadStoragePolicy,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    policy_issues = validate_client_private_upload_storage_policy(policy)
    issues.extend(ValidationIssue(f"policy.{issue.path}", issue.message) for issue in policy_issues)

    if not contract.adapter_id:
        issues.append(ValidationIssue("adapter_id", "adapter_id is required"))
    if contract.source_kind not in LOCAL_PARSER_ADAPTER_SOURCE_KINDS:
        issues.append(ValidationIssue("source_kind", f"unsupported source_kind: {contract.source_kind}"))
    if contract.output_mode not in LOCAL_PARSER_ADAPTER_OUTPUT_MODES:
        issues.append(ValidationIssue("output_mode", f"unsupported output_mode: {contract.output_mode}"))
    if contract.output_mode != policy.parser_mode:
        issues.append(ValidationIssue("output_mode", "output mode must match upload/storage policy parser_mode"))
    if contract.handoff_target not in LOCAL_PARSER_ADAPTER_HANDOFF_TARGETS:
        issues.append(ValidationIssue("handoff_target", f"unsupported handoff_target: {contract.handoff_target}"))
    if not contract.allowed_document_types:
        issues.append(ValidationIssue("allowed_document_types", "at least one allowed document type is required"))
    for document_type in contract.allowed_document_types:
        if document_type not in LOCAL_PRIVATE_DOCUMENT_TYPES:
            issues.append(ValidationIssue("allowed_document_types", f"unsupported document_type: {document_type}"))
    if not contract.allowed_domains:
        issues.append(ValidationIssue("allowed_domains", "at least one allowed domain is required"))
    for domain in contract.allowed_domains:
        if domain not in SUPPORTED_DOMAINS:
            issues.append(ValidationIssue("allowed_domains", f"unsupported domain: {domain}"))
    if not contract.required_extracted_fields:
        issues.append(ValidationIssue("required_extracted_fields", "required_extracted_fields are required"))
    if "KIFRS1116" in contract.allowed_domains:
        required = {"party", "lease_term", "payment_schedule"}
        missing = sorted(required.difference(contract.required_extracted_fields))
        if missing:
            issues.append(
                ValidationIssue(
                    "required_extracted_fields",
                    f"KIFRS1116 adapter contract is missing required fields: {missing}",
                )
            )
    missing_forbidden = sorted(LOCAL_PARSER_ADAPTER_FORBIDDEN_OUTPUTS.difference(contract.forbidden_outputs))
    if missing_forbidden:
        issues.append(ValidationIssue("forbidden_outputs", f"missing forbidden outputs: {missing_forbidden}"))
    missing_checks = sorted(LOCAL_PARSER_ADAPTER_REQUIRED_CHECKS.difference(contract.required_operator_checks))
    if missing_checks:
        issues.append(ValidationIssue("required_operator_checks", f"missing required checks: {missing_checks}"))
    if contract.reads_real_files:
        issues.append(ValidationIssue("reads_real_files", "adapter contract must not read real files yet"))
    if contract.runs_ocr:
        issues.append(ValidationIssue("runs_ocr", "adapter contract must not run OCR yet"))
    if contract.stores_source_body:
        issues.append(ValidationIssue("stores_source_body", "adapter contract must not store source bodies"))
    if contract.stores_private_embedding:
        issues.append(ValidationIssue("stores_private_embedding", "adapter contract must not store private embeddings"))
    if contract.deletion_automation:
        issues.append(ValidationIssue("deletion_automation", "adapter contract must not claim deletion automation yet"))
    issues.extend(_public_safe_issues(contract.to_dict()))
    return issues


def validate_local_private_parser_adapter_scaffold_request(
    request: LocalPrivateParserAdapterScaffoldRequest,
    contract: LocalPrivateParserAdapterContract,
    policy: ClientPrivateUploadStoragePolicy,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    contract_issues = validate_local_private_parser_adapter_contract(contract, policy)
    issues.extend(ValidationIssue(f"contract.{issue.path}", issue.message) for issue in contract_issues)

    if not request.scaffold_run_id:
        issues.append(ValidationIssue("scaffold_run_id", "scaffold_run_id is required"))
    if request.source_kind != contract.source_kind:
        issues.append(ValidationIssue("source_kind", "source_kind must match adapter contract"))
    if request.source_kind != "synthetic_fixture":
        issues.append(ValidationIssue("source_kind", "scaffold only supports synthetic_fixture until real adapter gate exists"))
    if not request.source_stub.startswith("local-private://dry-run/"):
        issues.append(ValidationIssue("source_stub", "source_stub must use local-private://dry-run/"))
    if request.document_type not in contract.allowed_document_types:
        issues.append(ValidationIssue("document_type", f"document_type is outside adapter contract: {request.document_type}"))
    if request.expected_domain not in contract.allowed_domains:
        issues.append(ValidationIssue("expected_domain", f"expected_domain is outside adapter contract: {request.expected_domain}"))
    if not request.extracted_fields:
        issues.append(ValidationIssue("extracted_fields", "extracted_fields are required"))
    missing_fields = sorted(set(contract.required_extracted_fields).difference(request.extracted_fields))
    if missing_fields:
        issues.append(ValidationIssue("extracted_fields", f"missing adapter-required fields: {missing_fields}"))
    if request.operator_ack != "structured-facts-only-public-safe":
        issues.append(ValidationIssue("operator_ack", "operator_ack must be structured-facts-only-public-safe"))
    if request.raw_file_path:
        issues.append(ValidationIssue("raw_file_path", "scaffold must not receive raw file paths"))
    if request.ocr_enabled:
        issues.append(ValidationIssue("ocr_enabled", "scaffold must not enable OCR"))
    if request.parse_source_body:
        issues.append(ValidationIssue("parse_source_body", "scaffold must not parse source bodies"))
    if request.persist_source_body:
        issues.append(ValidationIssue("persist_source_body", "scaffold must not persist source bodies"))
    if request.create_private_embedding:
        issues.append(ValidationIssue("create_private_embedding", "scaffold must not create private embeddings"))
    issues.extend(_public_safe_issues(request.to_dict()))
    return issues


def run_local_private_parser_adapter_scaffold(
    scaffold_id: str,
    contract: LocalPrivateParserAdapterContract,
    policy: ClientPrivateUploadStoragePolicy,
    request: LocalPrivateParserAdapterScaffoldRequest,
) -> LocalPrivateParserAdapterScaffoldRun:
    errors: list[str] = []
    if not scaffold_id:
        errors.append("scaffold_id: scaffold_id is required")
    request_issues = validate_local_private_parser_adapter_scaffold_request(request, contract, policy)
    errors.extend(f"{issue.path}: {issue.message}" for issue in request_issues)
    if errors:
        return LocalPrivateParserAdapterScaffoldRun(
            scaffold_id=scaffold_id,
            contract_id=contract.adapter_id,
            request=request,
            errors=errors,
            real_adapter_implemented=False,
        )

    try:
        prototype_input = contract_to_local_private_parser_prototype_input(
            contract,
            policy,
            parser_run_id=request.scaffold_run_id,
            source_stub=request.source_stub,
            document_type=request.document_type,
            expected_domain=request.expected_domain,
            extracted_fields=request.extracted_fields,
        )
        prototype_result = run_local_private_parser_prototype(prototype_input, policy)
    except ValueError as exc:
        return LocalPrivateParserAdapterScaffoldRun(
            scaffold_id=scaffold_id,
            contract_id=contract.adapter_id,
            request=request,
            errors=[str(exc)],
            real_adapter_implemented=False,
        )

    return LocalPrivateParserAdapterScaffoldRun(
        scaffold_id=scaffold_id,
        contract_id=contract.adapter_id,
        request=request,
        prototype_result=prototype_result,
        errors=[],
        real_adapter_implemented=False,
    )


def validate_local_private_parser_adapter_dry_run_case(
    dry_run_case: LocalPrivateParserAdapterDryRunCase,
    contract: LocalPrivateParserAdapterContract,
    policy: ClientPrivateUploadStoragePolicy,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    contract_issues = validate_local_private_parser_adapter_contract(contract, policy)
    issues.extend(ValidationIssue(f"contract.{issue.path}", issue.message) for issue in contract_issues)

    if not dry_run_case.dry_run_id:
        issues.append(ValidationIssue("dry_run_id", "dry_run_id is required"))
    if not dry_run_case.source_stub.startswith("local-private://dry-run/"):
        issues.append(ValidationIssue("source_stub", "source_stub must use local-private://dry-run/"))
    if dry_run_case.document_type not in contract.allowed_document_types:
        issues.append(ValidationIssue("document_type", f"document_type is outside adapter contract: {dry_run_case.document_type}"))
    if dry_run_case.expected_domain not in contract.allowed_domains:
        issues.append(ValidationIssue("expected_domain", f"expected_domain is outside adapter contract: {dry_run_case.expected_domain}"))
    if not dry_run_case.extracted_fields:
        issues.append(ValidationIssue("extracted_fields", "extracted_fields are required"))
    missing_fields = sorted(set(contract.required_extracted_fields).difference(dry_run_case.extracted_fields))
    if missing_fields:
        issues.append(ValidationIssue("extracted_fields", f"missing adapter-required fields: {missing_fields}"))
    issues.extend(_public_safe_issues(dry_run_case.to_dict()))
    return issues


def run_local_private_parser_adapter_dry_run_gate(
    gate_id: str,
    contract: LocalPrivateParserAdapterContract,
    policy: ClientPrivateUploadStoragePolicy,
    dry_run_cases: list[LocalPrivateParserAdapterDryRunCase],
) -> LocalPrivateParserAdapterDryRunGate:
    errors: list[str] = []
    passed_case_ids: list[str] = []
    failed_case_ids: list[str] = []
    prototype_results: list[LocalPrivateParserPrototypeResult] = []

    if not gate_id:
        errors.append("gate_id: gate_id is required")
    if not dry_run_cases:
        errors.append("dry_run_cases: at least one dry-run case is required")

    for dry_run_case in dry_run_cases:
        case_issues = validate_local_private_parser_adapter_dry_run_case(dry_run_case, contract, policy)
        if case_issues:
            failed_case_ids.append(dry_run_case.dry_run_id)
            errors.extend(f"{dry_run_case.dry_run_id}.{issue.path}: {issue.message}" for issue in case_issues)
            continue
        try:
            prototype_input = contract_to_local_private_parser_prototype_input(
                contract,
                policy,
                parser_run_id=dry_run_case.dry_run_id,
                source_stub=dry_run_case.source_stub,
                document_type=dry_run_case.document_type,
                expected_domain=dry_run_case.expected_domain,
                extracted_fields=dry_run_case.extracted_fields,
            )
            prototype_result = run_local_private_parser_prototype(prototype_input, policy)
        except ValueError as exc:
            failed_case_ids.append(dry_run_case.dry_run_id)
            errors.append(f"{dry_run_case.dry_run_id}: {exc}")
            continue

        if prototype_result.route.status != "candidate":
            failed_case_ids.append(dry_run_case.dry_run_id)
            errors.append(
                f"{dry_run_case.dry_run_id}.route: expected candidate, got {prototype_result.route.status}"
            )
            continue

        passed_case_ids.append(dry_run_case.dry_run_id)
        prototype_results.append(prototype_result)

    return LocalPrivateParserAdapterDryRunGate(
        gate_id=gate_id,
        contract_id=contract.adapter_id,
        case_count=len(dry_run_cases),
        passed_case_ids=passed_case_ids,
        failed_case_ids=failed_case_ids,
        errors=errors,
        prototype_results=prototype_results,
    )


def contract_to_local_private_parser_prototype_input(
    contract: LocalPrivateParserAdapterContract,
    policy: ClientPrivateUploadStoragePolicy,
    *,
    parser_run_id: str,
    source_stub: str,
    document_type: str,
    expected_domain: str,
    extracted_fields: dict[str, Any],
) -> LocalPrivateParserPrototypeInput:
    contract_issues = validate_local_private_parser_adapter_contract(contract, policy)
    if contract_issues:
        joined = "; ".join(f"{issue.path}: {issue.message}" for issue in contract_issues)
        raise ValueError(f"cannot hand off invalid local parser adapter contract: {joined}")
    if document_type not in contract.allowed_document_types:
        raise ValueError(f"document_type is outside adapter contract: {document_type}")
    if expected_domain not in contract.allowed_domains:
        raise ValueError(f"expected_domain is outside adapter contract: {expected_domain}")
    missing_fields = sorted(set(contract.required_extracted_fields).difference(extracted_fields))
    if missing_fields:
        raise ValueError(f"extracted_fields missing adapter-required fields: {missing_fields}")

    return LocalPrivateParserPrototypeInput(
        parser_run_id=parser_run_id,
        source_stub=source_stub,
        document_type=document_type,
        expected_domain=expected_domain,
        extracted_fields=dict(extracted_fields),
        parser_mode=contract.output_mode,
        allowed_output_level="review_pack_summary",
        redaction_status="reviewed_public_safe",
        reviewer_original_document_check=True,
        raw_file_present=False,
        parsed_body_present=False,
        ocr_text_present=False,
        embedding_present=False,
    )


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


def render_local_private_parser_adapter_scaffold_run(run: LocalPrivateParserAdapterScaffoldRun) -> str:
    lines = [
        f"# Local Parser Adapter Scaffold Run - {run.scaffold_id}",
        "",
        f"- Contract: {run.contract_id}",
        f"- OK: {run.ok}",
        f"- Real adapter implemented: {run.real_adapter_implemented}",
        f"- Source kind: {run.request.source_kind}",
        f"- Source stub: {run.request.source_stub}",
        "",
        "## Route",
        "",
    ]
    if run.prototype_result is not None:
        lines.extend([
            f"- Route: {run.prototype_result.route.route}",
            f"- Route status: {run.prototype_result.route.status}",
            f"- Deletion status: {run.prototype_result.deletion_attestation.deletion_status}",
        ])
    else:
        lines.append("- prototype route not produced")
    lines.extend([
        "",
        "## Boundary",
        "",
        "- This scaffold accepts structured facts only.",
        "- It refuses raw file paths, OCR, source-body parsing, source-body persistence, and private embeddings.",
        "- It is an adapter entrypoint scaffold, not a real private-file parser.",
    ])
    if run.errors:
        lines.extend([
            "",
            "## Errors",
            "",
        ])
        lines.extend(f"- {error}" for error in run.errors)
    return "\n".join(lines) + "\n"


def render_local_private_parser_adapter_dry_run_gate(gate: LocalPrivateParserAdapterDryRunGate) -> str:
    lines = [
        f"# Local Parser Adapter Dry-Run Gate - {gate.gate_id}",
        "",
        f"- Contract: {gate.contract_id}",
        f"- OK: {gate.ok}",
        f"- Case count: {gate.case_count}",
        f"- Passed: {len(gate.passed_case_ids)}",
        f"- Failed: {len(gate.failed_case_ids)}",
        "",
        "## Passed Cases",
        "",
    ]
    lines.extend(f"- {case_id}" for case_id in gate.passed_case_ids)
    lines.extend([
        "",
        "## Failed Cases",
        "",
    ])
    lines.extend(f"- {case_id}" for case_id in gate.failed_case_ids)
    lines.extend([
        "",
        "## Routes",
        "",
    ])
    lines.extend(
        f"- {result.parser_run_id}: {result.route.route} ({result.route.status})"
        for result in gate.prototype_results
    )
    lines.extend([
        "",
        "## Boundary",
        "",
        "- This gate runs synthetic dry-run cases only.",
        "- It does not read files, run OCR, store source bodies, create embeddings, or automate deletion.",
        "- A real local-only parser adapter still needs a separate implementation scaffold and operator gate.",
    ])
    if gate.errors:
        lines.extend([
            "",
            "## Errors",
            "",
        ])
        lines.extend(f"- {error}" for error in gate.errors)
    return "\n".join(lines) + "\n"


def render_local_private_parser_adapter_contract(
    contract: LocalPrivateParserAdapterContract,
    policy: ClientPrivateUploadStoragePolicy,
) -> str:
    issues = validate_local_private_parser_adapter_contract(contract, policy)
    lines = [
        f"# Local Parser Adapter Contract - {contract.adapter_id}",
        "",
        f"- Source kind: {contract.source_kind}",
        f"- Output mode: {contract.output_mode}",
        f"- Handoff target: {contract.handoff_target}",
        f"- Allowed document types: {', '.join(contract.allowed_document_types)}",
        f"- Allowed domains: {', '.join(contract.allowed_domains)}",
        f"- Validation issues: {len(issues)}",
        "",
        "## Required Extracted Fields",
        "",
    ]
    lines.extend(f"- {field_name}" for field_name in contract.required_extracted_fields)
    lines.extend([
        "",
        "## Forbidden Public Outputs",
        "",
    ])
    lines.extend(f"- {output}" for output in contract.forbidden_outputs)
    lines.extend([
        "",
        "## Required Operator Checks",
        "",
    ])
    lines.extend(f"- {check}" for check in contract.required_operator_checks)
    lines.extend([
        "",
        "## Boundary",
        "",
        "- This contract does not read files, run OCR, store source bodies, create embeddings, or automate deletion.",
        "- It only defines the public-safe adapter output shape before a real local-only parser exists.",
        "- The handoff target is LocalPrivateParserPrototypeInput for review-pack routing validation.",
    ])
    if issues:
        lines.extend([
            "",
            "## Validation Issues",
            "",
        ])
        lines.extend(f"- {issue.path}: {issue.message}" for issue in issues)
    return "\n".join(lines) + "\n"
