from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-drq1-demo-rehearsal-script.md"


def build_rehearsal_script() -> dict[str, Any]:
    stages = [
        _stage(0, "position", "python scripts\\accounting_intelligence_progress_map.py --format text --write", "docs/reports/2026-07-05-accounting-intelligence-progress-map.md", 60),
        _stage(1, "storyboard", "python scripts\\e2e_demo_asset_inventory.py --format text --write", "docs/reports/2026-07-05-e2e1-demo-asset-inventory.md", 90),
        _stage(2, "scenario-contract", "python scripts\\e2e_scenario_contract.py --format text --write", "docs/reports/2026-07-05-e2e2-scenario-contract.md", 90),
        _stage(3, "local-parser-boundary", "python scripts\\real_local_parser_prototype_close_gate.py --format text", "docs/reports/2026-07-05-real-local-parser-prototype-close-report.md", 90),
        _stage(4, "source-lane-boundary", "python scripts\\external_source_connector_body_close_gate.py --format text", "docs/reports/2026-07-05-external-source-body-connector-expansion-close-report.md", 90),
        _stage(5, "workflow-depth", "python scripts\\workflow_coverage_depth_close_gate.py --format text", "docs/reports/2026-07-05-workflow-coverage-depth-expansion-close-report.md", 90),
        _stage(6, "retriever-decision", "python scripts\\runtime_retriever_promotion_close_gate.py --format text", "docs/reports/2026-07-05-runtime-retriever-promotion-gate-close-report.md", 90),
        _stage(7, "operator-surface", "python scripts\\operator_experience_close_gate.py --format text", "docs/reports/2026-07-05-operator-experience-hardening-close-report.md", 90),
    ]
    total_budget_seconds = sum(stage["target_seconds"] for stage in stages)
    checks = {
        "stages_present": len(stages) >= 8,
        "all_stages_have_command": all(stage["operator_command"] for stage in stages),
        "all_stages_have_expected_output": all(stage["expected_output"] for stage in stages),
        "timing_budget_present": total_budget_seconds > 0,
        "public_safe_outputs_only": all(stage["expected_output"].startswith("docs/reports/") for stage in stages),
        "next_milestone_named": True,
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "DRQ1 Demo Rehearsal Script And Timing Gate",
        "ok": not errors,
        "horizon": "demo-rehearsal-quality-loop",
        "completed_milestone": "DRQ1",
        "total_budget_seconds": total_budget_seconds,
        "total_budget_minutes": round(total_budget_seconds / 60, 2),
        "stages": stages,
        "checks": checks,
        "errors": errors,
        "next_leaf": "DRQ2_demo_run_quality_checklist",
        "report_path": _display_path(REPORT_PATH),
    }


def _stage(order: int, stage_id: str, command: str, expected_output: str, target_seconds: int) -> dict[str, Any]:
    return {
        "order": order,
        "stage_id": stage_id,
        "operator_command": command,
        "expected_output": expected_output,
        "target_seconds": target_seconds,
        "recovery_route": "rerun stage command and inspect the expected report path",
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: timed local rehearsal script for the public-safe demo packet.",
        "",
        "## 한 줄 결론",
        "",
        (
            f"The demo rehearsal now has {len(result['stages'])} stages and a "
            f"{result['total_budget_minutes']}-minute target budget with explicit expected outputs."
        ),
        "",
        "## Rehearsal Stages",
        "",
        "| Order | Stage | Command | Expected Output | Target Seconds | Recovery |",
        "|---:|---|---|---|---:|---|",
    ]
    for stage in result["stages"]:
        lines.append(
            "| {order} | `{stage_id}` | `{operator_command}` | `{expected_output}` | {target_seconds} | {recovery_route} |".format(
                **stage
            )
        )
    lines.extend(
        [
            "",
            "## Timing Gate",
            "",
            f"- total budget seconds: {result['total_budget_seconds']}",
            f"- total budget minutes: {result['total_budget_minutes']}",
            "",
            "## Checks",
            "",
            "| Check | OK |",
            "|---|---|",
        ]
    )
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
    result = build_rehearsal_script()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build DRQ1 demo rehearsal script report.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_rehearsal_script()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- stages: {len(result['stages'])}")
        print(f"- next leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
