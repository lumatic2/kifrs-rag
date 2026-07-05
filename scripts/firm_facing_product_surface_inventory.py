from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-fps1-product-surface-inventory.md"


@dataclass(frozen=True)
class Surface:
    name: str
    path: str
    category: str
    use: str


SURFACES = (
    Surface("legacy markdown demo pack", "scripts/demo_poc.py", "demo", "Existing multi-file markdown demo, mostly 1115-centric."),
    Surface("multi-authority runtime gate", "scripts/multi_authority_runtime_gate.py", "gate", "Proves five evidence groups render separately."),
    Surface("client-private parser runtime gate", "scripts/client_private_parser_runtime_gate.py", "gate", "Proves structured-facts-only private parser runtime and deletion close."),
    Surface("1116 review pack", "kifrs/workflows/kifrs1116/review_pack.py", "workflow", "Best first walkthrough because it has memo, journal entry, disclosure, checklist, and human review questions."),
    Surface("1109 review pack", "kifrs/workflows/kifrs1109/review_pack.py", "workflow", "Useful second demo for financial instruments classification."),
    Surface("1115 review pack", "kifrs/workflows/kifrs1115/review_pack.py", "workflow", "Useful second demo for revenue scenarios."),
    Surface("statement draft adapters", "kifrs/workflows/statement_draft/adapters.py", "workflow", "Turns review packs into statement line candidates."),
    Surface("audit analytics", "kifrs/workflows/audit_analytics/metrics.py", "workflow", "Adds analytical-procedure review links."),
    Surface("product objective", "docs/OBJECTIVE.md", "narrative", "States the accounting intelligence product objective."),
    Surface("roadmap", "ROADMAP.md", "narrative", "Tracks current horizon and next leaf."),
)


def build_inventory() -> dict[str, Any]:
    surfaces = [
        {
            "name": surface.name,
            "path": surface.path,
            "category": surface.category,
            "use": surface.use,
            "exists": (ROOT / surface.path).exists(),
        }
        for surface in SURFACES
    ]
    errors = [f"missing surface: {surface['path']}" for surface in surfaces if not surface["exists"]]
    recommended_flow = {
        "id": "lease-review-pack-authority-private-boundary",
        "label": "1116 lease review pack with authority and private-runtime boundary",
        "why": "It is the most complete and easiest firm-facing walkthrough: memo, journal entry, disclosure, checklist, authority boundary, and private parser boundary can be shown together.",
        "steps": [
            "Generate 1116 simple lease review pack.",
            "Render primary/supporting/legal/fact/client-private authority boundary.",
            "Show client-private parser runtime contract and deletion gate as local-only boundary.",
            "Attach verification status from multi-authority and client-private runtime gates.",
        ],
    }
    gaps = [
        {
            "milestone": "FPS2",
            "gap": "No single operator demo command generates the recommended walkthrough packet yet.",
        },
        {
            "milestone": "FPS3",
            "gap": "Readiness checklist and local install/run path are scattered across reports and ROADMAP.",
        },
        {
            "milestone": "FPS4",
            "gap": "Product narrative does not yet plainly explain current capabilities, limits, and demo command in one surface.",
        },
        {
            "milestone": "FPS5",
            "gap": "No firm-facing surface close gate checks demo packet, readiness, narrative, and carried runtime/RAG gates together.",
        },
    ]
    return {
        "title": "FPS1 Product Surface Inventory",
        "ok": not errors,
        "horizon": "firm-facing-product-surface",
        "milestone": "FPS1",
        "surfaces": surfaces,
        "recommended_flow": recommended_flow,
        "gaps": gaps,
        "errors": errors,
        "next_leaf": "FPS2_operator_demo_command",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(inventory: dict[str, Any]) -> str:
    flow = inventory["recommended_flow"]
    lines = [
        f"# {inventory['title']}",
        "",
        "> Scope: FPS1 inventory for the first operator-facing local product surface.",
        "",
        "## Result",
        "",
        f"- ok: {inventory['ok']}",
        f"- horizon: `{inventory['horizon']}`",
        f"- milestone: `{inventory['milestone']}`",
        f"- next leaf: `{inventory['next_leaf']}`",
        "",
        "## Existing Surfaces",
        "",
        "| Surface | Path | Category | Use |",
        "|---|---|---|---|",
    ]
    for surface in inventory["surfaces"]:
        lines.append(f"| {surface['name']} | `{surface['path']}` | {surface['category']} | {surface['use']} |")
    lines.extend(
        [
            "",
            "## Recommended First Demo Flow",
            "",
            f"- id: `{flow['id']}`",
            f"- label: {flow['label']}",
            f"- why: {flow['why']}",
            "",
            "### Steps",
            "",
        ]
    )
    lines.extend(f"- {step}" for step in flow["steps"])
    lines.extend(
        [
            "",
            "## Implementation Gaps",
            "",
            "| Milestone | Gap |",
            "|---|---|",
        ]
    )
    for gap in inventory["gaps"]:
        lines.append(f"| {gap['milestone']} | {gap['gap']} |")
    lines.extend(["", "## Errors", ""])
    lines.extend(f"- {error}" for error in inventory["errors"]) if inventory["errors"] else lines.append("- none")
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


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Inventory firm-facing product surface candidates.")
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
        print(f"- recommended flow: {inventory['recommended_flow']['id']}")
        print(f"- next leaf: {inventory['next_leaf']}")
    return 0 if inventory["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
