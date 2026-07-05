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


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-ptq1-trust-evidence-inventory.md"


@dataclass(frozen=True)
class EvidenceSource:
    name: str
    path: str
    evidence_role: str
    speed: str
    public_safe: bool
    protected_data_required: bool
    use_in_product_trust: str


EVIDENCE_SOURCES = (
    EvidenceSource(
        "quality preflight",
        "scripts/quality_preflight.py",
        "baseline public-safe quality gate",
        "fast",
        True,
        False,
        "Shows focused tests, local-rag threshold, authority validators, and user_note audit are passing.",
    ),
    EvidenceSource(
        "RAG quality final gate",
        "scripts/rag_quality_final_gate.py",
        "retrieval and citation quality gate",
        "heavy",
        True,
        True,
        "Shows opt-in repair retriever reaches recall@20 1.000 and absent required citations 0 when local eval data exists.",
    ),
    EvidenceSource(
        "default retriever guard",
        "scripts/default_retriever_guard.py",
        "default-promotion safety gate",
        "fast",
        True,
        False,
        "Shows runtime default remains hybrid and repair retriever is not exposed as MCP default.",
    ),
    EvidenceSource(
        "firm-facing product surface close gate",
        "scripts/firm_facing_product_surface_gate.py",
        "demo surface integration gate",
        "fast",
        True,
        False,
        "Shows demo command, readiness checklist, README narrative, and carried evidence reports are connected.",
    ),
    EvidenceSource(
        "multi-authority runtime gate",
        "scripts/multi_authority_runtime_gate.py",
        "authority-boundary runtime gate",
        "heavy",
        True,
        True,
        "Shows primary/supporting/legal/fact/client-private authority groups are separated and carried regressions pass.",
    ),
    EvidenceSource(
        "client-private parser runtime gate",
        "scripts/client_private_parser_runtime_gate.py",
        "private-runtime boundary gate",
        "heavy",
        True,
        True,
        "Shows structured-facts-only private parser runtime, client_private_fact references, and deletion gate remain connected.",
    ),
    EvidenceSource(
        "FPS2 operator demo packet",
        "docs/reports/2026-07-05-fps2-operator-demo-command.md",
        "operator-visible demo evidence",
        "fast",
        True,
        False,
        "Shows the concrete 1116 walkthrough output a firm-side reviewer sees.",
    ),
    EvidenceSource(
        "firm-facing README narrative",
        "README.md",
        "product claims and non-goals",
        "fast",
        True,
        False,
        "Shows what the product claims, what it does not claim, and the demo command.",
    ),
)


def build_inventory() -> dict[str, Any]:
    sources = [
        {
            "name": source.name,
            "path": source.path,
            "exists": (ROOT / source.path).exists(),
            "evidence_role": source.evidence_role,
            "speed": source.speed,
            "public_safe": source.public_safe,
            "protected_data_required": source.protected_data_required,
            "use_in_product_trust": source.use_in_product_trust,
        }
        for source in EVIDENCE_SOURCES
    ]
    missing = [source["path"] for source in sources if not source["exists"]]
    categories = {
        "fast_public_safe": [source["name"] for source in sources if source["speed"] == "fast" and source["public_safe"]],
        "heavy_regression": [source["name"] for source in sources if source["speed"] == "heavy"],
        "protected_data_dependent": [source["name"] for source in sources if source["protected_data_required"]],
        "operator_visible": [
            source["name"]
            for source in sources
            if source["evidence_role"] in {"operator-visible demo evidence", "product claims and non-goals"}
        ],
    }
    gaps = [
        {
            "milestone": "PTQ2",
            "gap": "Review-pack sections do not yet expose ready/caution/human-review-required confidence labels.",
        },
        {
            "milestone": "PTQ3",
            "gap": "Failure modes are known across reports but not normalized into one operator action matrix.",
        },
        {
            "milestone": "PTQ4",
            "gap": "Retriever promotion decision exists as guardrails but not as a product-facing evidence pack.",
        },
        {
            "milestone": "PTQ5",
            "gap": "No trust-quality close gate yet ties PTQ reports to carried RAG/runtime/product gates.",
        },
    ]
    return {
        "title": "PTQ1 Trust Evidence Inventory",
        "ok": not missing,
        "horizon": "product-trust-and-quality-evidence",
        "milestone": "PTQ1",
        "sources": sources,
        "categories": categories,
        "missing": missing,
        "gaps": gaps,
        "report_path": _display_path(REPORT_PATH),
        "next_leaf": "PTQ2_review_pack_confidence_contract",
    }


def render_markdown(inventory: dict[str, Any]) -> str:
    lines = [
        f"# {inventory['title']}",
        "",
        "> Scope: PTQ1 inventory of evidence sources used to make the firm-facing demo trustable.",
        "",
        "## One-Line Result",
        "",
        (
            "Trust evidence sources are present and classified by product role, speed, public safety, and protected-data dependency."
            if inventory["ok"]
            else "Trust evidence inventory is incomplete; fix missing sources first."
        ),
        "",
        "## Evidence Sources",
        "",
        "| Source | Path | Role | Speed | Public Safe | Protected Data Required | Exists |",
        "|---|---|---|---|---|---|---|",
    ]
    for source in inventory["sources"]:
        lines.append(
            f"| {source['name']} | `{source['path']}` | {source['evidence_role']} | {source['speed']} | {source['public_safe']} | {source['protected_data_required']} | {source['exists']} |"
        )
    lines.extend(["", "## Categories", ""])
    for category, names in inventory["categories"].items():
        lines.append(f"### {category}")
        lines.extend(f"- {name}" for name in names)
        lines.append("")
    lines.extend(["## Gaps To Next Milestones", "", "| Milestone | Gap |", "|---|---|"])
    for gap in inventory["gaps"]:
        lines.append(f"| {gap['milestone']} | {gap['gap']} |")
    lines.extend(["", "## Missing", ""])
    lines.extend(f"- {path}" for path in inventory["missing"]) if inventory["missing"] else lines.append("- none")
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
    parser = argparse.ArgumentParser(description="Inventory product trust evidence sources.")
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
        print(f"- sources: {len(inventory['sources'])}")
        print(f"- missing: {inventory['missing']}")
        print(f"- next leaf: {inventory['next_leaf']}")
    return 0 if inventory["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
