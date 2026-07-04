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
        "actual accountant session evidence is still external/user-owned",
        "client-private intake can route redacted structured facts, but local-only close gate is not implemented",
        "external sources are metadata/synthetic fixtures, not live KASB/FSS/DART body ingestion",
        "default retriever promotion remains deferred until real session demo validation",
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
        next_leaf="real-accountant-session RS2/RS3 evidence capture, or CP4 local-only close gate",
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
