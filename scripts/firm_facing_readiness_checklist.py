from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-fps3-readiness-checklist.md"

REQUIRED_FILES = {
    "objective": ROOT / "docs" / "OBJECTIVE.md",
    "horizon": ROOT / "docs" / "horizons" / "firm-facing-product-surface.md",
    "fps1_inventory": ROOT / "docs" / "reports" / "2026-07-05-fps1-product-surface-inventory.md",
    "fps2_demo_packet": ROOT / "docs" / "reports" / "2026-07-05-fps2-operator-demo-command.md",
    "multi_authority_close": ROOT / "docs" / "reports" / "2026-07-05-multi-authority-runtime-hardening-close-report.md",
    "client_private_close": ROOT / "docs" / "reports" / "2026-07-05-client-private-parser-runtime-close-report.md",
    "rag_quality_close": ROOT / "docs" / "reports" / "2026-07-05-rag-quality-refresh-close-report.md",
    "default_retriever_guard": ROOT / "docs" / "reports" / "2026-07-05-default-retriever-guard.md",
}

RUN_COMMANDS = [
    "uv sync",
    "python scripts\\firm_facing_operator_demo_command.py --format markdown --write",
    "python scripts\\firm_facing_readiness_checklist.py --format text --write",
    "python scripts\\quality_preflight.py --format text",
    "python scripts\\rag_quality_final_gate.py --format text",
]

PROTECTED_BOUNDARY = [
    "Do not commit or publish K-IFRS PDFs, parsed text, SQLite paragraph DB dumps, or embedding indexes.",
    "Do not place CPA exam/dogfood materials in public reports.",
    "Do not include real client files, raw source body, OCR text, identifiers, private embeddings, or customer-specific locators in demo output.",
    "Client-private parser output is structured facts only, represented as client_private_fact authority references, with deletion-gated runtime evidence.",
    "The demo produces decision-prep drafts. Accountant review, sign-off, audit opinion, tax/legal conclusion, and final client communication remain human responsibilities.",
]


def build_readiness() -> dict[str, Any]:
    files = {
        name: {
            "path": _display_path(path),
            "exists": path.exists(),
        }
        for name, path in REQUIRED_FILES.items()
    }
    missing = [name for name, info in files.items() if not info["exists"]]
    return {
        "title": "FPS3 Readiness Checklist And Local Install Path",
        "ok": not missing,
        "horizon": "firm-facing-product-surface",
        "milestone": "FPS3",
        "required_files": files,
        "missing_files": missing,
        "local_install_path": {
            "python": "Python 3.11+",
            "dependency_command": "uv sync",
            "runtime_shape": "local toolkit; protected data is indexed locally by the operator",
        },
        "run_commands": RUN_COMMANDS,
        "protected_boundary": PROTECTED_BOUNDARY,
        "expected_outputs": [
            "docs/reports/2026-07-05-fps2-operator-demo-command.md",
            "docs/reports/2026-07-05-fps3-readiness-checklist.md",
            "docs/reports/2026-07-05-firm-facing-product-surface-close-report.md",
        ],
        "report_path": _display_path(REPORT_PATH),
        "next_leaf": "FPS4_product_narrative_readme_surface",
    }


def render_markdown(readiness: dict[str, Any]) -> str:
    lines = [
        f"# {readiness['title']}",
        "",
        "> Scope: FPS3 operator readiness checklist for the local firm-facing demo surface.",
        "",
        "## One-Line Result",
        "",
        (
            "The local demo has a concrete install/run path and explicit protected-data boundary."
            if readiness["ok"]
            else "The local demo readiness checklist is incomplete; fix missing files before use."
        ),
        "",
        "## Local Install Path",
        "",
        f"- Python: {readiness['local_install_path']['python']}",
        f"- Dependencies: `{readiness['local_install_path']['dependency_command']}`",
        f"- Runtime shape: {readiness['local_install_path']['runtime_shape']}",
        "",
        "## Run Commands",
        "",
    ]
    lines.extend(f"1. `{command}`" for command in readiness["run_commands"])
    lines.extend(
        [
            "",
            "## Required Files",
            "",
            "| Item | Path | Exists |",
            "|---|---|---|",
        ]
    )
    for name, info in readiness["required_files"].items():
        lines.append(f"| {name} | `{info['path']}` | {info['exists']} |")
    lines.extend(["", "## Protected Boundary", ""])
    lines.extend(f"- {item}" for item in readiness["protected_boundary"])
    lines.extend(["", "## Expected Outputs", ""])
    lines.extend(f"- `{path}`" for path in readiness["expected_outputs"])
    lines.extend(["", "## Missing Files", ""])
    lines.extend(f"- {item}" for item in readiness["missing_files"]) if readiness["missing_files"] else lines.append("- none")
    lines.extend(
        [
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps(readiness, ensure_ascii=False, indent=2, default=str),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH) -> dict[str, Any]:
    readiness = build_readiness()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(readiness), encoding="utf-8")
    return readiness


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the FPS3 firm-facing readiness checklist.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    readiness = write_report(args.out) if args.write else build_readiness()
    if args.format == "json":
        print(json.dumps(readiness, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(readiness), end="")
    else:
        print(readiness["title"])
        print(f"- ok: {readiness['ok']}")
        print(f"- missing files: {readiness['missing_files']}")
        print(f"- next leaf: {readiness['next_leaf']}")
    return 0 if readiness["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
