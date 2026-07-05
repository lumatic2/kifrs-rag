from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-rqf2-baseline-snapshot.md"


def build_baseline_snapshot() -> dict[str, Any]:
    evidence = [
        _evidence("validation_contract", "docs/reports/2026-07-05-rqf1-validation-contract.md"),
        _evidence("gap_audit", "docs/reports/2026-07-05-accounting-intelligence-gap-audit.md"),
        _evidence("default_guard", "docs/reports/2026-07-05-default-retriever-guard.md"),
        _evidence("previous_promotion_gate", "docs/reports/2026-07-05-runtime-retriever-promotion-gate-close-report.md"),
    ]
    baseline = {
        "default_retriever": "current_default_hybrid",
        "default_change_allowed": False,
        "fresh_numeric_eval_available_in_public_report": False,
        "public_safe_status": "baseline_contract_ready_numeric_eval_missing",
        "missing_local_evidence": [
            "fresh eval run against local K-IFRS DB",
            "fresh latency run on local retriever",
            "fresh regression comparison against opt-in retriever",
        ],
    }
    checks = {
        "all_required_evidence_exists": all(item["exists"] for item in evidence),
        "default_change_forbidden": baseline["default_change_allowed"] is False,
        "missing_local_evidence_recorded": len(baseline["missing_local_evidence"]) >= 3,
        "public_numeric_eval_not_faked": baseline["fresh_numeric_eval_available_in_public_report"] is False,
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "RQF2 Current Retriever Baseline Snapshot",
        "ok": not errors,
        "horizon": "rag-quality-fresh-validation",
        "completed_milestone": "RQF2",
        "baseline": baseline,
        "evidence": evidence,
        "checks": checks,
        "errors": errors,
        "next_leaf": "RQF3_opt_in_retriever_regression_matrix",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    baseline = result["baseline"]
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: public-safe baseline snapshot for the current default retriever.",
        "",
        "## 한 줄 결론",
        "",
        "The baseline contract is ready, but fresh numeric local eval evidence is not present in public reports; default retriever changes remain forbidden.",
        "",
        "## Baseline",
        "",
        f"- Default retriever: `{baseline['default_retriever']}`",
        f"- Default change allowed: {baseline['default_change_allowed']}",
        f"- Public fresh numeric eval available: {baseline['fresh_numeric_eval_available_in_public_report']}",
        f"- Status: `{baseline['public_safe_status']}`",
        "",
        "## Missing Local Evidence",
        "",
    ]
    lines.extend(f"- {item}" for item in baseline["missing_local_evidence"])
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
    result = build_baseline_snapshot()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _evidence(id_: str, path: str) -> dict[str, Any]:
    return {"id": id_, "path": path, "exists": (ROOT / path).exists()}


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build RQF2 current retriever baseline snapshot.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_baseline_snapshot()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- status: {result['baseline']['public_safe_status']}")
        print(f"- next leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
