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
from scripts.non_ifrs_source_asset_inventory import build_inventory  # noqa: E402
from scripts.validate_non_ifrs_chunking_policy import validate_policy  # noqa: E402
from scripts.validate_non_ifrs_source_records import build_validation  # noqa: E402


GATE_REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-nis5-dataization-gate.md"
CLOSE_REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-non-ifrs-source-dataization-close-report.md"

REQUIRED_REPORTS = [
    ROOT / "docs" / "reports" / "2026-07-05-nis1-source-asset-inventory.md",
    ROOT / "docs" / "reports" / "2026-07-05-nis2-source-record-contract.md",
    ROOT / "docs" / "reports" / "2026-07-05-nis3-dataization-fixtures.md",
    ROOT / "docs" / "reports" / "2026-07-05-nis4-chunking-embedding-policy.md",
]

REGRESSION_COMMANDS = [
    "python scripts\\validate_non_ifrs_source_records.py --format text",
    "python scripts\\validate_non_ifrs_chunking_policy.py --format text",
    "python scripts\\default_retriever_guard.py --format text",
    "python scripts\\quality_preflight.py --format text",
]

NEXT_HORIZON = "multi-authority-runtime-hardening"


def build_gate() -> dict[str, Any]:
    inventory = build_inventory()
    records = build_validation()
    chunking = validate_policy()
    default_guard = check_default_retriever_guard()
    report_status = [{"path": _display_path(path), "exists": path.exists()} for path in REQUIRED_REPORTS]

    errors: list[str] = []
    errors.extend(f"missing required report: {row['path']}" for row in report_status if not row["exists"])
    if inventory["ok"] is not True:
        errors.extend(f"inventory: {error}" for error in inventory["errors"])
    if records["ok"] is not True:
        errors.extend(f"records: {error}" for error in records["errors"])
    if chunking["ok"] is not True:
        errors.extend(f"chunking: {error}" for error in chunking["errors"])
    if default_guard["ok"] is not True:
        errors.extend(f"default_guard: {error}" for error in default_guard["errors"])

    handoff_contract = {
        "next_horizon": NEXT_HORIZON,
        "source_record_contract": "kifrs/ingestion/source_record.py",
        "source_records_fixture": "docs/ingestion/non_ifrs_source_records.example.json",
        "chunking_policy": "docs/ingestion/non_ifrs_chunking_policy.json",
        "runtime_boundary": [
            "K-IFRS paragraph evidence remains primary.",
            "supporting interpretation, legal boundary, fact evidence, and client-private facts stay separated.",
            "default retriever remains hybrid until a separate promotion implementation is approved.",
        ],
    }
    return {
        "ok": not errors,
        "title": "NIS5 Dataization Gate",
        "milestone": "NIS5",
        "required_reports": report_status,
        "inventory_snapshot": {
            "lanes": sorted(inventory["lanes"]),
            "reusable_asset_count": inventory["reusable_asset_count"],
            "missing_asset_count": inventory["missing_asset_count"],
        },
        "records_snapshot": {
            "total": records["total"],
            "by_type": records["by_type"],
            "records_path": records["records_path"],
        },
        "chunking_snapshot": {
            "total_lanes": chunking["total_lanes"],
            "policy_path": chunking["policy_path"],
            "lanes": chunking["lanes"],
        },
        "default_guard_snapshot": {
            "ok": default_guard["ok"],
            "default_mode": default_guard["default_mode"],
            "target_retriever_exposed_in_mcp": default_guard["target_retriever_exposed_in_mcp"],
            "promote_to_default": default_guard["promote_to_default"],
        },
        "handoff_contract": handoff_contract,
        "regression_commands": REGRESSION_COMMANDS,
        "next_horizon": NEXT_HORIZON,
        "errors": errors,
        "report_path": _display_path(GATE_REPORT_PATH),
        "close_report_path": _display_path(CLOSE_REPORT_PATH),
    }


