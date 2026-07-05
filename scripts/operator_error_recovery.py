from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-oeh4-error-recovery-playbook.md"


def build_operator_error_recovery() -> dict[str, Any]:
    cases = [
        _case(
            "pytest_failure",
            "A milestone test fails.",
            "Read the failing assertion, rerun only the named test, then rerun the milestone script with --write.",
            "python -m pytest <failing-test> -q",
        ),
        _case(
            "missing_report",
            "A required public report is missing from doctor or manifest.",
            "Run the producing command from OEH1 inventory or the hint shown by OEH2 doctor.",
            "python scripts\\operator_run_doctor.py --format text --write",
        ),
        _case(
            "default_retriever_guard_failure",
            "Default retriever guard fails or target retriever is exposed too early.",
            "Restore default mode expectation to hybrid and keep promotion deferred until RPG close gate is updated.",
            "python scripts\\default_retriever_guard.py --format text",
        ),
        _case(
            "protected_data_warning",
            "A report or manifest appears to reference protected private/source data.",
            "Remove protected references from public report surfaces and rerun the relevant public-safe test.",
            "python -m pytest tests\\test_operator_run_doctor.py tests\\test_operator_report_manifest.py -q",
        ),
        _case(
            "navigation_drift",
            "Progress map or manifest points to a stale next leaf.",
            "Regenerate progress map and report manifest, then rerun their tests.",
            "python scripts\\accounting_intelligence_progress_map.py --format text --write",
        ),
    ]
    checks = {
        "cases_present": len(cases) >= 5,
        "rerun_commands_present": all(item["rerun_command"] for item in cases),
        "no_destructive_recovery": all("git reset" not in item["remediation"].lower() and "delete" not in item["remediation"].lower() for item in cases),
        "protected_boundary_case_present": any(item["case_id"] == "protected_data_warning" for item in cases),
        "retriever_guard_case_present": any(item["case_id"] == "default_retriever_guard_failure" for item in cases),
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "OEH4 Error Recovery Playbook",
        "ok": not errors,
        "horizon": "operator-experience-hardening",
        "completed_milestone": "OEH4",
        "cases": cases,
        "checks": checks,
        "errors": errors,
        "next_gate": "operator_experience_close_gate",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: local operator recovery cases and rerun commands.",
        "",
        "## 한 줄 결론",
        "",
        "Common failures now point to specific rerun or remediation commands without destructive cleanup.",
        "",
        "## Recovery Cases",
        "",
        "| Case | Symptom | Remediation | Rerun Command |",
        "|---|---|---|---|",
    ]
    for item in result["cases"]:
        lines.append(
            f"| {item['case_id']} | {item['symptom']} | {item['remediation']} | `{item['rerun_command']}` |"
        )
    lines.extend(["", "## Checks", "", "| Check | OK |", "|---|---|"])
    for name, ok in result["checks"].items():
        lines.append(f"| {name} | {ok} |")
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
    result = build_operator_error_recovery()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _case(case_id: str, symptom: str, remediation: str, rerun_command: str) -> dict[str, str]:
    return {
        "case_id": case_id,
        "symptom": symptom,
        "remediation": remediation,
        "rerun_command": rerun_command,
    }


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build OEH4 operator error recovery playbook.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_operator_error_recovery()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- cases: {len(result['cases'])}")
        print(f"- next gate: {result['next_gate']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
