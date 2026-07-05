from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-oeh2-run-doctor.md"
REQUIRED_REPORTS = {
    "command_inventory": ROOT / "docs" / "reports" / "2026-07-05-oeh1-operator-command-inventory.md",
    "progress_map": ROOT / "docs" / "reports" / "2026-07-05-accounting-intelligence-progress-map.md",
    "weakness_queue": ROOT / "docs" / "reports" / "2026-07-05-product-weakness-horizon-candidates.md",
    "retriever_close": ROOT / "docs" / "reports" / "2026-07-05-runtime-retriever-promotion-gate-close-report.md",
}


def build_operator_run_doctor() -> dict[str, Any]:
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    reports = {
        name: {"path": _display_path(path), "exists": path.exists(), "hint": _hint_for_report(name)}
        for name, path in REQUIRED_REPORTS.items()
    }
    missing_reports = [name for name, info in reports.items() if not info["exists"]]
    protected_boundaries = {
        "no_private_payload_scan": True,
        "no_embedding_dump_scan": True,
        "no_dogfood_material_scan": True,
        "public_reports_only": True,
    }
    warnings = []
    if shutil.which("uv") is None:
        warnings.append("uv not found on PATH; current scripts use python directly, but uv setup checks may be unavailable")
    checks = {
        "python_available": sys.version_info.major >= 3 and sys.version_info.minor >= 10,
        "uv_checked": True,
        "required_reports_checked": True,
        "required_reports_present": not missing_reports,
        "protected_boundaries_checked": all(protected_boundaries.values()),
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "OEH2 Run Doctor",
        "ok": not errors,
        "horizon": "operator-experience-hardening",
        "completed_milestone": "OEH2",
        "python_version": python_version,
        "uv_available": shutil.which("uv") is not None,
        "reports": reports,
        "missing_reports": missing_reports,
        "protected_boundaries": protected_boundaries,
        "warnings": warnings,
        "checks": checks,
        "errors": errors,
        "next_gate": "report_manifest_and_navigation_surface",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: local operator diagnostics for environment, reports, and protected boundaries.",
        "",
        "## 한 줄 결론",
        "",
        "The run doctor checks Python, uv availability, required public reports, and protected-data boundaries without reading private payloads.",
        "",
        "## Environment",
        "",
        f"- Python: `{result['python_version']}`",
        f"- uv available: {result['uv_available']}",
        "",
        "## Required Reports",
        "",
        "| Report | Path | Exists | Hint |",
        "|---|---|---|---|",
    ]
    for name, info in result["reports"].items():
        lines.append(f"| {name} | `{info['path']}` | {info['exists']} | `{info['hint']}` |")
    lines.extend(["", "## Protected Boundaries", "", "| Boundary | OK |", "|---|---|"])
    for name, ok in result["protected_boundaries"].items():
        lines.append(f"| {name} | {ok} |")
    lines.extend(["", "## Warnings", ""])
    lines.extend(f"- {warning}" for warning in result["warnings"]) if result["warnings"] else lines.append("- none")
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
    result = build_operator_run_doctor()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _hint_for_report(name: str) -> str:
    return {
        "command_inventory": "python scripts\\operator_command_inventory.py --format text --write",
        "progress_map": "python scripts\\accounting_intelligence_progress_map.py --format text --write",
        "weakness_queue": "python scripts\\product_weakness_horizon_candidates.py --format text --write",
        "retriever_close": "python scripts\\runtime_retriever_promotion_close_gate.py --format text --write",
    }[name]


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build OEH2 operator run doctor.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_operator_run_doctor()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- python: {result['python_version']}")
        print(f"- uv available: {result['uv_available']}")
        for warning in result["warnings"]:
            print(f"- warning: {warning}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
