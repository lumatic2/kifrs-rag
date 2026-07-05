from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-ptq3-failure-boundary-matrix.md"


@dataclass(frozen=True)
class FailureBoundary:
    category: str
    symptom: str
    operator_action: str
    verification_command: str
    escalation: str
    public_safe: bool = True


BOUNDARIES = (
    FailureBoundary(
        "retrieval_quality",
        "Required citation is absent or outside the accepted retrieval window.",
        "Run the RAG final gate and inspect target misses before trusting a generated answer.",
        "python scripts\\rag_quality_final_gate.py --format text",
        "Do not promote the repair retriever or rely on the answer until misses are triaged.",
    ),
    FailureBoundary(
        "citation_assembly",
        "Workflow output has a memo or disclosure draft but missing or weak citations.",
        "Check review-pack confidence labels and keep the affected section at caution or human_review_required.",
        "python scripts\\review_pack_confidence_contract.py --format text",
        "Require accountant review of the affected memo/disclosure section.",
    ),
    FailureBoundary(
        "client_private_fact_gap",
        "The accounting conclusion depends on source facts that are only present in private client material.",
        "Keep the private fact in the client_private_fact lane and verify deletion/runtime gate.",
        "python scripts\\client_private_parser_runtime_gate.py --format text",
        "Do not copy private source body into public reports; request structured facts or local-only review.",
    ),
    FailureBoundary(
        "unsupported_workflow",
        "Review pack status is needs_human_review or the requested workflow has no supported adapter.",
        "Use the human-review checklist and stop before final conclusion.",
        "python -m pytest tests\\test_1116_review_pack.py tests\\test_1109_review_pack.py tests\\test_1115_review_pack.py -q",
        "Create a new workflow coverage milestone before claiming automation.",
    ),
    FailureBoundary(
        "authority_boundary",
        "Primary, supporting, legal, fact, and private authority groups are mixed or missing.",
        "Run the multi-authority runtime gate and inspect role counts.",
        "python scripts\\multi_authority_runtime_gate.py --format text",
        "Do not present the output as grounded until authority groups are separated.",
    ),
    FailureBoundary(
        "default_promotion",
        "The opt-in repair retriever appears better than default but promotion is not authorized.",
        "Run the default retriever guard and keep runtime default unchanged.",
        "python scripts\\default_retriever_guard.py --format text",
        "Require explicit authorization and a separate implementation before changing defaults.",
    ),
)


def build_matrix() -> dict[str, Any]:
    rows = [asdict(boundary) for boundary in BOUNDARIES]
    errors: list[str] = []
    categories = {row["category"] for row in rows}
    required = {
        "retrieval_quality",
        "citation_assembly",
        "client_private_fact_gap",
        "unsupported_workflow",
        "authority_boundary",
        "default_promotion",
    }
    missing = sorted(required - categories)
    if missing:
        errors.append(f"missing failure categories: {missing}")
    for row in rows:
        if not row["verification_command"].startswith(("python ", "python -m ")):
            errors.append(f"{row['category']}: verification command must be directly runnable")
        if row["public_safe"] is not True:
            errors.append(f"{row['category']}: boundary must be public-safe")
    return {
        "title": "PTQ3 Failure Boundary Matrix",
        "ok": not errors,
        "horizon": "product-trust-and-quality-evidence",
        "milestone": "PTQ3",
        "boundaries": rows,
        "errors": errors,
        "report_path": _display_path(REPORT_PATH),
        "next_leaf": "PTQ4_promotion_decision_evidence_pack",
    }


def render_markdown(matrix: dict[str, Any]) -> str:
    lines = [
        f"# {matrix['title']}",
        "",
        "> Scope: PTQ3 operator actions for known product trust failure boundaries.",
        "",
        "## One-Line Result",
        "",
        (
            "Known failure modes now map to operator actions, verification commands, and escalation boundaries."
            if matrix["ok"]
            else "Failure boundary matrix failed; fix listed errors."
        ),
        "",
        "## Matrix",
        "",
        "| Category | Symptom | Operator Action | Verify | Escalation |",
        "|---|---|---|---|---|",
    ]
    for row in matrix["boundaries"]:
        lines.append(
            f"| {row['category']} | {row['symptom']} | {row['operator_action']} | `{row['verification_command']}` | {row['escalation']} |"
        )
    lines.extend(["", "## Errors", ""])
    lines.extend(f"- {error}" for error in matrix["errors"]) if matrix["errors"] else lines.append("- none")
    lines.extend(
        [
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps(matrix, ensure_ascii=False, indent=2, default=str),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH) -> dict[str, Any]:
    matrix = build_matrix()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(matrix), encoding="utf-8")
    return matrix


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the PTQ3 failure boundary matrix.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    matrix = write_report(args.out) if args.write else build_matrix()
    if args.format == "json":
        print(json.dumps(matrix, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(matrix), end="")
    else:
        print(matrix["title"])
        print(f"- ok: {matrix['ok']}")
        print(f"- categories: {', '.join(row['category'] for row in matrix['boundaries'])}")
        print(f"- next leaf: {matrix['next_leaf']}")
    return 0 if matrix["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
