from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-rqf3-regression-matrix.md"


def build_regression_matrix() -> dict[str, Any]:
    comparisons = [
        _comparison(
            axis="fresh_numeric_eval",
            baseline_status="missing_public_numeric_eval",
            opt_in_status="previous_evidence_only",
            pass_status=False,
            blocker="fresh baseline and opt-in rerun are missing",
        ),
        _comparison(
            axis="known_regressions",
            baseline_status="not_recomputed",
            opt_in_status="not_recomputed",
            pass_status=False,
            blocker="regression count cannot be trusted without a fresh comparison run",
        ),
        _comparison(
            axis="latency",
            baseline_status="not_recomputed",
            opt_in_status="not_recomputed",
            pass_status=False,
            blocker="latency budget cannot be trusted without a fresh local timing run",
        ),
        _comparison(
            axis="rollback",
            baseline_status="current_default_preserved",
            opt_in_status="rollback_policy_documented",
            pass_status=True,
            blocker="none",
        ),
    ]
    evidence = [
        _evidence("validation_contract", "docs/reports/2026-07-05-rqf1-validation-contract.md"),
        _evidence("baseline_snapshot", "docs/reports/2026-07-05-rqf2-baseline-snapshot.md"),
        _evidence("previous_promotion_gate", "docs/reports/2026-07-05-runtime-retriever-promotion-gate-close-report.md"),
    ]
    checks = {
        "all_evidence_exists": all(item["exists"] for item in evidence),
        "all_axes_present": {item["axis"] for item in comparisons} == {"fresh_numeric_eval", "known_regressions", "latency", "rollback"},
        "rollback_axis_passes": any(item["axis"] == "rollback" and item["pass"] is True for item in comparisons),
        "quality_axes_do_not_pass_without_fresh_runs": all(
            item["pass"] is False for item in comparisons if item["axis"] in {"fresh_numeric_eval", "known_regressions", "latency"}
        ),
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "RQF3 Opt-In Retriever Regression Matrix",
        "ok": not errors,
        "horizon": "rag-quality-fresh-validation",
        "completed_milestone": "RQF3",
        "matrix_result": "defer_until_fresh_comparison",
        "comparisons": comparisons,
        "evidence": evidence,
        "checks": checks,
        "errors": errors,
        "next_leaf": "RQF4_promotion_decision_gate",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: public-safe regression matrix for opt-in retriever promotion evidence.",
        "",
        "## 한 줄 결론",
        "",
        f"Matrix result: `{result['matrix_result']}`. Rollback evidence exists, but quality and latency axes need fresh local reruns.",
        "",
        "## Regression Matrix",
        "",
        "| Axis | Baseline | Opt-In | Pass | Blocker |",
        "|---|---|---|---|---|",
    ]
    for item in result["comparisons"]:
        lines.append(
            f"| {item['axis']} | {item['baseline_status']} | {item['opt_in_status']} | {item['pass']} | {item['blocker']} |"
        )
    lines.extend(["", "## Evidence", "", "| ID | Path | Exists |", "|---|---|---|"])
    for item in result["evidence"]:
        lines.append(f"| {item['id']} | `{item['path']}` | {item['exists']} |")
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
    result = build_regression_matrix()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _comparison(axis: str, baseline_status: str, opt_in_status: str, pass_status: bool, blocker: str) -> dict[str, Any]:
    return {
        "axis": axis,
        "baseline_status": baseline_status,
        "opt_in_status": opt_in_status,
        "pass": pass_status,
        "blocker": blocker,
    }


def _evidence(id_: str, path: str) -> dict[str, Any]:
    return {"id": id_, "path": path, "exists": (ROOT / path).exists()}


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build RQF3 opt-in retriever regression matrix.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_regression_matrix()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- matrix result: {result['matrix_result']}")
        print(f"- next leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
