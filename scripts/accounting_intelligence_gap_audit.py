from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs.ingestion.evidence import validate_evidence_manifest  # noqa: E402
from kifrs.ingestion.manifest import validate_manifest  # noqa: E402
from kifrs.workflows.source_aware_rebuild import build_default_rebuild_report  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-accounting-intelligence-gap-audit.md"

REQUIRED_REPORTS = {
    "rag_quality_refresh": ROOT / "docs" / "reports" / "2026-07-05-rag-quality-refresh-close-report.md",
    "authority_source_map": ROOT / "docs" / "reports" / "2026-07-05-authority-source-map-close-report.md",
    "multi_source_ingestion": ROOT / "docs" / "reports" / "2026-07-05-msi5-ingestion-gate-close-report.md",
    "multi_authority_runtime": ROOT / "docs" / "reports" / "2026-07-05-rt5-runtime-close-demo.md",
    "workflow_rebuild": ROOT / "docs" / "reports" / "2026-07-05-wr4-workflow-rebuild-close-report.md",
    "field_feedback_capture": ROOT / "docs" / "reports" / "2026-07-05-fc4-field-feedback-capture-close-report.md",
    "client_private_intake_readiness": ROOT / "docs" / "reports" / "2026-07-05-client-private-intake-readiness.md",
    "client_private_close_gate": ROOT / "docs" / "reports" / "2026-07-05-cp4-client-private-close-report.md",
    "live_external_source_validation": ROOT / "docs" / "reports" / "2026-07-05-lev1-live-external-source-validation.md",
    "opt_in_retriever_demo_validation": ROOT / "docs" / "reports" / "2026-07-05-odv1-opt-in-retriever-demo-validation.md",
    "opt_in_retriever_promotion_decision_gate": ROOT
    / "docs"
    / "reports"
    / "2026-07-05-orpd1-opt-in-retriever-promotion-decision-gate.md",
    "real_accountant_invite_dispatch_gate": ROOT
    / "docs"
    / "reports"
    / "real-accountant-session"
    / "2026-07-05-invite-dispatch-gate.md",
    "real_accountant_response_handling_gate": ROOT
    / "docs"
    / "reports"
    / "real-accountant-session"
    / "2026-07-05-response-handling-gate.md",
    "real_accountant_scheduled_session_gate": ROOT
    / "docs"
    / "reports"
    / "real-accountant-session"
    / "2026-07-05-scheduled-session-gate.md",
    "real_accountant_capture_readiness_gate": ROOT
    / "docs"
    / "reports"
    / "real-accountant-session"
    / "2026-07-05-rs3-capture-readiness-gate.md",
    "real_accountant_operator_execution_brief": ROOT
    / "docs"
    / "reports"
    / "real-accountant-session"
    / "2026-07-05-operator-execution-brief.md",
    "real_accountant_pre_send_final_gate": ROOT
    / "docs"
    / "reports"
    / "real-accountant-session"
    / "2026-07-05-pre-send-final-gate.md",
    "client_private_upload_storage_policy": ROOT / "docs" / "reports" / "2026-07-05-cpu1-client-private-upload-storage-policy.md",
    "private_parser_dry_run_fixture": ROOT / "docs" / "reports" / "2026-07-05-pdf1-private-parser-dry-run-fixture.md",
    "local_deletion_attestation_gate": ROOT / "docs" / "reports" / "2026-07-05-lda1-local-deletion-attestation-gate.md",
    "client_private_local_parser_close_gate": ROOT / "docs" / "reports" / "2026-07-05-cpl1-client-private-local-parser-close-gate.md",
    "local_parser_prototype_spike": ROOT / "docs" / "reports" / "2026-07-05-lpp1-local-parser-prototype-spike.md",
    "local_parser_prototype_close_gate": ROOT / "docs" / "reports" / "2026-07-05-lpc1-local-parser-prototype-close-gate.md",
    "local_parser_adapter_contract": ROOT / "docs" / "reports" / "2026-07-05-lpa1-local-parser-adapter-contract.md",
    "local_parser_adapter_dry_run_gate": ROOT / "docs" / "reports" / "2026-07-05-lpad1-local-parser-adapter-dry-run-gate.md",
    "local_parser_adapter_scaffold": ROOT / "docs" / "reports" / "2026-07-05-lpas1-local-parser-adapter-scaffold.md",
    "local_parser_operator_runbook": ROOT / "docs" / "reports" / "2026-07-05-lpor1-local-parser-operator-runbook.md",
    "local_parser_real_adapter_decision_gate": ROOT
    / "docs"
    / "reports"
    / "2026-07-05-lprd1-local-parser-real-adapter-decision-gate.md",
    "local_parser_real_adapter_implementation_plan": ROOT
    / "docs"
    / "reports"
    / "2026-07-05-local-parser-real-adapter-implementation-plan.md",
    "external_body_ingestion_decision_gate": ROOT
    / "docs"
    / "reports"
    / "2026-07-05-esbd1-external-source-body-ingestion-decision-gate.md",
    "external_body_policy_plan": ROOT
    / "docs"
    / "reports"
    / "2026-07-05-espp1-external-source-body-policy-plan.md",
    "external_body_authorization_gate": ROOT
    / "docs"
    / "reports"
    / "2026-07-05-esag1-external-source-body-authorization-gate.md",
    "external_synthetic_parser_chunker_dry_run": ROOT
    / "docs"
    / "reports"
    / "2026-07-05-essd1-external-source-synthetic-parser-chunker-dry-run.md",
    "external_synthetic_parser_chunker_close_gate": ROOT
    / "docs"
    / "reports"
    / "2026-07-05-essc1-external-source-synthetic-parser-chunker-close-gate.md",
    "external_connector_policy_record": ROOT
    / "docs"
    / "reports"
    / "2026-07-05-escp1-external-source-connector-policy-record.md",
    "external_connector_metadata_dry_run_gate": ROOT
    / "docs"
    / "reports"
    / "2026-07-05-esmd1-external-source-connector-metadata-dry-run-gate.md",
    "external_connector_metadata_close_gate": ROOT
    / "docs"
    / "reports"
    / "2026-07-05-esmc1-external-source-connector-metadata-close-gate.md",
    "external_connector_live_metadata_decision_gate": ROOT
    / "docs"
    / "reports"
    / "2026-07-05-eslm1-external-source-connector-live-metadata-decision-gate.md",
    "external_connector_live_metadata_probe_scaffold": ROOT
    / "docs"
    / "reports"
    / "2026-07-05-eslp1-external-source-connector-live-metadata-probe-scaffold.md",
    "external_connector_live_metadata_close_gate": ROOT
    / "docs"
    / "reports"
    / "2026-07-05-eslc1-external-source-connector-live-metadata-close-gate.md",
    "external_connector_live_metadata_report_fixture": ROOT
    / "docs"
    / "reports"
    / "2026-07-05-eslr1-external-source-connector-live-metadata-report-fixture.md",
    "external_connector_live_metadata_report_close_gate": ROOT
    / "docs"
    / "reports"
    / "2026-07-05-eslrc1-external-source-connector-live-metadata-report-close-gate.md",
    "external_connector_demo_index_bridge": ROOT
    / "docs"
    / "reports"
    / "2026-07-05-esdib1-external-source-connector-demo-index-bridge.md",
    "external_connector_demo_index_close_gate": ROOT
    / "docs"
    / "reports"
    / "2026-07-05-esdibc1-external-source-connector-demo-index-close-gate.md",
    "external_connector_lane_summary": ROOT
    / "docs"
    / "reports"
    / "2026-07-05-esls1-external-source-connector-lane-summary.md",
    "external_connector_lane_close_gate": ROOT
    / "docs"
    / "reports"
    / "2026-07-05-eslsc1-external-source-connector-lane-close-gate.md",
    "external_connector_post_close_demo_packet_note": ROOT
    / "docs"
    / "reports"
    / "2026-07-05-espdn1-external-source-connector-post-close-demo-packet-note.md",
}

