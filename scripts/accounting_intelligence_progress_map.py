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
from scripts.accounting_intelligence_next_action import build_next_action  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-accounting-intelligence-progress-map.md"


def build_progress_map() -> dict[str, Any]:
    gap = build_gap_audit()
    next_action = build_next_action()
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
            "id": "field-feedback runbook/capture",
            "result": "Prepared a 30-minute feedback session flow and safe feedback capture/queue conversion pipeline.",
            "evidence": "docs/reports/2026-07-05-fc4-field-feedback-capture-close-report.md",
        },
    ]
    current_horizon = {
        "id": "rag-reliability-revalidation",
        "status": "active",
        "goal": "Re-validate K-IFRS RAG quality and define retriever promotion criteria before expanding sources or product UX.",
        "milestones": [
            {"id": "RR1", "name": "baseline inventory", "status": "completed"},
            {"id": "RR2", "name": "eval matrix and seed coverage", "status": "completed"},
            {"id": "RR3", "name": "retrieval and citation diagnostics", "status": "active_next"},
            {"id": "RR4", "name": "repair policy candidate", "status": "pending"},
            {"id": "RR5", "name": "promotion gate and handoff", "status": "pending"},
        ],
    }
    decisions = [
        {
            "id": next_action["recommended_next_decision"],
            "status": next_action["status"],
            "decide": next_action["user_decision"],
            "blocker": next_action["current_blocker"],
            "command": next_action["next_command"],
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
        "objective": "Prove how far accountant work can be automated, then package that proof as a local toolkit for firm PoC.",
        "current_horizon": current_horizon,
        "completed_horizons": completed_horizons,
        "open_decisions": decisions,
        "automation_snapshot": {
            "review_packs": gap.total_review_packs,
            "automated_packs": gap.automated_packs,
            "human_review_packs": gap.human_review_packs,
            "automation_rate": gap.automation_rate,
        },
        "remaining_gaps": gap.remaining_gaps,
        "next_leaf": next_action["recommended_next_decision"] or "RR3_retrieval_and_citation_diagnostics",
        "next_command": next_action["next_command"]
        if next_action["next_command"] != "none"
        else "python scripts\\quality_preflight.py --format text",
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
        "The next active horizon is RAG reliability revalidation: prove the K-IFRS retrieval and citation baseline before source expansion or product hardening.",
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
