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
from scripts.minimal_workflow_review_pack_adapter import build_minimal_review_pack_adapter  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-wce4-coverage-metric-update.md"


def build_workflow_coverage_metric_update() -> dict[str, Any]:
    gap = build_gap_audit()
    adapter = build_minimal_review_pack_adapter()
    new_workflow = {
        "workflow_id": adapter["workflow_id"],
        "service_line": "F-ACC / F-AUD",
        "coverage_status": "conditional_decision_prep_adapter",
        "implemented": [
            "candidate ranking",
            "workflow contract",
            "structured summary",
            "human-review checklist",
            "authority panel",
            "failure case for missing required inputs",
        ],
        "limits": [
            "no raw contract OCR",
            "no final recognition conclusion",
            "no invented probability or estimate",
            "no live external source fetch",
            "no default retriever promotion",
        ],
    }
    coverage_map = {
        "axis_1_workflow_map_coverage": {
            "before": "F-ACC review-pack surface plus F-AUD analytical-procedure support",
            "after": "F-ACC/F-AUD now also has a bounded 1037 provisions decision-prep workflow candidate",
            "delta": "+1 conditional workflow candidate with adapter evidence",
        },
        "axis_2_scenario_completion": {
            "review_packs": gap.total_review_packs,
            "automated_packs": gap.automated_packs,
            "human_review_packs": gap.human_review_packs,
            "automation_rate": gap.automation_rate,
            "new_workflow_status": new_workflow["coverage_status"],
        },
    }
    checks = {
        "gap_audit_ok": gap.ok,
        "adapter_ok": adapter["ok"],
        "new_workflow_recorded": new_workflow["workflow_id"] == "1037_provisions",
        "limits_recorded": bool(new_workflow["limits"]),
        "no_completion_overclaim": new_workflow["coverage_status"] != "fully_automated",
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "WCE4 Coverage Metric Update",
        "ok": not errors,
        "horizon": "workflow-coverage-expansion",
        "completed_milestone": "WCE4",
        "new_workflow": new_workflow,
        "coverage_map": coverage_map,
        "checks": checks,
        "errors": errors,
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    axis_1 = result["coverage_map"]["axis_1_workflow_map_coverage"]
    axis_2 = result["coverage_map"]["axis_2_scenario_completion"]
    workflow = result["new_workflow"]
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: reflect the WCE3 1037 provisions adapter in the objective coverage map.",
        "",
        "## 한 줄 결론",
        "",
        "Coverage expands by one conditional workflow candidate: `1037_provisions` now has ranking, contract, and adapter evidence, but remains a decision-prep draft with human review required.",
        "",
        "## Axis 1 — Workflow Map Coverage",
        "",
        f"- before: {axis_1['before']}",
        f"- after: {axis_1['after']}",
        f"- delta: {axis_1['delta']}",
        "",
        "## Axis 2 — Scenario Completion",
        "",
        f"- review packs: {axis_2['review_packs']}",
        f"- automated packs: {axis_2['automated_packs']}",
        f"- human-review packs: {axis_2['human_review_packs']}",
        f"- automation rate: {axis_2['automation_rate']:.2%}",
        f"- new workflow status: `{axis_2['new_workflow_status']}`",
        "",
        "## New Workflow Coverage Record",
        "",
        f"- workflow id: `{workflow['workflow_id']}`",
        f"- service line: {workflow['service_line']}",
        f"- coverage status: `{workflow['coverage_status']}`",
        "",
        "### Implemented",
        "",
    ]
    lines.extend(f"- {item}" for item in workflow["implemented"])
    lines.extend(["", "### Limits", ""])
    lines.extend(f"- {item}" for item in workflow["limits"])
    lines.extend(["", "## Checks", "", "| Check | OK |", "|---|---|"])
    for name, ok in result["checks"].items():
        lines.append(f"| {name} | {ok} |")
    lines.extend(["", "## Errors", ""])
    lines.extend(f"- {error}" for error in result["errors"]) if result["errors"] else lines.append("- none")
    lines.extend(
        [
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
    result = build_workflow_coverage_metric_update()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build WCE4 coverage metric update.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_workflow_coverage_metric_update()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- workflow id: {result['new_workflow']['workflow_id']}")
        print(f"- status: {result['new_workflow']['coverage_status']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