REQUIRED_DEMO_OUTPUTS = {
    "demo_index": ROOT / "docs" / "reports" / "demo-poc" / "index.md",
    "evidence_boundary": ROOT / "docs" / "reports" / "demo-poc" / "evidence-boundary.md",
    "statement_candidates": ROOT / "docs" / "reports" / "demo-poc" / "statement-candidates.md",
    "field_feedback_index": ROOT / "docs" / "reports" / "field-feedback" / "INDEX.md",
    "real_session_packet": ROOT / "docs" / "reports" / "real-accountant-session" / "SESSION_PACKET.md",
}


@dataclass(frozen=True)
class GapAudit:
    ok: bool
    missing_reports: list[str]
    missing_demo_outputs: list[str]
    source_manifest_ok: bool
    evidence_manifest_ok: bool
    total_review_packs: int
    automated_packs: int
    human_review_packs: int
    automation_rate: float
    objective_ready_claim: str
    next_leaf: str
    remaining_gaps: list[str]
    errors: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_gap_audit() -> GapAudit:
    errors: list[str] = []

    missing_reports = [name for name, path in REQUIRED_REPORTS.items() if not path.exists()]
    if missing_reports:
        errors.append(f"missing reports: {missing_reports}")

    missing_demo_outputs = [name for name, path in REQUIRED_DEMO_OUTPUTS.items() if not path.exists()]
    if missing_demo_outputs:
        errors.append(f"missing demo outputs: {missing_demo_outputs}")

    source_result = validate_manifest()
    evidence_result = validate_evidence_manifest()
    if not source_result["ok"]:
        errors.extend(f"source_manifest: {error}" for error in source_result["errors"])
    if not evidence_result["ok"]:
        errors.extend(f"evidence_manifest: {error}" for error in evidence_result["errors"])

    rebuild = build_default_rebuild_report()
    automation_rate = rebuild.automated_packs / rebuild.total_packs if rebuild.total_packs else 0.0

    remaining_gaps = [
        "actual accountant session evidence is still external/user-owned; invite, response handling, scheduled-session, RS3 capture-readiness, operator execution brief, and pre-send final gate are ready but the reviewer invite has not been sent",
        "local parser real-adapter implementation plan is present, but actual evidence and explicit authorization are still required before real upload/OCR/parser/deletion automation",
        "external source connector metadata-only lane is closed and demo-noted, but source-body connector is still not implemented",
        "opt-in retriever promotion decision gate is present, but default retriever change remains deferred until actual accountant evidence and explicit authorization",
    ]

    return GapAudit(
        ok=not errors,
        missing_reports=missing_reports,
        missing_demo_outputs=missing_demo_outputs,
        source_manifest_ok=source_result["ok"],
        evidence_manifest_ok=evidence_result["ok"],
        total_review_packs=rebuild.total_packs,
        automated_packs=rebuild.automated_packs,
        human_review_packs=rebuild.human_review_packs,
        automation_rate=round(automation_rate, 4),
        objective_ready_claim=(
            "technical demo package is ready for review, but final PoC proof requires an actual accountant session"
        ),
        next_leaf="real-accountant-session RS2/RS3 evidence capture, then explicit authorization before default retriever change",
        remaining_gaps=remaining_gaps,
        errors=errors,
    )


