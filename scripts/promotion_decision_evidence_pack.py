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
from scripts.failure_boundary_matrix import build_matrix  # noqa: E402
from scripts.rag_quality_final_gate import TARGET_RETRIEVER, build_report as build_rag_quality_report  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-ptq4-promotion-decision-evidence.md"
CURRENT_DEFAULT = "hybrid"


def build_evidence_pack() -> dict[str, Any]:
    rag_quality = build_rag_quality_report()
    default_guard = check_default_retriever_guard()
    failure_matrix = build_matrix()
    blockers = []
    if not rag_quality["ok"]:
        blockers.append("rag quality final gate is not passing")
    if not default_guard["ok"]:
        blockers.append("default retriever guard is not passing")
    if default_guard["promote_to_default"] is not True:
        blockers.append("explicit promotion authorization is absent")
    if not failure_matrix["ok"]:
        blockers.append("failure boundary matrix is not passing")

    promote = not blockers
    decision = "promote" if promote else "defer"
    return {
        "title": "PTQ4 Promotion Decision Evidence Pack",
        "ok": rag_quality["ok"] and default_guard["ok"] and failure_matrix["ok"],
        "horizon": "product-trust-and-quality-evidence",
        "milestone": "PTQ4",
        "decision": decision,
        "promote_to_default": promote,
        "current_default": CURRENT_DEFAULT,
        "target_retriever": TARGET_RETRIEVER,
        "evidence": {
            "rag_quality_ok": rag_quality["ok"],
            "target_recall20": rag_quality["target_recall20"],
            "target_absent_citations": rag_quality["target_buckets"]["absent"],
            "default_guard_ok": default_guard["ok"],
            "target_exposed_in_mcp": default_guard["target_retriever_exposed_in_mcp"],
            "cached_promotion_decision": default_guard["promotion_decision"],
            "failure_matrix_ok": failure_matrix["ok"],
            "failure_categories": [row["category"] for row in failure_matrix["boundaries"]],
        },
        "blockers": blockers,
        "operator_policy": [
            "Keep runtime default retriever as hybrid.",
            f"Use {TARGET_RETRIEVER} as opt-in evaluation/demo repair evidence only.",
            "A future default change requires explicit authorization and separate implementation.",
            "If RAG/citation failures appear, follow PTQ3 failure boundary actions before trusting output.",
        ],
        "report_path": _display_path(REPORT_PATH),
        "next_leaf": "PTQ5_trust_quality_close_gate",
    }


def render_markdown(pack: dict[str, Any]) -> str:
    lines = [
        f"# {pack['title']}",
        "",
        "> Scope: PTQ4 product-facing evidence for retriever promotion decision.",
        "",
        "## One-Line Result",
        "",
        (
            "Default retriever promotion remains deferred; the repair retriever stays opt-in until explicit authorization and separate implementation."
            if pack["decision"] == "defer"
            else "Evidence supports default retriever promotion, pending separate implementation."
        ),
        "",
        "## Decision",
        "",
        f"- decision: `{pack['decision']}`",
        f"- promote to default: {pack['promote_to_default']}",
        f"- current default: `{pack['current_default']}`",
        f"- target retriever: `{pack['target_retriever']}`",
        "",
        "## Evidence",
        "",
        "| Evidence | Value |",
        "|---|---|",
    ]
    for key, value in pack["evidence"].items():
        lines.append(f"| {key} | `{value}` |")
    lines.extend(["", "## Blockers", ""])
    lines.extend(f"- {blocker}" for blocker in pack["blockers"]) if pack["blockers"] else lines.append("- none")
    lines.extend(["", "## Operator Policy", ""])
    lines.extend(f"- {policy}" for policy in pack["operator_policy"])
    lines.extend(
        [
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps(pack, ensure_ascii=False, indent=2, default=str),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH) -> dict[str, Any]:
    pack = build_evidence_pack()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(pack), encoding="utf-8")
    return pack


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build PTQ4 retriever promotion decision evidence pack.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    pack = write_report(args.out) if args.write else build_evidence_pack()
    if args.format == "json":
        print(json.dumps(pack, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(pack), end="")
    else:
        print(pack["title"])
        print(f"- ok: {pack['ok']}")
        print(f"- decision: {pack['decision']}")
        print(f"- promote_to_default: {pack['promote_to_default']}")
        print(f"- blockers: {pack['blockers']}")
        print(f"- next leaf: {pack['next_leaf']}")
    return 0 if pack["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
