from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.e2e_demo_packet_builder import PACKET_PATH, REPORT_PATH as PACKET_REPORT_PATH, build_demo_packet  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-e2e4-demo-smoke-gate.md"
BLOCKED_TERMS = ("api_key", "token", "secret", "password", "kifrs.db", "data/dogfood", "data/standards")


def build_demo_smoke_gate(items: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    packet = build_demo_packet()
    packet_items = items if items is not None else packet["items"]
    missing_reports = [item["report"] for item in packet_items if not (ROOT / item["report"]).exists()]
    packet_texts = _read_existing_texts([PACKET_PATH, PACKET_REPORT_PATH])
    blocked_hits = _blocked_hits(packet_texts)
    checks = {
        "packet_index_exists": PACKET_PATH.exists(),
        "packet_report_exists": PACKET_REPORT_PATH.exists(),
        "all_packet_reports_exist": not missing_reports,
        "all_commands_present": all(item.get("command") for item in packet_items),
        "all_commands_local_scripts": all(str(item.get("command", "")).startswith("python scripts\\") for item in packet_items),
        "all_recovery_hints_present": all(item.get("recovery") for item in packet_items),
        "packet_surface_public_safe": not blocked_hits,
        "missing_report_failure_path_present": bool(_missing_report_failure_path(missing_reports)),
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "E2E4 Demo Smoke And Navigation Gate",
        "ok": not errors,
        "horizon": "end-to-end-demo-scenario",
        "completed_milestone": "E2E4",
        "packet_path": _display_path(PACKET_PATH),
        "packet_report_path": _display_path(PACKET_REPORT_PATH),
        "checks": checks,
        "errors": errors,
        "missing_reports": missing_reports,
        "blocked_hits": blocked_hits,
        "failure_path": _missing_report_failure_path(missing_reports),
        "next_leaf": "E2E5_horizon_close_gate",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: smoke gate for the end-to-end demo packet navigation surface.",
        "",
        "## 한 줄 결론",
        "",
        "The demo packet is navigable and public-safe when every check is true.",
        "",
        f"- Packet: `{result['packet_path']}`",
        f"- Packet build report: `{result['packet_report_path']}`",
        "",
        "## Checks",
        "",
        "| Check | OK |",
        "|---|---|",
    ]
    for name, ok in result["checks"].items():
        lines.append(f"| {name} | {ok} |")
    lines.extend(["", "## Missing Reports", ""])
    lines.extend(f"- `{path}`" for path in result["missing_reports"]) if result["missing_reports"] else lines.append("- none")
    lines.extend(["", "## Failure Path", ""])
    lines.append(result["failure_path"])
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
    result = build_demo_smoke_gate()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _read_existing_texts(paths: list[Path]) -> dict[str, str]:
    return {_display_path(path): path.read_text(encoding="utf-8") for path in paths if path.exists()}


def _blocked_hits(texts: dict[str, str]) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    for path, text in texts.items():
        lower = text.lower()
        for term in BLOCKED_TERMS:
            if term in lower:
                hits.append({"path": path, "term": term})
    return hits


def _missing_report_failure_path(missing_reports: list[str]) -> str:
    if not missing_reports:
        return "No missing reports. If a report disappears, rerun the command listed for that packet row and rerun this smoke gate."
    missing = ", ".join(missing_reports)
    return f"Missing report(s): {missing}. Rerun the matching packet command, then rerun E2E3 packet builder and E2E4 smoke gate."


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Run E2E4 demo smoke and navigation gate.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_demo_smoke_gate()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- packet: {result['packet_path']}")
        print(f"- next leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
