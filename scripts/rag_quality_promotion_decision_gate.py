from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-rqf4-promotion-decision.md"


def build_promotion_decision() -> dict[str, Any]:
    evidence = [
        _evidence("validation_contract", "docs/reports/2026-07-05-rqf1-validation-contract.md"),
        _evidence("baseline_snapshot", "docs/reports/2026-07-05-rqf2-baseline-snapshot.md"),
        _evidence("regression_matrix", "docs/reports/2026-07-05-rqf3-regression-matrix.md"),
        _evidence("default_guard", "docs/reports/2026-07-05-default-retriever-guard.md"),
    ]
    blockers = [
        "fresh numeric baseline eval missing",
        "fresh opt-in regression comparison missing",
        "fresh latency comparison missing",
        "explicit authorization missing",
    ]
    decision = {
        "result": "defer",
        "default_change_allowed": False,
        "rollback_required_if_later_promoted": True,
        "reason": "Promotion is not allowed because fresh numeric evidence and explicit authorization are missing.",
    }
    checks = {
        "all_evidence_exists": all(item["exists"] for item in evidence),
        "decision_is_valid": decision["result"] in {"promote", "defer", "rollback", "blocked"},
        "default_change_forbidden": decision["default_change_allowed"] is False,
        "blockers_present": len(blockers) >= 4,
        "rollback_requirement_present": decision["rollback_required_if_later_promoted"] is True,
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "RQF4 Promotion Decision Gate",
        "ok": not errors,
        "horizon": "rag-quality-fresh-validation",
        "completed_milestone": "RQF4",
        "decision": decision,
        "blockers": blockers,
        "evidence": evidence,
        "checks": checks,
        "errors": errors,
        "next_leaf": "RQF5_horizon_close_and_next_gap_handoff",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    decision = result["decision"]
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: promote/defer/rollback decision for RAG default retriever status.",
        "",
        "## 한 줄 결론",
        "",
        f"Decision: `{decision['result']}`. {decision['reason']}",
        "",
        "## Decision",
        "",
        f"- Result: `{decision['result']}`",
        f"- Default change allowed: {decision['default_change_allowed']}",
        f"- Rollback required if later promoted: {decision['rollback_required_if_later_promoted']}",
        "",
        "## Blockers",
        "",
    ]
    lines.extend(f"- {item}" for item in result["blockers"])
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
    result = build_promotion_decision()
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
    parser = argparse.ArgumentParser(description="Build RQF4 RAG promotion decision gate.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_promotion_decision()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- decision: {result['decision']['result']}")
        print(f"- next leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
