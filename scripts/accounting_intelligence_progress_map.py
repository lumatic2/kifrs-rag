from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.accounting_intelligence_gap_audit import build_gap_audit  # noqa: E402
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-accounting-intelligence-progress-map.md"


def build_progress_map() -> dict[str, Any]:
    gap = build_gap_audit()
    completed_horizons = [
        {
            "id": "firm-service-map",
            "result": "Mapped accounting firm teams and selected F-ACC/accounting advisory as the first product lane.",
            "evidence": "docs/horizons/firm-service-map.md",
        },
        {
            "id": "F-ACC sequence",
            "result": "Turned the firm-service map into review-pack workflow sequence candidates.",
            "evidence": "BACKLOG.md",
        },
        {
            "id": "rag-quality-refresh",
            "result": "Built an opt-in repair retriever stack that reaches 50-item recall@20 1.000 without default promotion.",
            "evidence": "docs/reports/2026-07-05-rag-quality-refresh-close-report.md",
        },
        {
            "id": "authority-source-map",
            "result": "Separated K-IFRS, regulator, disclosure, law, and private-client source lanes with storage boundaries.",
            "evidence": "docs/reports/2026-07-05-authority-source-map-close-report.md",
        },
        {
            "id": "client-private intake/local parser",
            "result": "Defined local-only private intake, redaction, parser dry-run, deletion attestation, and adapter plan boundaries.",
            "evidence": "docs/reports/2026-07-05-local-parser-real-adapter-implementation-plan.md",
        },
        {
            "id": "multi-authority-runtime-hardening",
            "result": "Connected K-IFRS primary, supporting, legal, fact, and client-private placeholder evidence across runtime, review packs, statement draft, analytics, and close gate.",
            "evidence": "docs/reports/2026-07-05-multi-authority-runtime-hardening-close-report.md",
        },
        {
            "id": "client-private-parser-runtime",
            "result": "Added structured-facts-only private parser runtime contract, client_private_fact adapter, deletion close gate, and close demo without public private payload.",
            "evidence": "docs/reports/2026-07-05-client-private-parser-runtime-close-report.md",
        },
        {
            "id": "real-local-parser-prototype",
            "result": "Closed a local-safe fixture parser path with asset inventory, fixture adapter, deletion simulation, leak tests, and close gate.",
            "evidence": "docs/reports/2026-07-05-real-local-parser-prototype-close-report.md",
        },
        {
            "id": "source-body-ingestion-controlled-lane",
            "result": "Closed one synthetic-only controlled non-IFRS interpretive lane with source selection, policy, chunking, retrieval, and public-safe close gate.",
            "evidence": "docs/reports/2026-07-05-source-body-ingestion-controlled-lane-close-report.md",
        },
        {
            "id": "workflow-coverage-expansion",
            "result": "Expanded firm-service coverage with a 1037 provisions decision-prep workflow ranking, contract, adapter, metric update, and close gate.",
            "evidence": "docs/reports/2026-07-05-workflow-coverage-expansion-close-report.md",
        },
        {
            "id": "runtime-retriever-promotion-gate",
            "result": "Closed retriever default promotion as defer with evidence inventory, regression/latency gate, rollback policy, operator dry-run, and close report.",
            "evidence": "docs/reports/2026-07-05-runtime-retriever-promotion-gate-close-report.md",
        },
        {
            "id": "operator-experience-hardening",
            "result": "Closed operator UX with command inventory, run doctor, report manifest, recovery playbook, and close gate.",
            "evidence": "docs/reports/2026-07-05-operator-experience-hardening-close-report.md",
        },
    ]
    current_horizon = {
        "id": "workflow-coverage-depth-expansion",
        "status": "active",
        "goal": "Deepen automation coverage against the firm-service map with broader workflow sampling and public-safe decision-prep evidence.",
        "milestones": [
            {"id": "WCD1", "name": "service-line coverage rerank", "status": "completed"},
            {"id": "WCD2", "name": "workflow sample contract pack", "status": "completed"},
            {"id": "WCD3", "name": "minimal adapter expansion", "status": "completed"},
            {"id": "WCD4", "name": "coverage depth metric update", "status": "active"},
            {"id": "WCD5", "name": "close and demo rehearsal handoff", "status": "pending"},
        ],
    }
    decisions = [
        {
            "id": "select_next_post_demo_horizon",
            "status": "closed_by_objective_gap_queue",
            "decide": "Objective gaps are grouped into a new horizon queue; run RAG quality fresh validation first.",
            "blocker": "none",
            "command": "python scripts\\objective_gap_horizon_candidates.py --format text",
        },
        {
            "id": "run_rag_quality_fresh_validation",
            "status": "closed_defer",
            "decide": "RAG quality fresh validation closed as defer; default retriever remains unchanged.",
            "blocker": "none",
            "command": "python scripts\\rag_quality_fresh_validation_close_gate.py --format text",
        },
        {
            "id": "run_private_parser_realism_hardening",
            "status": "closed_realism_contract_ready",
            "decide": "Private parser realism closed with authorization-safe adapter proof, fixture adapter contract, deletion rehearsal, leak gate, and source connector handoff.",
            "blocker": "none",
            "command": "python scripts\\private_parser_realism_close_gate.py --format text",
        },
        {
            "id": "run_external_connector_body_expansion",
            "status": "closed_connector_body_lane_ready",
            "decide": "External source-body connector expansion closed with selected lane, fixture contract, retrieval dry run, leak gate, and workflow coverage handoff.",
            "blocker": "none",
            "command": "python scripts\\external_source_connector_body_close_gate.py --format text",
        },
        {
            "id": "run_workflow_coverage_depth_expansion",
            "status": "active_horizon",
            "decide": "WCD1 selected audit_disclosure_tie_out, WCD2 defined its contract, and WCD3 added the minimal adapter; continue with coverage depth metric update.",
            "blocker": "none",
            "command": "python scripts\\workflow_coverage_depth_metric.py --format text --write",
        },
        {
            "id": "approve_default_retriever_promotion",
            "status": "deferred_until_eval_evidence_and_authorization",
            "decide": "Promote the opt-in repair retriever to default only after stronger evaluation evidence and explicit authorization.",
            "blocker": "stronger evaluation evidence and explicit authorization are missing",
            "command": "python scripts\\default_retriever_guard.py --format text",
        },
    ]
    return {
        "title": "Accounting Intelligence Progress Map",
        "objective": "Prove how far accountant work can be automated, then turn that proof into firm-facing local toolkit evidence.",
        "current_horizon": current_horizon,
        "completed_horizons": completed_horizons,
        "open_decisions": decisions,
        "automation_snapshot": {
            "review_packs": gap.total_review_packs,
            "automated_packs": gap.automated_packs,
            "human_review_packs": gap.human_review_packs,
            "automation_rate": gap.automation_rate,
        },
        "remaining_gaps": [
            item for item in gap.remaining_gaps if "external accountant" not in item.lower()
        ],
        "next_leaf": "WCD4_coverage_depth_metric_update",
        "next_command": "python scripts\\workflow_coverage_depth_metric.py --format text --write",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(progress: dict[str, Any]) -> str:
    current = progress["current_horizon"]
    snapshot = progress["automation_snapshot"]
    lines = [
        f"# {progress['title']}",
        "",
        "> Scope: plain-language objective/horizon/milestone position for continuing Accounting Intelligence work.",
        "",
        "## One-Line Position",
        "",
        "Objective gaps are grouped into horizons; WCD1 to WCD3 are complete and WCD4 coverage depth metric update is now active.",
        "",
        "## Objective",
        "",
        progress["objective"],
        "",
        "## Current Horizon",
        "",
        f"- Horizon: `{current['id']}`",
        f"- Status: {current['status']}",
        f"- Goal: {current['goal']}",
        "",
        "| Milestone | Name | Status |",
        "|---|---|---|",
    ]
    for milestone in current["milestones"]:
        lines.append(f"| {milestone['id']} | {milestone['name']} | {milestone['status']} |")
    lines.extend(
        [
            "",
            "## Completed Capability Chain",
            "",
            "| Horizon | Result | Evidence |",
            "|---|---|---|",
        ]
    )
    for horizon in progress["completed_horizons"]:
        lines.append(f"| {horizon['id']} | {horizon['result']} | `{horizon['evidence']}` |")
    lines.extend(
        [
            "",
            "## Automation Snapshot",
            "",
            f"- Review packs: {snapshot['review_packs']}",
            f"- Automated packs: {snapshot['automated_packs']}",
            f"- Human-review packs: {snapshot['human_review_packs']}",
            f"- Automation rate: {snapshot['automation_rate']:.2%}",
            "",
            "## Open Decisions",
            "",
            "| Decision | Status | Blocker | Command |",
            "|---|---|---|---|",
        ]
    )
    for decision in progress["open_decisions"]:
        lines.append(
            f"| {decision['id']} | {decision['status']} | {decision['blocker']} | `{decision['command']}` |"
        )
    lines.extend(
        [
            "",
            "## Remaining Gaps",
            "",
        ]
    )
    lines.extend(f"- {gap}" for gap in progress["remaining_gaps"])
    lines.extend(
        [
            "",
            "## Next Leaf",
            "",
            f"- decision: `{progress['next_leaf']}`",
            f"- command: `{progress['next_command']}`",
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps(progress, ensure_ascii=False, indent=2, default=str),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH) -> dict[str, Any]:
    progress = build_progress_map()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(progress), encoding="utf-8")
    return progress


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Render the Accounting Intelligence objective/horizon progress map.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    progress = write_report(args.out) if args.write else build_progress_map()
    if args.format == "json":
        print(json.dumps(progress, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(progress), end="")
    else:
        print(progress["title"])
        print(f"- objective: {progress['objective']}")
        print(f"- current horizon: {progress['current_horizon']['id']}")
        print(f"- next leaf: {progress['next_leaf']}")
        print(f"- next command: {progress['next_command']}")


if __name__ == "__main__":
    main()
