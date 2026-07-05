from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-runtime-retriever-promotion-gate-close-report.md"
REQUIRED_REPORTS = {
    "rpg1_evidence_inventory": ROOT / "docs" / "reports" / "2026-07-05-rpg1-promotion-evidence-inventory.md",
    "rpg2_regression_latency": ROOT / "docs" / "reports" / "2026-07-05-rpg2-regression-latency-gate.md",
    "rpg3_rollback_policy": ROOT / "docs" / "reports" / "2026-07-05-rpg3-failure-rollback-policy.md",
    "rpg4_operator_command": ROOT / "docs" / "reports" / "2026-07-05-rpg4-operator-promotion-command.md",
}


def build_runtime_retriever_promotion_close_gate() -> dict[str, Any]:
    payloads = {name: _load_report_payload(path) for name, path in REQUIRED_REPORTS.items()}
    rpg1 = payloads["rpg1_evidence_inventory"].get("payload", {})
    rpg2 = payloads["rpg2_regression_latency"].get("payload", {})
    rpg3 = payloads["rpg3_rollback_policy"].get("payload", {})
    rpg4 = payloads["rpg4_operator_command"].get("payload", {})
    reports = {
        name: {"path": _display_path(path), "exists": path.exists()}
        for name, path in REQUIRED_REPORTS.items()
    }
    missing_reports = [name for name, info in reports.items() if not info["exists"]]
    close_result = "defer"
    parse_errors = [
        error
        for info in payloads.values()
        for error in info.get("errors", [])
    ]
    checks = {
        "rpg1_inventory_ok": rpg1.get("ok") is True,
        "rpg2_gate_ok": rpg2.get("ok") is True,
        "rpg3_policy_ok": rpg3.get("ok") is True,
        "rpg4_command_ok": rpg4.get("ok") is True,
        "close_result_explicit": close_result in {"promote", "defer", "block"},
        "rollback_evidence_present": rpg3.get("policy", {}).get("safe_fallback") == "hybrid",
        "operator_command_dry_run": rpg4.get("command_output", {}).get("mutates_runtime") is False,
        "default_not_changed": rpg4.get("command_output", {}).get("current_default") == "hybrid",
        "reports_parseable": not parse_errors,
        "all_required_reports_present": not missing_reports,
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    errors.extend(parse_errors)
    return {
        "title": "Runtime Retriever Promotion Gate Close Report",
        "ok": not errors,
        "horizon": "runtime-retriever-promotion-gate",
        "completed_milestone": "RPG5",
        "close_status": "closed" if not errors else "blocked",
        "close_result": close_result,
        "reason": "promotion remains deferred because latency/cost evidence is missing and current default guard keeps the repair retriever opt-in",
        "target_retriever": rpg1.get("target_retriever", "unknown"),
        "current_default": rpg1.get("current_default", "unknown"),
        "checks": checks,
        "errors": errors,
        "reports": reports,
        "missing_reports": missing_reports,
        "rollback": rpg3.get("policy", {}),
        "next_horizon": "operator-experience-hardening",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: RPG5 close gate for runtime retriever promotion.",
        "",
        "## 한 줄 결론",
        "",
        "Runtime retriever promotion closes as `defer`: the opt-in repair retriever stays available for evaluation, while runtime default remains `hybrid` until latency/cost evidence exists.",
        "",
        "## Close Result",
        "",
        f"- close status: `{result['close_status']}`",
        f"- close result: `{result['close_result']}`",
        f"- reason: {result['reason']}",
        f"- target retriever: `{result['target_retriever']}`",
        f"- current default: `{result['current_default']}`",
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
    lines.extend(["", "## Rollback Summary", ""])
    lines.extend(
        [
            f"- safe fallback: `{result['rollback']['safe_fallback']}`",
            f"- target retriever: `{result['rollback']['target_retriever']}`",
            f"- current default: `{result['rollback']['current_default']}`",
        ]
    )
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
    result = build_runtime_retriever_promotion_close_gate()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _load_report_payload(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"payload": {}, "errors": [f"missing report: {_display_path(path)}"]}
    text = path.read_text(encoding="utf-8")
    marker = "## Machine Result"
    marker_index = text.find(marker)
    if marker_index == -1:
        return {"payload": {}, "errors": [f"missing Machine Result: {_display_path(path)}"]}
    fenced_start = text.find("```json", marker_index)
    if fenced_start == -1:
        return {"payload": {}, "errors": [f"missing Machine Result json fence: {_display_path(path)}"]}
    json_start = text.find("\n", fenced_start)
    fenced_end = text.find("```", json_start + 1)
    if json_start == -1 or fenced_end == -1:
        return {"payload": {}, "errors": [f"invalid Machine Result fence: {_display_path(path)}"]}
    try:
        return {"payload": json.loads(text[json_start:fenced_end].strip()), "errors": []}
    except json.JSONDecodeError as exc:
        return {"payload": {}, "errors": [f"invalid Machine Result json: {_display_path(path)}: {exc}"]}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run RPG5 runtime retriever promotion close gate.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_runtime_retriever_promotion_close_gate()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
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
