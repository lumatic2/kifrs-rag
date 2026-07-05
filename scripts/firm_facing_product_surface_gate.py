from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.firm_facing_operator_demo_command import build_demo_packet  # noqa: E402
from scripts.firm_facing_product_narrative import build_narrative_check  # noqa: E402
from scripts.firm_facing_readiness_checklist import build_readiness  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-firm-facing-product-surface-close-report.md"

REQUIRED_REPORTS = {
    "fps1_inventory": ROOT / "docs" / "reports" / "2026-07-05-fps1-product-surface-inventory.md",
    "fps2_operator_demo": ROOT / "docs" / "reports" / "2026-07-05-fps2-operator-demo-command.md",
    "fps3_readiness": ROOT / "docs" / "reports" / "2026-07-05-fps3-readiness-checklist.md",
    "fps4_narrative": ROOT / "docs" / "reports" / "2026-07-05-fps4-product-narrative.md",
    "multi_authority_runtime": ROOT / "docs" / "reports" / "2026-07-05-multi-authority-runtime-hardening-close-report.md",
    "client_private_parser_runtime": ROOT / "docs" / "reports" / "2026-07-05-client-private-parser-runtime-close-report.md",
    "rag_quality_refresh": ROOT / "docs" / "reports" / "2026-07-05-rag-quality-refresh-close-report.md",
    "default_retriever_guard": ROOT / "docs" / "reports" / "2026-07-05-default-retriever-guard.md",
}

CARRIED_REGRESSION_COMMANDS = [
    "python scripts\\quality_preflight.py --format text",
    "python scripts\\rag_quality_final_gate.py --format text",
    "python scripts\\default_retriever_guard.py --format text",
    "python scripts\\multi_authority_runtime_gate.py --format text",
    "python scripts\\client_private_parser_runtime_gate.py --format text",
]


def build_gate() -> dict[str, Any]:
    demo = build_demo_packet()
    readiness = build_readiness()
    narrative = build_narrative_check()
    reports = {
        name: {
            "path": _display_path(path),
            "exists": path.exists(),
        }
        for name, path in REQUIRED_REPORTS.items()
    }
    missing_reports = [name for name, info in reports.items() if not info["exists"]]
    errors: list[str] = []
    if not demo["ok"]:
        errors.append("FPS2 operator demo packet failed")
    if not readiness["ok"]:
        errors.append("FPS3 readiness checklist failed")
    if not narrative["ok"]:
        errors.append("FPS4 product narrative failed")
    if missing_reports:
        errors.append(f"missing reports: {missing_reports}")
    if not _public_safe(demo["review_pack_markdown"]):
        errors.append("demo walkthrough is not public-safe")

    return {
        "title": "Firm-Facing Product Surface Close Gate",
        "ok": not errors,
        "horizon": "firm-facing-product-surface",
        "milestone": "FPS5",
        "checks": {
            "fps2_operator_demo": demo["ok"],
            "fps3_readiness": readiness["ok"],
            "fps4_narrative": narrative["ok"],
            "all_required_reports_present": not missing_reports,
            "public_safe": _public_safe(demo["review_pack_markdown"]),
        },
        "reports": reports,
        "missing_reports": missing_reports,
        "errors": errors,
        "demo_flow": demo["demo_flow"],
        "verification_status": demo["verification_status"],
        "carried_regression_commands": CARRIED_REGRESSION_COMMANDS,
        "close_status": "closed" if not errors else "blocked",
        "report_path": _display_path(REPORT_PATH),
        "next_horizon": "none; horizon order is exhausted in ROADMAP",
    }


def render_markdown(gate: dict[str, Any]) -> str:
    lines = [
        f"# {gate['title']}",
        "",
        "> Scope: FPS5 close gate for the firm-facing local product surface horizon.",
        "",
        "## One-Line Result",
        "",
        (
            "Firm-facing product surface is ready to close: demo command, readiness checklist, README narrative, and carried evidence reports are connected."
            if gate["ok"]
            else "Firm-facing product surface is not ready to close; fix the listed errors."
        ),
        "",
        "## Close Status",
        "",
        f"- status: {gate['close_status']}",
        f"- horizon: `{gate['horizon']}`",
        f"- demo flow: `{gate['demo_flow']['id']}`",
        "",
        "## Checks",
        "",
        "| Check | OK |",
        "|---|---|",
    ]
    for name, ok in gate["checks"].items():
        lines.append(f"| {name} | {ok} |")
    lines.extend(
        [
            "",
            "## Verification Status",
            "",
            "| Verification | OK |",
            "|---|---|",
        ]
    )
    for name, ok in gate["verification_status"].items():
        lines.append(f"| {name} | {ok} |")
    lines.extend(
        [
            "",
            "## Required Reports",
            "",
            "| Report | Path | Exists |",
            "|---|---|---|",
        ]
    )
    for name, info in gate["reports"].items():
        lines.append(f"| {name} | `{info['path']}` | {info['exists']} |")
    lines.extend(["", "## Carried Regression Commands", ""])
    lines.extend(f"- `{command}`" for command in gate["carried_regression_commands"])
    lines.extend(["", "## Errors", ""])
    lines.extend(f"- {error}" for error in gate["errors"]) if gate["errors"] else lines.append("- none")
    lines.extend(
        [
            "",
            "## Product Meaning",
            "",
            "The repo now has a firm-side operator surface for the current proof: a single 1116 walkthrough command, local readiness checklist, README narrative, and close gate tying runtime/RAG evidence together.",
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps(gate, ensure_ascii=False, indent=2, default=str),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH) -> dict[str, Any]:
    gate = build_gate()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(gate), encoding="utf-8")
    return gate


def _public_safe(text: str) -> bool:
    lowered = text.lower()
    forbidden = ("api_key", "source_body", "full_text", "raw_xml", "xbrl_dump", "secret")
    return not any(item in lowered for item in forbidden)


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the FPS5 firm-facing product surface close gate.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    gate = write_report(args.out) if args.write else build_gate()
    if args.format == "json":
        print(json.dumps(gate, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(gate), end="")
    else:
        print(gate["title"])
        print(f"- ok: {gate['ok']}")
        print(f"- close status: {gate['close_status']}")
        print(f"- missing reports: {gate['missing_reports']}")
        print(f"- next horizon: {gate['next_horizon']}")
    return 0 if gate["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
