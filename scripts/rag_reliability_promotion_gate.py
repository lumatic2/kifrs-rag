from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.default_retriever_guard import check_default_retriever_guard  # noqa: E402
from scripts.opt_in_retriever_promotion_decision_gate import check_promotion_decision_gate  # noqa: E402
from scripts.rag_quality_final_gate import build_report as build_final_gate_report  # noqa: E402
from scripts.rag_reliability_repair_policy_candidate import build_policy_candidate  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-rr5-rag-promotion-gate.md"

REQUIRED_REPORTS = [
    ROOT / "docs" / "reports" / "2026-07-05-rr1-rag-baseline-inventory.md",
    ROOT / "docs" / "reports" / "2026-07-05-rr2-eval-matrix.md",
    ROOT / "docs" / "reports" / "2026-07-05-rr3-retrieval-citation-diagnostics.md",
    ROOT / "docs" / "reports" / "2026-07-05-rr4-repair-policy-candidate.md",
]

REGRESSION_COMMANDS = [
    "python scripts\\quality_preflight.py --format text",
    "python scripts\\rag_quality_final_gate.py --format text",
    "python scripts\\default_retriever_guard.py --format text",
    "python scripts\\rag_reliability_retrieval_citation_diagnostics.py --format text",
]

NEXT_HORIZON = "non-ifrs-source-dataization"


def build_promotion_gate() -> dict[str, Any]:
    report_status = [
        {"path": _display_path(path), "exists": path.exists()}
        for path in REQUIRED_REPORTS
    ]
    final_gate = build_final_gate_report()
    promotion = check_promotion_decision_gate(explicit_authorization=False)
    default_guard = check_default_retriever_guard()
    policy = build_policy_candidate()

    errors: list[str] = []
    missing_reports = [row["path"] for row in report_status if not row["exists"]]
    if missing_reports:
        errors.extend(f"missing required report: {path}" for path in missing_reports)
    if final_gate["ok"] is not True:
        errors.extend(f"final_gate: {failure}" for failure in final_gate["failures"])
    if promotion["ok"] is not True:
        errors.extend(f"promotion_gate: {error}" for error in promotion["errors"])
    if default_guard["ok"] is not True:
        errors.extend(f"default_guard: {error}" for error in default_guard["errors"])
    if policy["ok"] is not True:
        errors.extend(f"repair_policy: {error}" for error in policy["errors"])
    if promotion["decision"]["promote_to_default"] is True:
        errors.append("promotion gate unexpectedly approved default retriever promotion")

    default_promotion = bool(promotion["decision"]["promote_to_default"])
    handoff_ready = not errors and not default_promotion
    return {
        "ok": handoff_ready,
        "title": "RR5 RAG Promotion Gate",
        "milestone": "RR5",
        "default_promotion": default_promotion,
        "promotion_decision": promotion["decision"]["decision"],
        "target_retriever": promotion["decision"]["target_retriever"],
        "decision_reason": _decision_reason(promotion),
        "required_reports": report_status,
        "final_gate_snapshot": {
            "ok": final_gate["ok"],
            "n_items": final_gate["n_items"],
            "baseline_recall20": final_gate["baseline_recall20"],
            "target_recall20": final_gate["target_recall20"],
            "target_misses": len(final_gate["target_misses"]),
            "target_absent_citations": final_gate["target_buckets"]["absent"],
        },
        "default_guard_snapshot": {
            "ok": default_guard["ok"],
            "default_mode": default_guard["default_mode"],
            "target_retriever_exposed_in_mcp": default_guard["target_retriever_exposed_in_mcp"],
            "promote_to_default": default_guard["promote_to_default"],
        },
        "policy_snapshot": {
            "accepted": [item["id"] for item in policy["accepted_policies"]],
            "deferred": [item["id"] for item in policy["deferred_policies"]],
        },
        "regression_commands": REGRESSION_COMMANDS,
        "next_horizon": NEXT_HORIZON,
        "handoff_ready": handoff_ready,
        "errors": errors,
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(gate: dict[str, Any]) -> str:
    conclusion = (
        f"Close this horizon without default promotion. `{gate['target_retriever']}` stays opt-in, and `{gate['next_horizon']}` may use the regression commands below."
        if gate["ok"]
        else "Do not close this horizon until the listed gate errors are fixed."
    )
    lines = [
        "# RR5 RAG Promotion Gate",
        "",
        "> Scope: final gate for closing the RAG reliability revalidation horizon.",
        "",
        "## One-Line Conclusion",
        "",
        conclusion,
        "",
        "## Decision",
        "",
        f"- Default promotion: {gate['default_promotion']}",
        f"- Promotion decision: {gate['promotion_decision']}",
        f"- Target retriever: `{gate['target_retriever']}`",
        f"- Reason: {gate['decision_reason']}",
        f"- Next horizon: `{gate['next_horizon']}`",
        f"- Handoff ready: {gate['handoff_ready']}",
        "",
        "## Evidence Chain",
        "",
        "| Report | Exists |",
        "|---|---|",
    ]
    for row in gate["required_reports"]:
        lines.append(f"| `{row['path']}` | {row['exists']} |")
    final = gate["final_gate_snapshot"]
    guard = gate["default_guard_snapshot"]
    lines.extend(
        [
            "",
            "## Quality Snapshot",
            "",
            f"- Items: {final['n_items']}",
            f"- Baseline recall@20: {final['baseline_recall20']:.3f}",
            f"- Target recall@20: {final['target_recall20']:.3f}",
            f"- Target misses: {final['target_misses']}",
            f"- Target absent citations: {final['target_absent_citations']}",
            "",
            "## Runtime Guard",
            "",
            f"- Guard ok: {guard['ok']}",
            f"- Default mode: `{guard['default_mode']}`",
            f"- Target exposed in MCP: {guard['target_retriever_exposed_in_mcp']}",
            f"- Guard promote_to_default: {guard['promote_to_default']}",
            "",
            "## Regression Commands For Next Horizon",
            "",
        ]
    )
    lines.extend(f"- `{command}`" for command in gate["regression_commands"])
    if gate["errors"]:
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in gate["errors"])
    lines.extend(
        [
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps(gate, ensure_ascii=False, indent=2, default=str),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH) -> dict[str, Any]:
    gate = build_promotion_gate()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(gate), encoding="utf-8")
    return gate


def _decision_reason(promotion: dict[str, Any]) -> str:
    blockers = promotion["decision"]["blockers"]
    if not blockers:
        return "all promotion blockers cleared"
    return "; ".join(blockers)


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run RR5 RAG promotion gate and handoff.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    gate = write_report(args.out) if args.write else build_promotion_gate()
    if args.format == "json":
        print(json.dumps(gate, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(gate), end="")
    else:
        print(gate["title"])
        print(f"- ok: {gate['ok']}")
        print(f"- default_promotion: {gate['default_promotion']}")
        print(f"- promotion_decision: {gate['promotion_decision']}")
        print(f"- next_horizon: {gate['next_horizon']}")
        print(f"- report_path: {gate['report_path']}")
    if not gate["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
