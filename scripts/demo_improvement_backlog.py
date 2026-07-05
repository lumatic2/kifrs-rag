from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-drq4-demo-improvement-backlog.md"


def build_improvement_backlog() -> dict[str, Any]:
    findings = [
        {
            "finding_id": "retriever-decision-timing-warning",
            "source_stage": "retriever-decision",
            "finding": "timing variance recorded during rehearsal",
            "severity": "medium",
        },
        {
            "finding_id": "stage-output-freshness-check",
            "source_stage": "all",
            "finding": "stage reports can be stale if commands are skipped",
            "severity": "medium",
        },
        {
            "finding_id": "operator-summary-density",
            "source_stage": "position",
            "finding": "operator needs a compact current-state summary before demo start",
            "severity": "low",
        },
    ]
    backlog = [
        _item("DRQ4-1", findings[0], "Add retriever-decision timing note and expected variance threshold to the next checklist.", 4, 1),
        _item("DRQ4-2", findings[1], "Add generated-at freshness metadata check to rehearsal evidence capture.", 5, 2),
        _item("DRQ4-3", findings[2], "Add one-screen operator summary to the progress map report.", 3, 2),
    ]
    prioritized = sorted(backlog, key=lambda item: (-item["priority_score"], item["item_id"]))
    checks = {
        "findings_present": len(findings) >= 3,
        "backlog_items_present": len(backlog) >= 3,
        "all_items_internal": all(item["dependency"] == "internal" for item in backlog),
        "all_items_prioritized": all(item["priority_score"] > 0 for item in backlog),
        "next_milestone_named": True,
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "DRQ4 Demo Improvement Backlog",
        "ok": not errors,
        "horizon": "demo-rehearsal-quality-loop",
        "completed_milestone": "DRQ4",
        "findings": findings,
        "backlog": prioritized,
        "checks": checks,
        "errors": errors,
        "next_leaf": "DRQ5_horizon_close_and_objective_gap_audit",
        "report_path": _display_path(REPORT_PATH),
    }


def _item(
    item_id: str,
    finding: dict[str, str],
    action: str,
    product_impact: int,
    implementation_cost: int,
) -> dict[str, Any]:
    return {
        "item_id": item_id,
        "finding_id": finding["finding_id"],
        "source_stage": finding["source_stage"],
        "action": action,
        "product_impact": product_impact,
        "implementation_cost": implementation_cost,
        "priority_score": product_impact - implementation_cost,
        "dependency": "internal",
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: internal product improvement backlog from demo rehearsal findings.",
        "",
        "## 한 줄 결론",
        "",
        "Rehearsal findings are converted into prioritized internal fixes; no external dependency is introduced.",
        "",
        "## Findings",
        "",
        "| Finding | Stage | Severity | Summary |",
        "|---|---|---|---|",
    ]
    for finding in result["findings"]:
        lines.append(
            "| {finding_id} | {source_stage} | {severity} | {finding} |".format(**finding)
        )
    lines.extend(
        [
            "",
            "## Prioritized Backlog",
            "",
            "| Item | Finding | Action | Impact | Cost | Score | Dependency |",
            "|---|---|---|---:|---:|---:|---|",
        ]
    )
    for item in result["backlog"]:
        lines.append(
            "| {item_id} | {finding_id} | {action} | {product_impact} | {implementation_cost} | {priority_score} | {dependency} |".format(
                **item
            )
        )
    lines.extend(["", "## Checks", "", "| Check | OK |", "|---|---|"])
    for name, ok in result["checks"].items():
        lines.append(f"| {name} | {ok} |")
    lines.extend(["", "## Errors", ""])
    lines.extend(f"- {error}" for error in result["errors"]) if result["errors"] else lines.append("- none")
    lines.extend(
        [
            "",
            "## Next Leaf",
            "",
            f"- `{result['next_leaf']}`",
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps(result, ensure_ascii=False, indent=2),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH) -> dict[str, Any]:
    result = build_improvement_backlog()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build DRQ4 demo improvement backlog report.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_improvement_backlog()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- backlog items: {len(result['backlog'])}")
        print(f"- next leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
