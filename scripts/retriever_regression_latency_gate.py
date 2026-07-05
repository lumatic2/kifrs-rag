from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.retriever_promotion_evidence_inventory import build_retriever_promotion_evidence_inventory  # noqa: E402
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-rpg2-regression-latency-gate.md"


def build_retriever_regression_latency_gate() -> dict[str, Any]:
    inventory = build_retriever_promotion_evidence_inventory()
    checks = {
        "inventory_ok": inventory["ok"],
        "recall_support_present": any(
            item["id"] == "target_recall_at_20_full_coverage"
            for item in inventory["promotion_supporting"]
        ),
        "citation_miss_support_present": any(
            item["id"] == "target_misses_zero" for item in inventory["promotion_supporting"]
        ),
        "default_guard_blocks_accidental_promotion": any(
            item["id"] == "default_guard_defers_promotion"
            for item in inventory["promotion_blocking"]
        ),
        "latency_cost_measured": False,
        "rollback_policy_present": False,
    }
    blocking_reasons = [
        name for name in ["latency_cost_measured", "rollback_policy_present"] if checks[name] is not True
    ]
    promotion_gate_result = "defer" if blocking_reasons else "promotion_candidate"
    errors = [
        name
        for name in [
            "inventory_ok",
            "recall_support_present",
            "citation_miss_support_present",
            "default_guard_blocks_accidental_promotion",
        ]
        if checks[name] is not True
    ]
    return {
        "title": "RPG2 Regression And Latency Gate",
        "ok": not errors,
        "horizon": "runtime-retriever-promotion-gate",
        "completed_milestone": "RPG2",
        "target_retriever": inventory["target_retriever"],
        "current_default": inventory["current_default"],
        "promotion_gate_result": promotion_gate_result,
        "checks": checks,
        "blocking_reasons": blocking_reasons,
        "errors": errors,
        "minimum_requirements": [
            "inventory is valid",
            "recall support exists",
            "citation miss support exists",
            "default guard blocks accidental promotion",
            "latency/cost measurement exists",
            "rollback policy exists",
        ],
        "next_gate": "failure_and_rollback_policy",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: RPG2 regression and runtime-cost precondition gate.",
        "",
        "## 한 줄 결론",
        "",
        "Recall and citation evidence are present, but promotion remains `defer` because latency/cost measurement and rollback policy are not yet present.",
        "",
        "## Gate Result",
        "",
        f"- target retriever: `{result['target_retriever']}`",
        f"- current default: `{result['current_default']}`",
        f"- promotion gate result: `{result['promotion_gate_result']}`",
        f"- next gate: `{result['next_gate']}`",
        "",
        "## Minimum Requirements",
        "",
    ]
    lines.extend(f"- {item}" for item in result["minimum_requirements"])
    lines.extend(["", "## Checks", "", "| Check | OK |", "|---|---|"])
    for name, ok in result["checks"].items():
        lines.append(f"| {name} | {ok} |")
    lines.extend(["", "## Blocking Reasons", ""])
    lines.extend(f"- {reason}" for reason in result["blocking_reasons"]) if result["blocking_reasons"] else lines.append("- none")
    lines.extend(["", "## Errors", ""])
    lines.extend(f"- {error}" for error in result["errors"]) if result["errors"] else lines.append("- none")
    lines.extend(
        [
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps(result, ensure_ascii=False, indent=2, default=str),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH) -> dict[str, Any]:
    result = build_retriever_regression_latency_gate()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build RPG2 regression and latency gate.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_retriever_regression_latency_gate()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- promotion gate result: {result['promotion_gate_result']}")
        for reason in result["blocking_reasons"]:
            print(f"- blocks promotion: {reason}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
