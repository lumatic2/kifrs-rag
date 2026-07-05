from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.controlled_lane_close_gate import build_controlled_lane_close_gate  # noqa: E402
from scripts.first_workflow_contract import build_first_workflow_contract  # noqa: E402
from scripts.minimal_workflow_review_pack_adapter import build_minimal_review_pack_adapter  # noqa: E402
from scripts.product_trust_quality_gate import build_gate as build_product_trust_gate  # noqa: E402
from scripts.workflow_coverage_gap_ranking import build_workflow_coverage_gap_ranking  # noqa: E402
from scripts.workflow_coverage_metric_update import build_workflow_coverage_metric_update  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-workflow-coverage-expansion-close-report.md"
REQUIRED_REPORTS = {
    "wce1_coverage_gap_ranking": ROOT / "docs" / "reports" / "2026-07-05-wce1-coverage-gap-ranking.md",
    "wce2_first_workflow_contract": ROOT / "docs" / "reports" / "2026-07-05-wce2-first-workflow-contract.md",
    "wce3_minimal_review_pack_adapter": ROOT / "docs" / "reports" / "2026-07-05-wce3-minimal-review-pack-adapter.md",
    "wce4_coverage_metric_update": ROOT / "docs" / "reports" / "2026-07-05-wce4-coverage-metric-update.md",
    "product_trust_close": ROOT / "docs" / "reports" / "2026-07-05-product-trust-quality-close-report.md",
    "controlled_lane_close": ROOT
    / "docs"
    / "reports"
    / "2026-07-05-source-body-ingestion-controlled-lane-close-report.md",
}


def build_workflow_coverage_close_gate() -> dict[str, Any]:
    wce1 = build_workflow_coverage_gap_ranking()
    wce2 = build_first_workflow_contract()
    wce3 = build_minimal_review_pack_adapter()
    wce4 = build_workflow_coverage_metric_update()
    product_trust = build_product_trust_gate()
    controlled_lane = build_controlled_lane_close_gate()
    reports = {
        name: {"path": _display_path(path), "exists": path.exists()}
        for name, path in REQUIRED_REPORTS.items()
    }
    missing_reports = [name for name, info in reports.items() if not info["exists"]]
    checks = {
        "wce1_ranking_ok": wce1["ok"],
        "wce2_contract_ok": wce2["ok"],
        "wce3_adapter_ok": wce3["ok"],
        "wce4_metric_ok": wce4["ok"],
        "recommended_candidate_carried": wce1["recommended_candidate"] == wce2["selected_candidate"] == wce3["workflow_id"],
        "coverage_recorded_without_overclaim": wce4["new_workflow"]["coverage_status"]
        == "conditional_decision_prep_adapter",
        "product_trust_carried": product_trust["ok"],
        "controlled_lane_carried": controlled_lane["ok"],
        "all_required_reports_present": not missing_reports,
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "Workflow Coverage Expansion Close Gate",
        "ok": not errors,
        "horizon": "workflow-coverage-expansion",
        "completed_milestone": "WCE5",
        "close_status": "closed" if not errors else "blocked",
        "new_workflow": "1037_provisions",
        "coverage_status": wce4["new_workflow"]["coverage_status"],
        "checks": checks,
        "errors": errors,
        "reports": reports,
        "missing_reports": missing_reports,
        "next_horizon": "runtime-retriever-promotion-gate",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: WCE5 close gate for workflow coverage expansion.",
        "",
        "## 한 줄 결론",
        "",
        (
            "Workflow coverage expansion is closed: the 1037 provisions workflow now has ranking, contract, adapter, and coverage metric evidence without claiming full automation."
            if result["ok"]
            else "Workflow coverage expansion is blocked; fix the listed checks."
        ),
        "",
        "## Close Status",
        "",
        f"- status: {result['close_status']}",
        f"- new workflow: `{result['new_workflow']}`",
        f"- coverage status: `{result['coverage_status']}`",
        f"- next horizon: `{result['next_horizon']}`",
        "",
        "## Checks",
        "",
        "| Check | OK |",
        "|---|---|",
    ]
    for name, ok in result["checks"].items():
        lines.append(f"| {name} | {ok} |")
    lines.extend(["", "## Required Reports", "", "| Report | Path | Exists |", "|---|---|---|"])
    for name, info in result["reports"].items():
        lines.append(f"| {name} | `{info['path']}` | {info['exists']} |")
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
    result = build_workflow_coverage_close_gate()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Run WCE5 workflow coverage close gate.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_workflow_coverage_close_gate()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- close status: {result['close_status']}")
        print(f"- next horizon: {result['next_horizon']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
