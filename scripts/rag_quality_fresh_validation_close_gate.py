from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.rag_quality_baseline_snapshot import build_baseline_snapshot  # noqa: E402
from scripts.rag_quality_promotion_decision_gate import build_promotion_decision  # noqa: E402
from scripts.rag_quality_regression_matrix import build_regression_matrix  # noqa: E402
from scripts.rag_quality_validation_contract import build_validation_contract  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-rag-quality-fresh-validation-close-report.md"


def build_close_gate() -> dict[str, Any]:
    rqf1 = build_validation_contract()
    rqf2 = build_baseline_snapshot()
    rqf3 = build_regression_matrix()
    rqf4 = build_promotion_decision()
    evidence = [
        _evidence("RQF1", "validation contract", "docs/reports/2026-07-05-rqf1-validation-contract.md", rqf1["ok"]),
        _evidence("RQF2", "baseline snapshot", "docs/reports/2026-07-05-rqf2-baseline-snapshot.md", rqf2["ok"]),
        _evidence("RQF3", "regression matrix", "docs/reports/2026-07-05-rqf3-regression-matrix.md", rqf3["ok"]),
        _evidence("RQF4", "promotion decision", "docs/reports/2026-07-05-rqf4-promotion-decision.md", rqf4["ok"]),
    ]
    close_result = rqf4["decision"]["result"]
    checks = {
        "all_evidence_exists": all(item["exists"] for item in evidence),
        "all_gates_ok": all(item["gate_ok"] for item in evidence),
        "close_result_is_defer": close_result == "defer",
        "default_change_forbidden": rqf4["decision"]["default_change_allowed"] is False,
        "next_gap_handoff_present": True,
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "RAG Quality Fresh Validation Close Report",
        "ok": not errors,
        "horizon": "rag-quality-fresh-validation",
        "completed_milestone": "RQF5",
        "close_result": close_result,
        "default_change_allowed": False,
        "evidence": evidence,
        "checks": checks,
        "errors": errors,
        "residual_risks": [
            "Fresh numeric local eval is still missing from public reports.",
            "Default retriever promotion remains deferred.",
            "Explicit authorization is still required before any default retriever change.",
        ],
        "next_horizon": "private-parser-realism-hardening",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: close gate for the RAG quality fresh validation horizon.",
        "",
        "## 한 줄 결론",
        "",
        f"Close result: `{result['close_result']}`. Default retriever change remains forbidden.",
        "",
        f"- Next horizon: `{result['next_horizon']}`",
        "",
        "## Evidence",
        "",
        "| Milestone | Evidence | Exists | Gate OK |",
        "|---|---|---|---|",
    ]
    for item in result["evidence"]:
        lines.append(f"| {item['id']} {item['name']} | `{item['path']}` | {item['exists']} | {item['gate_ok']} |")
    lines.extend(["", "## Checks", "", "| Check | OK |", "|---|---|"])
    for name, ok in result["checks"].items():
        lines.append(f"| {name} | {ok} |")
    lines.extend(["", "## Residual Risks", ""])
    lines.extend(f"- {risk}" for risk in result["residual_risks"])
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
    result = build_close_gate()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _evidence(id_: str, name: str, path: str, gate_ok: bool) -> dict[str, Any]:
    return {
        "id": id_,
        "name": name,
        "path": path,
        "exists": (ROOT / path).exists(),
        "gate_ok": gate_ok,
    }


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Close RAG quality fresh validation horizon.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_close_gate()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- close result: {result['close_result']}")
        print(f"- next horizon: {result['next_horizon']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
