from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.e2e_demo_asset_inventory import build_demo_asset_inventory  # noqa: E402
from scripts.e2e_demo_packet_builder import build_demo_packet  # noqa: E402
from scripts.e2e_demo_smoke_gate import build_demo_smoke_gate  # noqa: E402
from scripts.e2e_scenario_contract import build_scenario_contract  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-end-to-end-demo-scenario-close-report.md"


def build_demo_close_gate() -> dict[str, Any]:
    evidence = [
        _evidence("E2E1", "Demo asset inventory and storyboard", "docs/reports/2026-07-05-e2e1-demo-asset-inventory.md", build_demo_asset_inventory()["ok"]),
        _evidence("E2E2", "Scenario contract", "docs/reports/2026-07-05-e2e2-scenario-contract.md", build_scenario_contract()["ok"]),
        _evidence("E2E3", "Demo packet builder", "docs/reports/2026-07-05-e2e3-demo-packet-builder.md", build_demo_packet()["ok"]),
        _evidence("E2E3P", "Demo packet index", "docs/reports/end-to-end-demo/INDEX.md", (ROOT / "docs/reports/end-to-end-demo/INDEX.md").exists()),
        _evidence("E2E4", "Demo smoke and navigation gate", "docs/reports/2026-07-05-e2e4-demo-smoke-gate.md", build_demo_smoke_gate()["ok"]),
    ]
    checks = {
        "all_evidence_reports_exist": all(item["exists"] for item in evidence),
        "all_evidence_gates_ok": all(item["gate_ok"] for item in evidence),
        "packet_index_exists": (ROOT / "docs/reports/end-to-end-demo/INDEX.md").exists(),
        "smoke_gate_ok": build_demo_smoke_gate()["ok"],
        "public_safe_boundary_declared": True,
        "human_review_boundary_declared": True,
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    close_result = "demo_ready" if not errors else "partial"
    return {
        "title": "End-to-End Demo Scenario Close Report",
        "ok": not errors,
        "horizon": "end-to-end-demo-scenario",
        "completed_milestone": "E2E5",
        "close_result": close_result,
        "evidence": evidence,
        "checks": checks,
        "errors": errors,
        "demo_packet": "docs/reports/end-to-end-demo/INDEX.md",
        "residual_risks": [
            "This is a public-safe local demo packet, not production packaging.",
            "Default retriever promotion remains deferred until stronger evaluation evidence and explicit authorization.",
            "The demo supports decision preparation and review, not final accounting judgment.",
        ],
        "next_horizon_candidate": "demo-rehearsal-or-packaging-readiness",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: close gate for the public-safe end-to-end demo scenario horizon.",
        "",
        "## 한 줄 결론",
        "",
        f"Close result: `{result['close_result']}`.",
        "",
        f"- Demo packet: `{result['demo_packet']}`",
        f"- Next horizon candidate: `{result['next_horizon_candidate']}`",
        "",
        "## Evidence",
        "",
        "| Milestone | Evidence | Exists | Gate OK |",
        "|---|---|---|---|",
    ]
    for item in result["evidence"]:
        lines.append(f"| {item['id']} {item['name']} | `{item['path']}` | {item['exists']} | {item['gate_ok']} |")
    lines.extend(["", "## Checks", "", "| Check | OK |", "|---|---|"])
    for name, ok in result["checks"].items():
        lines.append(f"| {name} | {ok} |")
    lines.extend(["", "## Residual Risks", ""])
    lines.extend(f"- {risk}" for risk in result["residual_risks"])
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
    result = build_demo_close_gate()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _evidence(id_: str, name: str, path: str, gate_ok: bool) -> dict[str, Any]:
    return {
        "id": id_,
        "name": name,
        "path": path,
        "exists": (ROOT / path).exists(),
        "gate_ok": gate_ok,
    }


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Close E2E demo scenario horizon.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_demo_close_gate()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- close result: {result['close_result']}")
        print(f"- demo packet: {result['demo_packet']}")
        print(f"- next horizon candidate: {result['next_horizon_candidate']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
