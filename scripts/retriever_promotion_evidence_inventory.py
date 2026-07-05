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
from scripts.product_trust_quality_gate import build_gate as build_product_trust_gate  # noqa: E402
from scripts.rag_quality_final_gate import build_report as build_final_gate_report  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-rpg1-promotion-evidence-inventory.md"
REQUIRED_REPORTS = {
    "rag_quality_close": ROOT / "docs" / "reports" / "2026-07-05-rag-quality-refresh-close-report.md",
    "default_retriever_guard": ROOT / "docs" / "reports" / "2026-07-05-default-retriever-guard.md",
    "product_trust_close": ROOT / "docs" / "reports" / "2026-07-05-product-trust-quality-close-report.md",
    "failure_boundary": ROOT / "docs" / "reports" / "2026-07-05-ptq3-failure-boundary-matrix.md",
    "workflow_coverage_close": ROOT
    / "docs"
    / "reports"
    / "2026-07-05-workflow-coverage-expansion-close-report.md",
}


def build_retriever_promotion_evidence_inventory() -> dict[str, Any]:
    final_gate = build_final_gate_report()
    default_guard = check_default_retriever_guard()
    product_trust = build_product_trust_gate()
    reports = {
        name: {"path": _display_path(path), "exists": path.exists()}
        for name, path in REQUIRED_REPORTS.items()
    }
    missing_reports = [name for name, info in reports.items() if not info["exists"]]
    promotion_supporting = [
        {
            "id": "target_recall_at_20_full_coverage",
            "evidence": "final opt-in retriever reaches recall@20 1.000 on current 50-item retrieval-only eval",
            "source": "docs/reports/2026-07-05-rag-quality-refresh-close-report.md",
        },
        {
            "id": "target_misses_zero",
            "evidence": "final gate reports no target misses under opt-in repair stack",
            "source": "scripts/rag_quality_final_gate.py",
        },
        {
            "id": "repair_retriever_available",
            "evidence": f"{default_guard['target_retriever']} exists as an opt-in eval retriever",
            "source": "scripts/default_retriever_guard.py",
        },
    ]
    promotion_blocking = [
        {
            "id": "default_guard_defers_promotion",
            "evidence": f"default guard decision is {default_guard['promotion_decision']} and promote_to_default is {default_guard['promote_to_default']}",
            "source": "docs/reports/2026-07-05-default-retriever-guard.md",
        },
        {
            "id": "target_not_exposed_in_mcp",
            "evidence": "target repair retriever is not exposed as an MCP search mode",
            "source": "scripts/default_retriever_guard.py",
        },
        {
            "id": "general_usage_not_proven",
            "evidence": "current evidence is strong on the 50-item eval but not yet a broad default-runtime proof",
            "source": "docs/reports/2026-07-05-rag-quality-refresh-close-report.md",
        },
    ]
    advisory = [
        {
            "id": "product_trust_failure_boundaries",
            "evidence": "product trust close gate carries retrieval_quality and default_promotion failure categories",
            "source": "docs/reports/2026-07-05-product-trust-quality-close-report.md",
        },
        {
            "id": "workflow_coverage_closed",
            "evidence": "workflow coverage expansion is closed, so promotion decision can focus on runtime retrieval quality",
            "source": "docs/reports/2026-07-05-workflow-coverage-expansion-close-report.md",
        },
    ]
    missing_evidence = [
        "broad runtime latency/cost measurement",
        "regression gate that compares recall/citation preservation and runtime cost together",
        "operator rollback policy and command surface",
        "explicit final promote/defer/block close result",
    ]
    checks = {
        "final_gate_ok": final_gate["ok"],
        "default_guard_ok": default_guard["ok"],
        "product_trust_ok": product_trust["ok"],
        "supporting_evidence_present": bool(promotion_supporting),
        "blocking_evidence_present": bool(promotion_blocking),
        "advisory_evidence_present": bool(advisory),
        "missing_evidence_recorded": bool(missing_evidence),
        "all_required_reports_present": not missing_reports,
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "RPG1 Promotion Evidence Inventory",
        "ok": not errors,
        "horizon": "runtime-retriever-promotion-gate",
        "completed_milestone": "RPG1",
        "target_retriever": default_guard["target_retriever"],
        "current_default": default_guard["default_mode"],
        "promotion_decision_now": "defer",
        "promotion_supporting": promotion_supporting,
        "promotion_blocking": promotion_blocking,
        "advisory": advisory,
        "missing_evidence": missing_evidence,
        "checks": checks,
        "errors": errors,
        "reports": reports,
        "missing_reports": missing_reports,
        "next_gate": "regression_and_latency_gate",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: RPG1 inventory for runtime retriever promotion decisioning.",
        "",
        "## 한 줄 결론",
        "",
        "The opt-in repair retriever has strong recall-supporting evidence, but current product evidence still points to `defer` until regression/latency, rollback, and operator evidence are added.",
        "",
        "## Runtime Boundary",
        "",
        f"- target retriever: `{result['target_retriever']}`",
        f"- current default: `{result['current_default']}`",
        f"- promotion decision now: `{result['promotion_decision_now']}`",
        f"- next gate: `{result['next_gate']}`",
        "",
        "## Promotion-Supporting Evidence",
        "",
    ]
    lines.extend(_render_evidence_items(result["promotion_supporting"]))
    lines.extend(["", "## Promotion-Blocking Evidence", ""])
    lines.extend(_render_evidence_items(result["promotion_blocking"]))
    lines.extend(["", "## Advisory Evidence", ""])
    lines.extend(_render_evidence_items(result["advisory"]))
    lines.extend(["", "## Missing Evidence Before Promotion", ""])
    lines.extend(f"- {item}" for item in result["missing_evidence"])
    lines.extend(["", "## Checks", "", "| Check | OK |", "|---|---|"])
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
            json.dumps(result, ensure_ascii=False, indent=2, default=str),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH) -> dict[str, Any]:
    result = build_retriever_promotion_evidence_inventory()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _render_evidence_items(items: list[dict[str, str]]) -> list[str]:
    return [f"- `{item['id']}` — {item['evidence']} (`{item['source']}`)" for item in items]


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build RPG1 retriever promotion evidence inventory.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_retriever_promotion_evidence_inventory()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- target retriever: {result['target_retriever']}")
        print(f"- promotion decision now: {result['promotion_decision_now']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
