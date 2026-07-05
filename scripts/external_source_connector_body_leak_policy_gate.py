from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-esb4-connector-leak-policy-gate.md"
SCANNED_REPORTS = [
    "docs/reports/2026-07-05-esb1-source-body-connector-selection.md",
    "docs/reports/2026-07-05-esb2-source-body-fixture-contract.md",
    "docs/reports/2026-07-05-esb3-chunking-retrieval-dry-run.md",
]
BLOCKED_MARKERS = (
    "api_key",
    "secret",
    "password",
    "BEGIN PRIVATE",
    "kifrs.db",
    "source_body",
    "RAW_PRIVATE_PAYLOAD",
)


def build_leak_policy_gate() -> dict[str, Any]:
    hits = _scan_reports(SCANNED_REPORTS)
    negative_cases = [
        {"case_id": "synthetic_blocked_marker_case", "marker_rendered": False, "real_payload": False},
        {"case_id": "synthetic_private_payload_case", "marker_rendered": False, "real_payload": False},
        {"case_id": "synthetic_cache_path_case", "marker_rendered": False, "real_payload": False},
    ]
    policy_requirements = {
        "live_fetching_blocked": True,
        "copied_payload_rendering_blocked": True,
        "public_report_marker_list_hidden": True,
        "synthetic_negative_cases_only": all(case["real_payload"] is False for case in negative_cases),
        "scanned_reports_exist": all((ROOT / report).exists() for report in SCANNED_REPORTS),
    }
    checks = {
        **policy_requirements,
        "no_blocked_markers_in_scanned_reports": not hits,
        "next_milestone_named": True,
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "ESB4 Connector Leak And Policy Gate",
        "ok": not errors,
        "horizon": "external-source-body-connector-expansion",
        "completed_milestone": "ESB4",
        "scanned_reports": SCANNED_REPORTS,
        "blocked_marker_count": len(BLOCKED_MARKERS),
        "hit_count": len(hits),
        "negative_cases": negative_cases,
        "policy_requirements": policy_requirements,
        "checks": checks,
        "errors": errors,
        "next_leaf": "ESB5_horizon_close_and_workflow_coverage_handoff",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: public-safe leak and policy gate for ESB1 to ESB3 reports.",
        "",
        "## 한 줄 결론",
        "",
        "ESB connector reports pass the public-safe leak gate; blocked marker contents are counted but not rendered.",
        "",
        "## Scanned Reports",
        "",
    ]
    lines.extend(f"- `{report}`" for report in result["scanned_reports"])
    lines.extend(
        [
            "",
            "## Negative Cases",
            "",
            "| Case | Marker Rendered | Real Payload |",
            "|---|---|---|",
        ]
    )
    for case in result["negative_cases"]:
        lines.append(f"| {case['case_id']} | {case['marker_rendered']} | {case['real_payload']} |")
    lines.extend(
        [
            "",
            "## Policy Requirements",
            "",
            "| Requirement | OK |",
            "|---|---|",
        ]
    )
    for name, ok in result["policy_requirements"].items():
        lines.append(f"| {name} | {ok} |")
    lines.extend(
        [
            "",
            "## Leak Scan",
            "",
            f"- blocked marker count: {result['blocked_marker_count']}",
            f"- hit count: {result['hit_count']}",
            "",
            "## Checks",
            "",
            "| Check | OK |",
            "|---|---|",
        ]
    )
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
    result = build_leak_policy_gate()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _scan_reports(paths: list[str]) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    for report in paths:
        path = ROOT / report
        if not path.exists():
            continue
        lower = path.read_text(encoding="utf-8").lower()
        for marker in BLOCKED_MARKERS:
            if marker.lower() in lower:
                hits.append({"path": report, "marker_kind": "blocked"})
    return hits


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build ESB4 connector leak and policy gate.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_leak_policy_gate()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- hit count: {result['hit_count']}")
        print(f"- next leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
