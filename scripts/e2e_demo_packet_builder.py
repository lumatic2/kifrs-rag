from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / "docs" / "reports" / "end-to-end-demo" / "INDEX.md"
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-e2e3-demo-packet-builder.md"


def build_demo_packet() -> dict[str, Any]:
    packet_items = [
        _packet_item(
            order=0,
            section="start",
            title="Current Position",
            report="docs/reports/2026-07-05-accounting-intelligence-progress-map.md",
            command="python scripts\\accounting_intelligence_progress_map.py --format text --write",
            purpose="Orient the operator to the active horizon and next leaf.",
            recovery="rerun the progress map command if the position report is missing",
        ),
        _packet_item(
            order=1,
            section="storyboard",
            title="Demo Asset Inventory",
            report="docs/reports/2026-07-05-e2e1-demo-asset-inventory.md",
            command="python scripts\\e2e_demo_asset_inventory.py --format text --write",
            purpose="Show the ordered public-safe demo story.",
            recovery="rerun E2E1 inventory if any core report is missing",
        ),
        _packet_item(
            order=2,
            section="contract",
            title="Scenario Contract",
            report="docs/reports/2026-07-05-e2e2-scenario-contract.md",
            command="python scripts\\e2e_scenario_contract.py --format text --write",
            purpose="Fix stage inputs, evidence, outputs, review checkpoints, commands, and failure boundaries.",
            recovery="rerun E2E2 contract if stage boundaries are unclear",
        ),
        _packet_item(
            order=3,
            section="parser",
            title="Local Parser Evidence",
            report="docs/reports/2026-07-05-real-local-parser-prototype-close-report.md",
            command="python scripts\\real_local_parser_prototype_close_gate.py --format text",
            purpose="Explain the local-safe parser boundary.",
            recovery="use E2E1 inventory to identify missing parser evidence",
        ),
        _packet_item(
            order=4,
            section="source",
            title="Controlled Source Evidence",
            report="docs/reports/2026-07-05-source-body-ingestion-controlled-lane-close-report.md",
            command="python scripts\\controlled_lane_close_gate.py --format text",
            purpose="Explain authorized source lane handling.",
            recovery="rerun controlled lane close gate after source policy reports exist",
        ),
        _packet_item(
            order=5,
            section="workflow",
            title="Workflow Evidence",
            report="docs/reports/2026-07-05-workflow-coverage-expansion-close-report.md",
            command="python scripts\\workflow_coverage_close_gate.py --format text",
            purpose="Explain the 1037 provisions decision-prep extension.",
            recovery="rerun workflow coverage close gate after adapter evidence exists",
        ),
        _packet_item(
            order=6,
            section="retriever",
            title="Retriever Promotion Evidence",
            report="docs/reports/2026-07-05-runtime-retriever-promotion-gate-close-report.md",
            command="python scripts\\runtime_retriever_promotion_close_gate.py --format text",
            purpose="Explain why default retriever promotion is deferred.",
            recovery="rerun promotion close gate and keep default unchanged if evidence is weak",
        ),
        _packet_item(
            order=7,
            section="operator",
            title="Operator Evidence",
            report="docs/reports/2026-07-05-operator-experience-hardening-close-report.md",
            command="python scripts\\operator_experience_close_gate.py --format text",
            purpose="Show command discovery, doctor, manifest, and recovery path.",
            recovery="run operator doctor and follow recovery playbook hints",
        ),
    ]
    checks = {
        "packet_items_ordered": [item["order"] for item in packet_items] == sorted(item["order"] for item in packet_items),
        "all_reports_exist": all(item["report_exists"] for item in packet_items),
        "all_commands_present": all(item["command"] for item in packet_items),
        "all_recovery_hints_present": all(item["recovery"] for item in packet_items),
        "protected_paths_absent": all(_is_safe_report(item["report"]) for item in packet_items),
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "E2E3 Demo Packet Builder",
        "ok": not errors,
        "horizon": "end-to-end-demo-scenario",
        "completed_milestone": "E2E3",
        "packet_path": _display_path(PACKET_PATH),
        "packet_claim": "Open one index and walk the public-safe end-to-end demo without reading ROADMAP internals.",
        "items": packet_items,
        "checks": checks,
        "errors": errors,
        "next_leaf": "E2E4_demo_smoke_and_navigation_gate",
        "report_path": _display_path(REPORT_PATH),
    }


def render_packet_index(packet: dict[str, Any]) -> str:
    lines = [
        "# End-to-End Demo Packet",
        "",
        "> Scope: one public-safe navigation surface for the firm-facing local toolkit demo.",
        "",
        "## How To Use",
        "",
        packet["packet_claim"],
        "",
        "## Demo Run Order",
        "",
        "| Order | Section | Report | Command | Purpose | Recovery |",
        "|---:|---|---|---|---|---|",
    ]
    for item in packet["items"]:
        lines.append(
            "| {order} | {section} | `{report}` | `{command}` | {purpose} | {recovery} |".format(
                order=item["order"],
                section=item["section"],
                report=item["report"],
                command=item["command"],
                purpose=item["purpose"],
                recovery=item["recovery"],
            )
        )
    lines.extend(
        [
            "",
            "## Boundaries",
            "",
            "- This packet uses public-safe reports only.",
            "- It demonstrates decision-prep and review support, not final accounting judgment.",
            "- It does not claim release readiness.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: generator report for the end-to-end demo packet.",
        "",
        "## 한 줄 결론",
        "",
        result["packet_claim"],
        "",
        f"- Packet: `{result['packet_path']}`",
        "",
        "## Packet Items",
        "",
        "| Order | Section | Report | Exists |",
        "|---:|---|---|---|",
    ]
    for item in result["items"]:
        lines.append(f"| {item['order']} | {item['section']} | `{item['report']}` | {item['report_exists']} |")
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


def write_outputs(packet_path: Path = PACKET_PATH, report_path: Path = REPORT_PATH) -> dict[str, Any]:
    packet = build_demo_packet()
    packet_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    packet_path.write_text(render_packet_index(packet), encoding="utf-8")
    report_path.write_text(render_markdown(packet), encoding="utf-8")
    return packet


def _packet_item(
    *,
    order: int,
    section: str,
    title: str,
    report: str,
    command: str,
    purpose: str,
    recovery: str,
) -> dict[str, Any]:
    return {
        "order": order,
        "section": section,
        "title": title,
        "report": report,
        "report_exists": (ROOT / report).exists(),
        "command": command,
        "purpose": purpose,
        "recovery": recovery,
    }


def _is_safe_report(value: str) -> bool:
    normalized = value.replace("\\", "/").lower()
    blocked = ("data/", "embedding", "kifrs.db", "dogfood")
    return not any(term in normalized for term in blocked)


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build E2E3 demo packet.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--packet-out", type=Path, default=PACKET_PATH)
    parser.add_argument("--report-out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_outputs(args.packet_out, args.report_out) if args.write else build_demo_packet()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- packet: {result['packet_path']}")
        print(f"- items: {len(result['items'])}")
        print(f"- next leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