def render_gate_markdown(gate: dict[str, Any]) -> str:
    conclusion = (
        f"Non-IFRS source dataization is ready to hand off to `{gate['next_horizon']}`."
        if gate["ok"]
        else "Non-IFRS source dataization is not ready; fix the listed errors."
    )
    lines = [
        "# NIS5 Dataization Gate",
        "",
        "> Scope: final gate for the non-IFRS source dataization horizon.",
        "",
        "## One-Line Conclusion",
        "",
        conclusion,
        "",
        "## Evidence Chain",
        "",
        "| Report | Exists |",
        "|---|---|",
    ]
    for row in gate["required_reports"]:
        lines.append(f"| `{row['path']}` | {row['exists']} |")
    records = gate["records_snapshot"]
    default_guard = gate["default_guard_snapshot"]
    lines.extend(
        [
            "",
            "## Dataization Snapshot",
            "",
            f"- Inventory lanes: {', '.join(gate['inventory_snapshot']['lanes'])}",
            f"- Reusable assets: {gate['inventory_snapshot']['reusable_asset_count']}",
            f"- Source records: {records['total']} ({records['by_type']})",
            f"- Chunking lanes: {gate['chunking_snapshot']['total_lanes']}",
            "",
            "## Runtime Boundary",
            "",
            f"- Default mode: `{default_guard['default_mode']}`",
            f"- Target exposed in MCP: {default_guard['target_retriever_exposed_in_mcp']}",
            f"- Promote to default: {default_guard['promote_to_default']}",
            "",
            "## Handoff Contract",
            "",
            f"- Next horizon: `{gate['handoff_contract']['next_horizon']}`",
            f"- Source record contract: `{gate['handoff_contract']['source_record_contract']}`",
            f"- Source records fixture: `{gate['handoff_contract']['source_records_fixture']}`",
            f"- Chunking policy: `{gate['handoff_contract']['chunking_policy']}`",
            "",
            "## Regression Commands",
            "",
        ]
    )
    lines.extend(f"- `{command}`" for command in gate["regression_commands"])
    if gate["errors"]:
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in gate["errors"])
    lines.extend(
        [
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps(gate, ensure_ascii=False, indent=2, default=str),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def render_close_markdown(gate: dict[str, Any]) -> str:
    lines = [
        "# Non-IFRS Source Dataization Close Report",
        "",
        "> Scope: close report for `non-ifrs-source-dataization`.",
        "",
        "## One-Line Result",
        "",
        "The horizon is closed: non-IFRS sources now have inventory, source record contract, public-safe fixtures, chunk/index policy, and runtime handoff gate.",
        "",
        "## Closed Milestones",
        "",
        "| Milestone | Result | Evidence |",
        "|---|---|---|",
        "| NIS1 | Existing source assets inventoried by lane. | `docs/reports/2026-07-05-nis1-source-asset-inventory.md` |",
        "| NIS2 | Source record contract implemented and tested. | `docs/reports/2026-07-05-nis2-source-record-contract.md` |",
        "| NIS3 | Public-safe source record fixture and validator completed. | `docs/reports/2026-07-05-nis3-dataization-fixtures.md` |",
        "| NIS4 | Chunking and embedding policy completed. | `docs/reports/2026-07-05-nis4-chunking-embedding-policy.md` |",
        "| NIS5 | Dataization gate and runtime handoff completed. | `docs/reports/2026-07-05-nis5-dataization-gate.md` |",
        "",
        "## Handoff",
        "",
        f"- Next horizon: `{gate['next_horizon']}`",
        "- Runtime must keep primary K-IFRS evidence separate from supporting interpretation, legal boundary, fact evidence, and client-private facts.",
        "- Public repo remains metadata/schema/synthetic-fixture only.",
        "",
        "## Regression Commands",
        "",
    ]
    lines.extend(f"- `{command}`" for command in gate["regression_commands"])
    lines.extend(
        [
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps(gate, ensure_ascii=False, indent=2, default=str),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_reports(gate_path: Path = GATE_REPORT_PATH, close_path: Path = CLOSE_REPORT_PATH) -> dict[str, Any]:
    gate = build_gate()
    gate_path.parent.mkdir(parents=True, exist_ok=True)
    close_path.parent.mkdir(parents=True, exist_ok=True)
    gate_path.write_text(render_gate_markdown(gate), encoding="utf-8")
    close_path.write_text(render_close_markdown(gate), encoding="utf-8")
    return gate


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run NIS5 non-IFRS dataization gate.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=GATE_REPORT_PATH)
    parser.add_argument("--close-out", type=Path, default=CLOSE_REPORT_PATH)
    args = parser.parse_args()

    gate = write_reports(args.out, args.close_out) if args.write else build_gate()
    if args.format == "json":
        print(json.dumps(gate, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_gate_markdown(gate), end="")
    else:
        print(gate["title"])
        print(f"- ok: {gate['ok']}")
        print(f"- next_horizon: {gate['next_horizon']}")
        print(f"- records: {gate['records_snapshot']['total']}")
        print(f"- chunking_lanes: {gate['chunking_snapshot']['total_lanes']}")
        print(f"- report_path: {gate['report_path']}")
        print(f"- close_report_path: {gate['close_report_path']}")
    if not gate["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
