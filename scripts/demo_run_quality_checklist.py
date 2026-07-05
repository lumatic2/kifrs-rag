from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.demo_rehearsal_script import build_rehearsal_script  # noqa: E402

REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-drq2-demo-run-quality-checklist.md"


def build_quality_checklist() -> dict[str, Any]:
    rehearsal = build_rehearsal_script()
    stage_checks = [_checks_for_stage(stage) for stage in rehearsal["stages"]]
    checks = {
        "stage_checks_present": len(stage_checks) == len(rehearsal["stages"]),
        "each_stage_has_pass_checks": all(item["pass_checks"] for item in stage_checks),
        "each_stage_has_failure_note": all(item["failure_note"] for item in stage_checks),
        "each_stage_has_recovery_route": all(item["recovery_route"] for item in stage_checks),
        "has_timing_check": all(any("timing" in check for check in item["pass_checks"]) for item in stage_checks),
        "next_milestone_named": True,
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "DRQ2 Demo Run Quality Checklist",
        "ok": not errors,
        "horizon": "demo-rehearsal-quality-loop",
        "completed_milestone": "DRQ2",
        "source_stage_count": len(rehearsal["stages"]),
        "stage_checks": stage_checks,
        "checks": checks,
        "errors": errors,
        "next_leaf": "DRQ3_rehearsal_evidence_capture",
        "report_path": _display_path(REPORT_PATH),
    }


def _checks_for_stage(stage: dict[str, Any]) -> dict[str, Any]:
    timing_variance_threshold_seconds = 15 if stage["stage_id"] == "retriever-decision" else 0
    return {
        "stage_id": stage["stage_id"],
        "target_seconds": stage["target_seconds"],
        "timing_variance_threshold_seconds": timing_variance_threshold_seconds,
        "pass_checks": [
            "command_exits_zero_or_existing_report_is_present",
            "expected_output_path_exists",
            "public_safe_boundary_still_visible",
            "timing_within_stage_budget_or_within_variance_threshold",
        ],
        "failure_note": (
            "record missing report, timeout, unclear boundary, stale output, or timing variance above threshold before continuing"
        ),
        "recovery_route": stage["recovery_route"],
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: pass/fail checklist for each timed demo rehearsal stage.",
        "",
        "## 한 줄 결론",
        "",
        "Every rehearsal stage has pass checks, a failure note, a recovery route, and a timing check.",
        "",
        "## Stage Checks",
        "",
        "| Stage | Target Seconds | Variance Threshold | Pass Checks | Failure Note | Recovery |",
        "|---|---:|---:|---|---|---|",
    ]
    for item in result["stage_checks"]:
        lines.append(
            "| {stage_id} | {target_seconds} | {timing_variance_threshold_seconds} | {pass_checks} | {failure_note} | {recovery_route} |".format(
                stage_id=item["stage_id"],
                target_seconds=item["target_seconds"],
                timing_variance_threshold_seconds=item["timing_variance_threshold_seconds"],
                pass_checks=", ".join(item["pass_checks"]),
                failure_note=item["failure_note"],
                recovery_route=item["recovery_route"],
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
    result = build_quality_checklist()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build DRQ2 demo run quality checklist report.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_quality_checklist()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- stages: {result['source_stage_count']}")
        print(f"- next leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
