from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.client_private_evidence_adapter_report import build_adapter_report  # noqa: E402
from scripts.client_private_parser_boundary_audit import build_boundary_audit  # noqa: E402
from scripts.client_private_parser_runtime_contract_report import build_contract_report  # noqa: E402
from scripts.client_private_runtime_deletion_gate_report import build_deletion_gate_report  # noqa: E402
from scripts.multi_authority_runtime_gate import build_gate as build_multi_authority_gate  # noqa: E402


GATE_REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-cp5-private-runtime-close-demo.md"
CLOSE_REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-client-private-parser-runtime-close-report.md"


def build_gate() -> dict[str, Any]:
    cp1 = build_boundary_audit()
    cp2 = build_contract_report()
    cp3 = build_adapter_report()
    cp4 = build_deletion_gate_report()
    multi_authority = build_multi_authority_gate()
    checks = {
        "cp1_boundary_audit": cp1["ok"],
        "cp2_runtime_contract": cp2["ok"],
        "cp3_evidence_adapter": cp3["ok"],
        "cp4_deletion_gate": cp4["ok"],
        "multi_authority_runtime_gate": multi_authority["ok"],
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "CP5 Private Runtime Close Demo",
        "ok": not errors,
        "horizon": "client-private-parser-runtime",
        "milestone": "CP5",
        "checks": checks,
        "errors": errors,
        "public_safe": cp2["public_safe"] and cp3["public_safe"] and cp4["public_safe"],
        "runtime_path": [
            "synthetic parser-shaped structured facts",
            "runtime parser contract",
            "client_private_fact authority reference",
            "review-pack client-private authority panel",
            "runtime deletion gate",
        ],
        "carried_regression_commands": [
            "python scripts\\multi_authority_runtime_gate.py --format text",
            "python scripts\\quality_preflight.py --format text",
            "python scripts\\rag_quality_final_gate.py --format text",
        ],
        "next_horizon": "firm-facing-product-surface",
        "report_path": _display_path(GATE_REPORT_PATH),
        "close_report_path": _display_path(CLOSE_REPORT_PATH),
    }


def render_markdown(gate: dict[str, Any]) -> str:
    conclusion = (
        "Client-private parser runtime is ready to close."
        if gate["ok"]
        else "Client-private parser runtime is not ready; fix the listed checks."
    )
    lines = [
        f"# {gate['title']}",
        "",
        "> Scope: CP5 close demo for local-only client-private parser runtime.",
        "",
        "## One-Line Conclusion",
        "",
        conclusion,
        "",
        "## Gate Status",
        "",
        f"- ok: {gate['ok']}",
        f"- public safe: {gate['public_safe']}",
        f"- next horizon: `{gate['next_horizon']}`",
        "",
        "## Checks",
        "",
        "| Check | OK |",
        "|---|---|",
    ]
    for name, ok in gate["checks"].items():
        lines.append(f"| {name} | {ok} |")
    lines.extend(["", "## Runtime Path", ""])
    lines.extend(f"- {step}" for step in gate["runtime_path"])
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


def render_close_markdown(gate: dict[str, Any]) -> str:
    lines = [
        "# Client-Private Parser Runtime Close Report",
        "",
        "## Result",
        "",
        f"- close status: {'closed' if gate['ok'] else 'blocked'}",
        f"- gate report: `{gate['report_path']}`",
        f"- next horizon: `{gate['next_horizon']}`",
        "",
        "## Completed Milestones",
        "",
        "- CP1 private parser boundary audit",
        "- CP2 local parser runtime contract",
        "- CP3 client-private evidence adapter",
        "- CP4 deletion and retention gate",
        "- CP5 private runtime close demo",
        "",
        "## Product Meaning",
        "",
        "A client-private local parser path now exists as a public-safe runtime contract: structured facts only, client-private authority reference only, deletion-gated close, and no public private-source payload.",
        "",
        "## Next Horizon",
        "",
        "`firm-facing-product-surface` should turn the runtime proof into an operator-facing demo surface and install/readiness package.",
        "",
    ]
    return "\n".join(lines)


def write_reports() -> dict[str, Any]:
    gate = build_gate()
    GATE_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    GATE_REPORT_PATH.write_text(render_markdown(gate), encoding="utf-8")
    CLOSE_REPORT_PATH.write_text(render_close_markdown(gate), encoding="utf-8")
    return gate


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Run CP5 client-private parser runtime close gate.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    gate = write_reports() if args.write else build_gate()
    if args.format == "json":
        print(json.dumps(gate, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(gate), end="")
    else:
        print(gate["title"])
        print(f"- ok: {gate['ok']}")
        print(f"- public safe: {gate['public_safe']}")
        print(f"- next horizon: {gate['next_horizon']}")
    return 0 if gate["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
