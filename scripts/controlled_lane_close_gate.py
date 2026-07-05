from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-source-body-ingestion-controlled-lane-close-report.md"
REQUIRED_REPORTS = {
    "sbi1_source_selection": ROOT / "docs" / "reports" / "2026-07-05-sbi1-source-class-selection.md",
    "sbi2_policy_record": ROOT / "docs" / "reports" / "2026-07-05-sbi2-source-body-policy-record.md",
    "sbi3_parser_chunker": ROOT / "docs" / "reports" / "2026-07-05-sbi3-synthetic-body-parser-chunker.md",
    "sbi4_retrieval_gate": ROOT / "docs" / "reports" / "2026-07-05-sbi4-controlled-lane-retrieval-gate.md",
    "product_trust_close": ROOT / "docs" / "reports" / "2026-07-05-product-trust-quality-close-report.md",
}


def build_controlled_lane_close_gate() -> dict[str, Any]:
    from scripts.controlled_lane_retrieval_gate import build_controlled_lane_retrieval_gate
    from scripts.product_trust_quality_gate import build_gate as build_product_trust_gate
    from scripts.source_class_selection import build_source_class_selection
    from scripts.source_policy_record import build_source_policy_record
    from scripts.synthetic_body_parser_chunker import build_synthetic_body_parser_chunker

    sbi1 = build_source_class_selection()
    sbi2 = build_source_policy_record()
    sbi3 = build_synthetic_body_parser_chunker()
    sbi4 = build_controlled_lane_retrieval_gate()
    product_trust = build_product_trust_gate()
    reports = {
        name: {"path": _display_path(path), "exists": path.exists()}
        for name, path in REQUIRED_REPORTS.items()
    }
    missing_reports = [name for name, info in reports.items() if not info["exists"]]
    checks = {
        "sbi1_source_selection": sbi1["ok"],
        "sbi2_policy_record": sbi2["ok"],
        "sbi3_parser_chunker": sbi3["ok"],
        "sbi4_retrieval_gate": sbi4["ok"],
        "product_trust_close": product_trust["ok"],
        "synthetic_only_boundary": sbi2["policy"]["storage_mode"] == "synthetic_body_only",
        "primary_evidence_preserved": sbi4["primary_evidence_preserved"],
        "all_required_reports_present": not missing_reports,
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "Source Body Ingestion Controlled Lane Close Gate",
        "ok": not errors,
        "horizon": "source-body-ingestion-controlled-lane",
        "completed_milestone": "SBI5",
        "close_status": "closed" if not errors else "blocked",
        "checks": checks,
        "errors": errors,
        "reports": reports,
        "missing_reports": missing_reports,
        "selected_source_class": sbi1["selected_source_class"],
        "implementation_mode": sbi1["implementation_mode"],
        "chunk_count": sbi3["chunk_count"],
        "retrieved_count": sbi4["retrieved_count"],
        "still_not_implemented": [
            "live external body fetch",
            "external body cache",
            "external body embeddings",
            "default retriever change",
            "primary evidence override",
        ],
        "carried_regression_commands": [
            "python -m pytest tests\\test_source_class_selection.py tests\\test_source_policy_record.py tests\\test_synthetic_body_parser_chunker.py tests\\test_controlled_lane_retrieval_gate.py tests\\test_controlled_lane_close_gate.py -q",
            "python scripts\\product_trust_quality_gate.py --format text",
        ],
        "next_horizon": "workflow-coverage-expansion",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(gate: dict[str, Any]) -> str:
    lines = [
        f"# {gate['title']}",
        "",
        "> Scope: SBI5 close gate for the controlled non-IFRS source-body lane.",
        "",
        "## 한 줄 결론",
        "",
        (
            "The controlled source-body lane is closed as a synthetic-only interpretive lane: source class, policy, chunks, retrieval role, and product trust evidence are connected."
            if gate["ok"]
            else "The controlled source-body lane is blocked; fix the listed checks."
        ),
        "",
        "## Close Status",
        "",
        f"- status: {gate['close_status']}",
        f"- selected source class: `{gate['selected_source_class']}`",
        f"- implementation mode: `{gate['implementation_mode']}`",
        f"- chunk count: {gate['chunk_count']}",
        f"- retrieved count: {gate['retrieved_count']}",
        f"- next horizon: `{gate['next_horizon']}`",
        "",
        "## Checks",
        "",
        "| Check | OK |",
        "|---|---|",
    ]
    for name, ok in gate["checks"].items():
        lines.append(f"| {name} | {ok} |")
    lines.extend(["", "## Required Reports", "", "| Report | Path | Exists |", "|---|---|---|"])
    for name, info in gate["reports"].items():
        lines.append(f"| {name} | `{info['path']}` | {info['exists']} |")
    lines.extend(["", "## Still Not Implemented", ""])
    lines.extend(f"- {item}" for item in gate["still_not_implemented"])
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
    gate = build_controlled_lane_close_gate()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(gate), encoding="utf-8")
    return gate


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Run SBI5 controlled lane close gate.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    gate = write_report(args.out) if args.write else build_controlled_lane_close_gate()
    if args.format == "json":
        print(json.dumps(gate, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(gate), end="")
    else:
        print(gate["title"])
        print(f"- ok: {gate['ok']}")
        print(f"- close status: {gate['close_status']}")
        print(f"- next horizon: {gate['next_horizon']}")
        for error in gate["errors"]:
            print(f"- {error}")
    return 0 if gate["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
