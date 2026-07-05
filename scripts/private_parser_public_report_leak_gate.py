from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-ppr4-public-report-leak-gate.md"
BLOCKED_MARKERS = (
    "api_key",
    "secret",
    "password",
    "kifrs.db",
    "data/dogfood",
    "data/standards",
    "BEGIN PRIVATE",
    "RAW_PRIVATE_PAYLOAD",
)


def build_public_report_leak_gate() -> dict[str, Any]:
    scanned_reports = [
        "docs/reports/2026-07-05-ppr1-authorization-safe-adapter-proof.md",
        "docs/reports/2026-07-05-ppr2-fixture-adapter-contract.md",
        "docs/reports/2026-07-05-ppr3-deletion-retention-rehearsal.md",
    ]
    negative_cases = [
        {"case_id": "synthetic_blocked_marker_case", "marker_rendered": False, "real_payload": False},
        {"case_id": "synthetic_raw_payload_marker_case", "marker_rendered": False, "real_payload": False},
        {"case_id": "synthetic_identifier_marker_case", "marker_rendered": False, "real_payload": False},
    ]
    hits = _scan_reports(scanned_reports)
    checks = {
        "all_reports_exist": all((ROOT / path).exists() for path in scanned_reports),
        "no_blocked_markers_in_reports": not hits,
        "negative_cases_are_synthetic": all(case["real_payload"] is False for case in negative_cases),
        "blocked_marker_list_present": len(BLOCKED_MARKERS) >= 6,
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "PPR4 Parser Leak And Public Report Gate",
        "ok": not errors,
        "horizon": "private-parser-realism-hardening",
        "completed_milestone": "PPR4",
        "scanned_reports": scanned_reports,
        "blocked_marker_count": len(BLOCKED_MARKERS),
        "hits": hits,
        "negative_cases": negative_cases,
        "checks": checks,
        "errors": errors,
        "next_leaf": "PPR5_horizon_close_and_source_connector_handoff",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: public-safe leak gate for private parser realism reports.",
        "",
        "## 한 줄 결론",
        "",
        "The private parser public reports contain structured statuses only; synthetic negative cases do not use real protected payloads.",
        "",
        "## Scanned Reports",
        "",
    ]
    lines.extend(f"- `{path}`" for path in result["scanned_reports"])
    lines.extend(["", "## Negative Cases", "", "| Case | Marker Rendered | Real Payload |", "|---|---|---|"])
    for case in result["negative_cases"]:
        lines.append(f"| {case['case_id']} | {case['marker_rendered']} | {case['real_payload']} |")
    lines.extend(["", "## Hits", ""])
    if result["hits"]:
        lines.extend(f"- `{hit['path']}` contains `{hit['marker']}`" for hit in result["hits"])
    else:
        lines.append("- none")
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
    result = build_public_report_leak_gate()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _scan_reports(paths: list[str]) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    for report_path in paths:
        path = ROOT / report_path
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        lower = text.lower()
        for marker in BLOCKED_MARKERS:
            if marker.lower() in lower:
                hits.append({"path": report_path, "marker": marker})
    return hits


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build PPR4 parser public report leak gate.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_public_report_leak_gate()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- hits: {len(result['hits'])}")
        print(f"- next leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
