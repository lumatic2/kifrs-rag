"""Runtime close gate for client-private parser deletion and retention state."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from kifrs.feedback.case_intake import ClientPrivateDeletionAttestation
from kifrs.runtime.client_private_parser import RuntimeClientPrivateParserContract


@dataclass(frozen=True)
class RuntimeClientPrivateDeletionGate:
    parser_run_id: str
    deletion_status: str
    deletion_policy: str
    local_only: bool
    deleted_before_report_write: bool
    raw_file_present: bool
    parsed_body_present: bool
    ocr_text_present: bool
    embedding_present: bool
    operator_check: str
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def to_dict(self) -> dict[str, Any]:
        return {**asdict(self), "ok": self.ok}


def build_runtime_client_private_deletion_gate(
    contract: RuntimeClientPrivateParserContract,
    attestation: ClientPrivateDeletionAttestation,
) -> RuntimeClientPrivateDeletionGate:
    errors: list[str] = []
    if attestation.fixture_id != contract.parser_run_id:
        errors.append("attestation fixture_id must match parser_run_id")
    if attestation.deletion_status != "deleted":
        errors.append("deletion_status must be deleted")
    if attestation.deletion_mode != contract.deletion_policy:
        errors.append("deletion_mode must match parser contract deletion_policy")
    if contract.local_only is not True:
        errors.append("parser contract local_only must be true")
    if not attestation.deleted_before_report_write:
        errors.append("deleted_before_report_write must be true")
    if attestation.raw_file_present:
        errors.append("raw_file_present must be false")
    if attestation.parsed_body_present:
        errors.append("parsed_body_present must be false")
    if attestation.ocr_text_present:
        errors.append("ocr_text_present must be false")
    if attestation.embedding_present:
        errors.append("embedding_present must be false")
    if "gitignored" not in attestation.operator_check:
        errors.append("operator_check must mention gitignored local-only paths")
    if "deleted" not in attestation.operator_check.lower():
        errors.append("operator_check must state deletion was checked")
    return RuntimeClientPrivateDeletionGate(
        parser_run_id=contract.parser_run_id,
        deletion_status=attestation.deletion_status,
        deletion_policy=contract.deletion_policy,
        local_only=contract.local_only,
        deleted_before_report_write=attestation.deleted_before_report_write,
        raw_file_present=attestation.raw_file_present,
        parsed_body_present=attestation.parsed_body_present,
        ocr_text_present=attestation.ocr_text_present,
        embedding_present=attestation.embedding_present,
        operator_check=attestation.operator_check,
        errors=errors,
    )


def render_runtime_client_private_deletion_gate(gate: RuntimeClientPrivateDeletionGate) -> str:
    lines = [
        f"# Runtime Client-Private Deletion Gate - {gate.parser_run_id}",
        "",
        f"- ok: {gate.ok}",
        f"- deletion status: {gate.deletion_status}",
        f"- deletion policy: {gate.deletion_policy}",
        f"- local only: {gate.local_only}",
        f"- deleted before report write: {gate.deleted_before_report_write}",
        f"- raw file present: {gate.raw_file_present}",
        f"- parsed body present: {gate.parsed_body_present}",
        f"- OCR text present: {gate.ocr_text_present}",
        f"- embedding present: {gate.embedding_present}",
        "",
        "## Boundary",
        "",
        "- Client-private parser runtime cannot close unless deletion state is explicit.",
        "- The gate records deletion state only; it does not expose private content.",
    ]
    if gate.errors:
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in gate.errors)
    return "\n".join(lines) + "\n"


__all__ = [
    "RuntimeClientPrivateDeletionGate",
    "build_runtime_client_private_deletion_gate",
    "render_runtime_client_private_deletion_gate",
]
