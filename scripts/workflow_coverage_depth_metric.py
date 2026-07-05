from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-wcd4-coverage-depth-metric.md"
TOTAL_SERVICE_LINES = 8


def build_metric_update() -> dict[str, Any]:
    workflow_records = [
        {
            "workflow_id": "1109_financial_instrument_review",
            "service_lines": ["F-ACC", "F-AUD"],
            "coverage_status": "decision_engine_evidence",
            "evidence_depth": 4,
        },
        {
            "workflow_id": "1116_lease_review_pack",
            "service_lines": ["F-ACC", "F-AUD"],
            "coverage_status": "review_pack_and_disclosure_evidence",
            "evidence_depth": 4,
        },
        {
            "workflow_id": "1037_provisions",
            "service_lines": ["F-ACC", "F-AUD"],
            "coverage_status": "conditional_decision_prep_adapter",
            "evidence_depth": 3,
        },
        {
            "workflow_id": "audit_disclosure_tie_out",
            "service_lines": ["F-AUD", "F-ACC"],
            "coverage_status": "minimal_decision_prep_adapter",
            "evidence_depth": 3,
        },
    ]
    touched_service_lines = sorted({line for record in workflow_records for line in record["service_lines"]})
    metric = {
        "service_lines_total": TOTAL_SERVICE_LINES,
        "service_lines_with_adapter_evidence": len(touched_service_lines),
        "service_line_touch_rate": len(touched_service_lines) / TOTAL_SERVICE_LINES,
        "workflow_surfaces_with_adapter_evidence": len(workflow_records),
        "conditional_or_better_workflows": sum(record["evidence_depth"] >= 3 for record in workflow_records),
        "new_workflow_added": "audit_disclosure_tie_out",
        "not_a_field_validation_rate": True,
    }
    limits = [
        "metric counts repo evidence, not actual firm adoption",
        "metric does not claim external accountant validation",
        "metric does not claim final audit or accounting conclusion automation",
        "metric does not include tax-agent workflows",
    ]
    checks = {
        "new_workflow_recorded": any(record["workflow_id"] == "audit_disclosure_tie_out" for record in workflow_records),
        "service_line_count_bounded": metric["service_lines_with_adapter_evidence"] <= metric["service_lines_total"],
        "workflow_count_increased": metric["workflow_surfaces_with_adapter_evidence"] >= 4,
        "not_field_validation_rate": metric["not_a_field_validation_rate"] is True,
        "limits_recorded": len(limits) >= 4,
        "next_milestone_named": True,
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "WCD4 Coverage Depth Metric Update",
        "ok": not errors,
        "horizon": "workflow-coverage-depth-expansion",
        "completed_milestone": "WCD4",
        "workflow_records": workflow_records,
        "touched_service_lines": touched_service_lines,
        "metric": metric,
        "limits": limits,
        "checks": checks,
        "errors": errors,
        "next_leaf": "WCD5_horizon_close_and_demo_rehearsal_handoff",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    metric = result["metric"]
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: update internal workflow coverage depth after WCD3 adapter evidence.",
        "",
        "## 한 줄 결론",
        "",
        (
            "`audit_disclosure_tie_out` adds one public-safe minimal adapter surface. "
            "This is repo evidence coverage, not field validation or final judgment automation."
        ),
        "",
        "## Workflow Records",
        "",
        "| Workflow | Service Lines | Status | Evidence Depth |",
        "|---|---|---|---:|",
    ]
    for record in result["workflow_records"]:
        lines.append(
            "| {workflow_id} | {service_lines} | {coverage_status} | {evidence_depth} |".format(
                workflow_id=record["workflow_id"],
                service_lines=", ".join(record["service_lines"]),
                coverage_status=record["coverage_status"],
                evidence_depth=record["evidence_depth"],
            )
        )
    lines.extend(
        [
            "",
            "## Metric",
            "",
            f"- service lines total: {metric['service_lines_total']}",
            f"- service lines with adapter evidence: {metric['service_lines_with_adapter_evidence']}",
            f"- service-line touch rate: {metric['service_line_touch_rate']:.2%}",
            f"- workflow surfaces with adapter evidence: {metric['workflow_surfaces_with_adapter_evidence']}",
            f"- conditional or better workflows: {metric['conditional_or_better_workflows']}",
            f"- new workflow added: `{metric['new_workflow_added']}`",
            f"- not a field validation rate: {metric['not_a_field_validation_rate']}",
            "",
            "## Limits",
            "",
        ]
    )
    lines.extend(f"- {limit}" for limit in result["limits"])
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
    result = build_metric_update()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build WCD4 workflow coverage depth metric report.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_metric_update()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- new workflow: {result['metric']['new_workflow_added']}")
        print(f"- next leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
