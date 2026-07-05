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
from scripts.failure_boundary_matrix import build_matrix as build_failure_matrix  # noqa: E402
from scripts.firm_facing_product_surface_gate import build_gate as build_firm_surface_gate  # noqa: E402
from scripts.product_trust_evidence_inventory import build_inventory as build_evidence_inventory  # noqa: E402
from scripts.promotion_decision_evidence_pack import build_evidence_pack  # noqa: E402
from scripts.review_pack_confidence_contract import build_contract as build_confidence_contract  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-product-trust-quality-close-report.md"
REQUIRED_REPORTS = {
    "ptq1_inventory": ROOT / "docs" / "reports" / "2026-07-05-ptq1-trust-evidence-inventory.md",
    "ptq2_confidence": ROOT / "docs" / "reports" / "2026-07-05-ptq2-review-pack-confidence-contract.md",
    "ptq3_failure_boundary": ROOT / "docs" / "reports" / "2026-07-05-ptq3-failure-boundary-matrix.md",
    "ptq4_promotion": ROOT / "docs" / "reports" / "2026-07-05-ptq4-promotion-decision-evidence.md",
    "firm_surface_close": ROOT / "docs" / "reports" / "2026-07-05-firm-facing-product-surface-close-report.md",
    "rag_quality_close": ROOT / "docs" / "reports" / "2026-07-05-rag-quality-refresh-close-report.md",
    "default_guard": ROOT / "docs" / "reports" / "2026-07-05-default-retriever-guard.md",
}

CARRIED_REGRESSION_COMMANDS = [
    "python -m pytest tests\\test_product_trust_evidence_inventory.py tests\\test_review_pack_confidence_contract.py tests\\test_failure_boundary_matrix.py tests\\test_promotion_decision_evidence_pack.py tests\\test_product_trust_quality_gate.py -q",
    "python scripts\\quality_preflight.py --format text",
    "python scripts\\rag_quality_final_gate.py --format text",
    "python scripts\\default_retriever_guard.py --format text",
    "python scripts\\firm_facing_product_surface_gate.py --format text",
]


def build_gate() -> dict[str, Any]:
    inventory = build_evidence_inventory()
    confidence = build_confidence_contract()
    failure_matrix = build_failure_matrix()
    promotion = build_evidence_pack()
    default_guard = check_default_retriever_guard()
    firm_surface = build_firm_surface_gate()
    reports = {
        name: {"path": _display_path(path), "exists": path.exists()}
        for name, path in REQUIRED_REPORTS.items()
    }
    missing_reports = [name for name, info in reports.items() if not info["exists"]]
    checks = {
        "ptq1_inventory": inventory["ok"],
        "ptq2_confidence": confidence["ok"],
        "ptq3_failure_boundary": failure_matrix["ok"],
        "ptq4_promotion_decision": promotion["ok"] and promotion["decision"] == "defer",
        "default_guard": default_guard["ok"],
        "firm_surface": firm_surface["ok"],
        "all_required_reports_present": not missing_reports,
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "Product Trust And Quality Close Gate",
        "ok": not errors,
        "horizon": "product-trust-and-quality-evidence",
        "milestone": "PTQ5",
        "checks": checks,
        "reports": reports,
        "missing_reports": missing_reports,
        "errors": errors,
        "promotion_decision": promotion["decision"],
        "promote_to_default": promotion["promote_to_default"],
        "confidence_labels": confidence["allowed_labels"],
        "failure_categories": [row["category"] for row in failure_matrix["boundaries"]],
        "carried_regression_commands": CARRIED_REGRESSION_COMMANDS,
        "close_status": "closed" if not errors else "blocked",
        "report_path": _display_path(REPORT_PATH),
        "next_horizon": "real-local-parser-prototype",
    }


def render_markdown(gate: dict[str, Any]) -> str:
    lines = [
        f"# {gate['title']}",
        "",
        "> Scope: PTQ5 close gate for product trust and quality evidence.",
        "",
        "## One-Line Result",
        "",
        (
            "Product trust and quality evidence is ready to close: evidence inventory, confidence labels, failure boundaries, and promotion decision are connected."
            if gate["ok"]
            else "Product trust and quality evidence is not ready to close; fix listed errors."
        ),
        "",
        "## Close Status",
        "",
        f"- status: {gate['close_status']}",
        f"- promotion decision: `{gate['promotion_decision']}`",
        f"- promote to default: {gate['promote_to_default']}",
        f"- next horizon: `{gate['next_horizon']}`",
        "",
        "## Checks",
        "",
        "| Check | OK |",
        "|---|---|",
    ]
    for name, ok in gate["checks"].items():
        lines.append(f"| {name} | {ok} |")
    lines.extend(["", "## Failure Categories", ""])
    lines.extend(f"- {category}" for category in gate["failure_categories"])
    lines.extend(["", "## Required Reports", "", "| Report | Path | Exists |", "|---|---|---|"])
    for name, info in gate["reports"].items():
        lines.append(f"| {name} | `{info['path']}` | {info['exists']} |")
    lines.extend(["", "## Carried Regression Commands", ""])
    lines.extend(f"- `{command}`" for command in gate["carried_regression_commands"])
    lines.extend(["", "## Errors", ""])
    lines.extend(f"- {error}" for error in gate["errors"]) if gate["errors"] else lines.append("- none")
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
    gate = build_gate()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(gate), encoding="utf-8")
    return gate


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Run PTQ5 product trust and quality close gate.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    gate = write_report(args.out) if args.write else build_gate()
    if args.format == "json":
        print(json.dumps(gate, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(gate), end="")
    else:
        print(gate["title"])
        print(f"- ok: {gate['ok']}")
        print(f"- close status: {gate['close_status']}")
        print(f"- promotion decision: {gate['promotion_decision']}")
        print(f"- next horizon: {gate['next_horizon']}")
    return 0 if gate["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
