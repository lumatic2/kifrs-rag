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
    ]
    current_horizon = {
        "id": "multi-authority-runtime-hardening",
        "status": "active",
        "goal": "Use K-IFRS, supporting interpretation, legal boundary, fact evidence, and client-private facts as separated runtime evidence.",
        "milestones": [
            {"id": "MAH1", "name": "runtime evidence boundary audit", "status": "completed"},
            {"id": "MAH2", "name": "runtime evidence contract hardening", "status": "completed"},
            {"id": "MAH3", "name": "review pack authority panel", "status": "active_next"},
            {"id": "MAH4", "name": "statement draft and analytics fact hook", "status": "pending"},
            {"id": "MAH5", "name": "authority composer gate and runtime demo", "status": "pending"},
        ],
    }
    decisions = [
        {
            "id": "run_MAH3_review_pack_authority_panel",
            "status": "active",
            "decide": "Attach the shared five-group runtime authority boundary to 1116, 1109, and 1115 review pack outputs.",
            "blocker": "none",
            "command": "python -m pytest tests\\test_1116_review_pack.py tests\\test_1109_review_pack.py tests\\test_1115_review_pack.py -q",
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
        "remaining_gaps": [
            item for item in gap.remaining_gaps if "external accountant" not in item.lower()
        ],
        "next_leaf": "MAH3_review_pack_authority_panel",
        "next_command": "python -m pytest tests\\test_1116_review_pack.py tests\\test_1109_review_pack.py tests\\test_1115_review_pack.py -q",
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
        "The active horizon is multi-authority runtime hardening: make workflow outputs keep primary, supporting, legal, fact, and private evidence separate.",
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
