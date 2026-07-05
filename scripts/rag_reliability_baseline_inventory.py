from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.default_retriever_guard import check_default_retriever_guard  # noqa: E402
from scripts.opt_in_retriever_promotion_decision_gate import check_promotion_decision_gate  # noqa: E402
from scripts.quality_preflight import DEFAULT_COMMANDS  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-rr1-rag-baseline-inventory.md"

EVIDENCE_REPORTS = {
    "rag_quality_refresh_close": ROOT / "docs" / "reports" / "2026-07-05-rag-quality-refresh-close-report.md",
    "opt_in_retriever_demo_validation": ROOT
    / "docs"
    / "reports"
    / "2026-07-05-odv1-opt-in-retriever-demo-validation.md",
    "promotion_decision_gate": ROOT
    / "docs"
    / "reports"
    / "2026-07-05-orpd1-opt-in-retriever-promotion-decision-gate.md",
    "default_retriever_guard": ROOT / "docs" / "reports" / "2026-07-05-default-retriever-guard.md",
}


def build_inventory() -> dict[str, Any]:
    default_guard = check_default_retriever_guard()
    promotion = check_promotion_decision_gate()
    public_safe_commands = [
        {
            "name": entry["name"],
            "command": _format_command(entry["cmd"]),
            "protected_assets_required": False,
            "purpose": _command_purpose(entry["name"]),
        }
        for entry in DEFAULT_COMMANDS
    ]
    local_data_commands = [
        {
            "name": "full_retrieval_goldset_gate",
            "command": "python scripts\\rag_quality_final_gate.py --format text",
            "protected_assets_required": True,
            "local_dependency": "data/eval/goldset.json",
            "purpose": "50-item retrieval-only gate for the opt-in repair retriever.",
        },
        {
            "name": "default_retriever_guard",
            "command": "python scripts\\default_retriever_guard.py --format text",
            "protected_assets_required": False,
            "local_dependency": "cached promotion report",
            "purpose": "Code-level invariant that keeps MCP search default at hybrid.",
        },
    ]
    return {
        "ok": default_guard["ok"] and promotion["ok"],
        "title": "RR1 RAG Baseline Inventory",
        "milestone": "RR1",
        "public_safe_commands": public_safe_commands,
        "local_data_commands": local_data_commands,
        "retriever_state": {
            "default_mode": default_guard["default_mode"],
            "target_retriever": default_guard["target_retriever"],
            "target_retriever_opt_in_available": default_guard["target_retriever_opt_in_available"],
            "target_retriever_exposed_in_mcp": default_guard["target_retriever_exposed_in_mcp"],
            "promotion_decision": promotion["decision"]["decision"],
            "promote_to_default": promotion["decision"]["promote_to_default"],
            "promotion_blockers": promotion["decision"]["blockers"],
        },
        "evidence_reports": [
            {
                "name": name,
                "path": _display_path(path),
                "present": path.exists(),
            }
            for name, path in EVIDENCE_REPORTS.items()
        ],
        "minimum_rr_verification_set": [
            "python scripts\\quality_preflight.py --format text",
            "python scripts\\eval_quality_gate.py --runner local-rag --only Q019 Q020 Q021 Q022 Q023 --min-composite 0.6 --min-cite 0.45 --format text",
            "python scripts\\default_retriever_guard.py --format text",
            "python scripts\\rag_quality_final_gate.py --format text",
        ],
        "rr2_input": {
            "needed": "question-type eval matrix and seed coverage split",
            "buckets": [
                "direct standard lookup",
                "judgment and paragraph-combination question",
                "workflow seed question",
                "disclosure question",
                "user_note or source-pack dependent question",
            ],
        },
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(inventory: dict[str, Any]) -> str:
    lines = [
        "# RR1 RAG Baseline Inventory",
        "",
        "> Scope: public-safe inventory of current K-IFRS RAG quality commands, evidence reports, and retriever state.",
        "",
        "## 한 줄 결론",
        "",
        _one_line_conclusion(inventory),
        "",
        "## Retriever State",
        "",
        f"- Runtime default mode: `{inventory['retriever_state']['default_mode']}`",
        f"- Opt-in repair retriever: `{inventory['retriever_state']['target_retriever']}`",
        f"- Opt-in retriever available in eval registry: {inventory['retriever_state']['target_retriever_opt_in_available']}",
        f"- Opt-in retriever exposed in MCP search modes: {inventory['retriever_state']['target_retriever_exposed_in_mcp']}",
        f"- Promotion decision: {inventory['retriever_state']['promotion_decision']}",
        f"- Promote to default now: {inventory['retriever_state']['promote_to_default']}",
        "",
        "## Public-Safe Commands",
        "",
        "| Name | Command | Purpose |",
        "|---|---|---|",
    ]
    for command in inventory["public_safe_commands"]:
        lines.append(f"| {command['name']} | `{command['command']}` | {command['purpose']} |")
    lines.extend(
        [
            "",
            "## Local Data / Protected Boundary Commands",
            "",
            "| Name | Command | Local Dependency | Protected Assets Required | Purpose |",
            "|---|---|---|---|---|",
        ]
    )
    for command in inventory["local_data_commands"]:
        lines.append(
            "| {name} | `{cmd}` | `{dep}` | {protected} | {purpose} |".format(
                name=command["name"],
                cmd=command["command"],
                dep=command["local_dependency"],
                protected=command["protected_assets_required"],
                purpose=command["purpose"],
            )
        )
    lines.extend(
        [
            "",
            "## Existing Evidence Reports",
            "",
            "| Report | Path | Present |",
            "|---|---|---|",
        ]
    )
    for report in inventory["evidence_reports"]:
        lines.append(f"| {report['name']} | `{report['path']}` | {report['present']} |")
    lines.extend(
        [
            "",
            "## Minimum RR Verification Set",
            "",
        ]
    )
    lines.extend(f"- `{command}`" for command in inventory["minimum_rr_verification_set"])
    lines.extend(
        [
            "",
            "## RR2 Input",
            "",
            f"- Needed: {inventory['rr2_input']['needed']}",
            "- Buckets:",
        ]
    )
    lines.extend(f"  - {bucket}" for bucket in inventory["rr2_input"]["buckets"])
    lines.extend(
        [
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps(inventory, ensure_ascii=False, indent=2, default=str),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH) -> dict[str, Any]:
    inventory = build_inventory()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(inventory), encoding="utf-8")
    return inventory


def _one_line_conclusion(inventory: dict[str, Any]) -> str:
    if inventory["ok"]:
        return "The current default remains `hybrid`; RAG reliability work can continue with public-safe gates plus one local goldset gate."
    return "The baseline inventory found a failing guard; fix it before moving to RR2."


def _command_purpose(name: str) -> str:
    return {
        "focused_pytest": "Regression tests for eval gates, authority source pack, and user notes.",
        "local_rag_threshold_gate": "Focused local RAG answer-quality threshold gate.",
        "authority_registry": "Validate source registry metadata.",
        "authority_source_pack": "Validate authority source pack boundaries.",
        "user_note_v2_audit": "Validate user_note v2 trigger and anchor hygiene.",
    }.get(name, "Quality preflight command.")


def _format_command(parts: list[str]) -> str:
    normalized = ["python" if Path(part).name.lower().startswith("python") else part for part in parts]
    return " ".join(normalized)


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Render RR1 RAG baseline inventory.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    inventory = write_report(args.out) if args.write else build_inventory()
    if args.format == "json":
        print(json.dumps(inventory, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(inventory), end="")
    else:
        print(inventory["title"])
        print(f"- ok: {inventory['ok']}")
        print(f"- default_mode: {inventory['retriever_state']['default_mode']}")
        print(f"- target_retriever: {inventory['retriever_state']['target_retriever']}")
        print(f"- promotion_decision: {inventory['retriever_state']['promotion_decision']}")
        print(f"- report_path: {inventory['report_path']}")

    if not inventory["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
