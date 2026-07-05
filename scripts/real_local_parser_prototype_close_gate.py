from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-real-local-parser-prototype-close-report.md"
REQUIRED_REPORTS = {
    "rlp1_asset_inventory": ROOT / "docs" / "reports" / "2026-07-05-rlp1-parser-prototype-asset-inventory.md",
    "rlp2_fixture_adapter": ROOT / "docs" / "reports" / "2026-07-05-rlp2-local-fixture-parser-adapter.md",
    "rlp3_deletion_simulation": ROOT / "docs" / "reports" / "2026-07-05-rlp3-deletion-automation-simulation.md",
    "rlp4_leak_tests": ROOT / "docs" / "reports" / "2026-07-05-rlp4-private-payload-leak-tests.md",
    "product_trust_close": ROOT / "docs" / "reports" / "2026-07-05-product-trust-quality-close-report.md",
    "client_private_runtime_close": ROOT / "docs" / "reports" / "2026-07-05-client-private-parser-runtime-close-report.md",
}


def build_close_gate() -> dict[str, Any]:
    from scripts.client_private_parser_runtime_gate import build_gate as build_private_runtime_gate
    from scripts.deletion_automation_simulation import check_deletion_automation_simulation
    from scripts.local_fixture_parser_adapter import check_local_fixture_parser_adapter
    from scripts.parser_prototype_asset_inventory import build_inventory
    from scripts.private_payload_leak_tests import scan_public_parser_artifacts
    from scripts.product_trust_quality_gate import build_gate as build_product_trust_gate

    rlp1 = build_inventory()
    rlp2 = check_local_fixture_parser_adapter()
    rlp3 = check_deletion_automation_simulation()
    rlp4 = scan_public_parser_artifacts()
    product_trust = build_product_trust_gate()
    private_runtime = build_private_runtime_gate()
    reports = {
        name: {"path": _display_path(path), "exists": path.exists()}
        for name, path in REQUIRED_REPORTS.items()
    }
    missing_reports = [name for name, info in reports.items() if not info["exists"]]
    checks = {
        "rlp1_asset_inventory": rlp1["ok"],
        "rlp2_fixture_adapter": rlp2["ok"],
        "rlp3_deletion_simulation": rlp3["ok"],
        "rlp4_leak_tests": rlp4["ok"],
        "product_trust_close": product_trust["ok"],
        "client_private_runtime_close": private_runtime["ok"],
        "all_required_reports_present": not missing_reports,
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "Real Local Parser Prototype Close Gate",
        "ok": not errors,
        "horizon": "real-local-parser-prototype",
        "completed_milestone": "RLP5",
        "close_status": "closed" if not errors else "blocked",
        "checks": checks,
        "errors": errors,
        "reports": reports,
        "missing_reports": missing_reports,
        "prototype_path": [
            "RLP1 inventory existing parser/runtime assets",
            "RLP2 fixture-like input to structured facts and review questions",
            "RLP3 deletion lifecycle simulation blocks close without attestation",
            "RLP4 public report leak tests",
            "RLP5 close gate with carried trust/runtime evidence",
        ],
        "carried_regression_commands": [
            "python -m pytest tests\\test_parser_prototype_asset_inventory.py tests\\test_local_fixture_parser_adapter.py tests\\test_deletion_automation_simulation.py tests\\test_private_payload_leak_tests.py tests\\test_real_local_parser_prototype_close_gate.py -q",
            "python scripts\\product_trust_quality_gate.py --format text",
            "python scripts\\client_private_parser_runtime_gate.py --format text",
        ],
        "still_not_implemented": [
            "real private-file parser",
            "OCR",
            "upload UI",
            "private embedding/index namespace",
            "real filesystem deletion automation",
        ],
        "next_horizon": "source-body-ingestion-controlled-lane",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(gate: dict[str, Any]) -> str:
    lines = [
        f"# {gate['title']}",
        "",
        "> Scope: RLP5 close gate for the real-local-parser-prototype horizon.",
        "",
        "## 한 줄 결론",
        "",
        (
            "The real-local-parser-prototype horizon is closed: the toolkit now has a local-safe fixture parser path from structured input to review questions, deletion simulation, and leak-tested public reports."
            if gate["ok"]
            else "The real-local-parser-prototype horizon is blocked; fix the listed checks."
        ),
        "",
        "## Close Status",
        "",
        f"- status: {gate['close_status']}",
        f"- next horizon: `{gate['next_horizon']}`",
        "",
        "## Checks",
        "",
        "| Check | OK |",
        "|---|---|",
    ]
    for name, ok in gate["checks"].items():
        lines.append(f"| {name} | {ok} |")
    lines.extend(["", "## Prototype Path", ""])
    lines.extend(f"- {step}" for step in gate["prototype_path"])
    lines.extend(["", "## Required Reports", "", "| Report | Path | Exists |", "|---|---|---|"])
    for name, info in gate["reports"].items():
        lines.append(f"| {name} | `{info['path']}` | {info['exists']} |")
    lines.extend(["", "## Still Not Implemented", ""])
    lines.extend(f"- {item}" for item in gate["still_not_implemented"])
    lines.extend(["", "## Carried Regression Commands", ""])
    lines.extend(f"- `{command}`" for command in gate["carried_regression_commands"])
    lines.extend(["", "## Errors", ""])
    lines.extend(f"- {error}" for error in gate["errors"]) if gate["errors"] else lines.append("- none")
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


def write_report(path: Path = REPORT_PATH) -> dict[str, Any]:
    gate = build_close_gate()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(gate), encoding="utf-8")
    return gate


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Run RLP5 real local parser prototype close gate.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    gate = write_report(args.out) if args.write else build_close_gate()
    if args.format == "json":
        print(json.dumps(gate, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(gate), end="")
    else:
        print(gate["title"])
        print(f"- ok: {gate['ok']}")
        print(f"- close status: {gate['close_status']}")
        print(f"- next horizon: {gate['next_horizon']}")
        for error in gate["errors"]:
            print(f"- {error}")
    return 0 if gate["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