def render_markdown(audit: GapAudit) -> str:
    lines = [
        "# Accounting Intelligence Gap Audit",
        "",
        "> Objective: 회계사 업무를 AI로 어디까지 자동화할 수 있는가를 실증하고, 회계법인 PoC 가능한 로컬 도구킷으로 만든다.",
        "> Scope: RAG Quality Refresh -> Authority Source Map -> Multi-Source Ingestion -> Multi-Authority Runtime -> Workflow Rebuild -> Field Feedback Capture.",
        "",
        "## 한 줄 결론",
        "",
        audit.objective_ready_claim,
        "",
        "## Evidence Coverage",
        "",
        "| Layer | Evidence | Status |",
        "|---|---|---|",
    ]
    for name, path in REQUIRED_REPORTS.items():
        status = "present" if name not in audit.missing_reports else "missing"
        lines.append(f"| {name} | `{_display_path(path)}` | {status} |")

    lines.extend([
        "",
        "## Demo Outputs",
        "",
        "| Output | Path | Status |",
        "|---|---|---|",
    ])
    for name, path in REQUIRED_DEMO_OUTPUTS.items():
        status = "present" if name not in audit.missing_demo_outputs else "missing"
        lines.append(f"| {name} | `{_display_path(path)}` | {status} |")

    lines.extend([
        "",
        "## Workflow Automation Snapshot",
        "",
        f"- Total source-aware F-ACC review packs: {audit.total_review_packs}",
        f"- Automated packs: {audit.automated_packs}",
        f"- Needs human review packs: {audit.human_review_packs}",
        f"- Automation rate: {audit.automation_rate:.2%}",
        "",
        "## Manifest Gates",
        "",
        f"- Source manifest ok: {audit.source_manifest_ok}",
        f"- Evidence manifest ok: {audit.evidence_manifest_ok}",
        "",
        "## Remaining Gaps",
        "",
    ])
    lines.extend(f"- {gap}" for gap in audit.remaining_gaps)
    lines.extend([
        "",
        "## Next Leaf",
        "",
        audit.next_leaf,
        "",
        "## Machine Result",
        "",
        "```json",
        json.dumps(audit.to_dict(), ensure_ascii=False, indent=2),
        "```",
    ])
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH) -> GapAudit:
    audit = build_gap_audit()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(audit), encoding="utf-8")
    return audit


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Accounting Intelligence Expansion evidence and remaining gaps.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true", help=f"Write {REPORT_PATH.relative_to(ROOT)}")
    args = parser.parse_args()

    audit = write_report() if args.write else build_gap_audit()
    if args.format == "json":
        print(json.dumps(audit.to_dict(), ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(audit))
    else:
        print(f"ok: {audit.ok}")
        print(f"reports_missing: {audit.missing_reports}")
        print(f"demo_outputs_missing: {audit.missing_demo_outputs}")
        print(f"source_manifest_ok: {audit.source_manifest_ok}")
        print(f"evidence_manifest_ok: {audit.evidence_manifest_ok}")
        print(f"review_packs: {audit.total_review_packs}")
        print(f"automated_packs: {audit.automated_packs}")
        print(f"human_review_packs: {audit.human_review_packs}")
        print(f"automation_rate: {audit.automation_rate:.2%}")
        print(f"next_leaf: {audit.next_leaf}")
        for error in audit.errors:
            print(f"- {error}")

    if not audit.ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
