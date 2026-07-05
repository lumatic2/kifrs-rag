from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-operator-experience-hardening-close-report.md"
REQUIRED_REPORTS = {
    "oeh1_command_inventory": ROOT / "docs" / "reports" / "2026-07-05-oeh1-operator-command-inventory.md",
    "oeh2_run_doctor": ROOT / "docs" / "reports" / "2026-07-05-oeh2-run-doctor.md",
    "oeh3_report_manifest": ROOT / "docs" / "reports" / "2026-07-05-oeh3-report-manifest.md",
    "oeh4_error_recovery": ROOT / "docs" / "reports" / "2026-07-05-oeh4-error-recovery-playbook.md",
    "retriever_close": ROOT / "docs" / "reports" / "2026-07-05-runtime-retriever-promotion-gate-close-report.md",
}


def build_operator_experience_close_gate() -> dict[str, Any]:
    payloads = {name: _load_report_payload(path) for name, path in REQUIRED_REPORTS.items()}
    reports = {
        name: {"path": _display_path(path), "exists": path.exists()}
        for name, path in REQUIRED_REPORTS.items()
    }
    missing_reports = [name for name, info in reports.items() if not info["exists"]]
    parse_errors = [
        error
        for info in payloads.values()
        for error in info.get("errors", [])
    ]
    oeh1 = payloads["oeh1_command_inventory"].get("payload", {})
    oeh2 = payloads["oeh2_run_doctor"].get("payload", {})
    oeh3 = payloads["oeh3_report_manifest"].get("payload", {})
    oeh4 = payloads["oeh4_error_recovery"].get("payload", {})
    checks = {
        "command_discovery_ok": oeh1.get("ok") is True and len(oeh1.get("commands", [])) >= 5,
        "run_doctor_ok": oeh2.get("ok") is True,
        "report_manifest_ok": oeh3.get("ok") is True and len(oeh3.get("entries", [])) >= 5,
        "error_recovery_ok": oeh4.get("ok") is True and len(oeh4.get("cases", [])) >= 5,
        "protected_boundary_carried": oeh2.get("protected_boundaries", {}).get("public_reports_only") is True,
        "all_required_reports_present": not missing_reports,
        "reports_parseable": not parse_errors,
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    errors.extend(parse_errors)
    return {
        "title": "Operator Experience Hardening Close Gate",
        "ok": not errors,
        "horizon": "operator-experience-hardening",
        "completed_milestone": "OEH5",
        "close_status": "closed" if not errors else "blocked",
        "operator_capabilities": [
            "discover commands by goal",
            "run environment/report doctor",
            "navigate reports in order",
            "recover common failures with rerun commands",
        ],
        "checks": checks,
        "errors": errors,
        "reports": reports,
        "missing_reports": missing_reports,
        "product_weakness_queue_status": "closed",
        "next_horizon": "none",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: OEH5 close gate for local operator experience hardening.",
        "",
        "## 한 줄 결론",
        "",
        "Operator experience hardening is closed: the local operator can discover, run, verify, navigate, and recover the toolkit through public-safe surfaces.",
        "",
        "## Close Status",
        "",
        f"- status: `{result['close_status']}`",
        f"- product weakness queue: `{result['product_weakness_queue_status']}`",
        f"- next horizon: `{result['next_horizon']}`",
        "",
        "## Operator Capabilities",
        "",
    ]
    lines.extend(f"- {item}" for item in result["operator_capabilities"])
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
            json.dumps(result, ensure_ascii=False, indent=2),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH) -> dict[str, Any]:
    result = build_operator_experience_close_gate()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _load_report_payload(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"payload": {}, "errors": [f"missing report: {_display_path(path)}"]}
    text = path.read_text(encoding="utf-8")
    marker_index = text.find("## Machine Result")
    fenced_start = text.find("```json", marker_index)
    if marker_index == -1 or fenced_start == -1:
        return {"payload": {}, "errors": [f"missing Machine Result: {_display_path(path)}"]}
    json_start = text.find("\n", fenced_start)
    fenced_end = text.find("```", json_start + 1)
    if json_start == -1 or fenced_end == -1:
        return {"payload": {}, "errors": [f"invalid Machine Result fence: {_display_path(path)}"]}
    try:
        return {"payload": json.loads(text[json_start:fenced_end].strip()), "errors": []}
    except json.JSONDecodeError as exc:
        return {"payload": {}, "errors": [f"invalid Machine Result json: {_display_path(path)}: {exc}"]}


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Run OEH5 operator experience close gate.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_operator_experience_close_gate()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- close status: {result['close_status']}")
        print(f"- product weakness queue: {result['product_weakness_queue_status']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
