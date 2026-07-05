from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-product-weakness-horizon-candidates.md"


@dataclass(frozen=True)
class HorizonCandidate:
    order: int
    horizon_id: str
    weakness: str
    product_value: str
    status: str
    plan: str
    first_milestone: str


def build_candidates() -> dict[str, Any]:
    candidates = [
        HorizonCandidate(
            order=1,
            horizon_id="real-local-parser-prototype",
            weakness="Local private inputs are still mostly represented by contracts and synthetic parser dry-runs.",
            product_value="Moves the toolkit toward realistic local-file handling while preserving structured-facts-only public output.",
            status="closed",
            plan="docs/plans/2026-07-05-real-local-parser-prototype.md",
            first_milestone="RLP1 parser prototype asset inventory",
        ),
        HorizonCandidate(
            order=2,
            horizon_id="source-body-ingestion-controlled-lane",
            weakness="K-IFRS-only evidence is insufficient for real accounting work that also needs interpretive, regulatory, legal, filing, and private facts.",
            product_value="Proves one non-IFRS source lane can be policy-bound, parsed, chunked, retrieved, and reported safely.",
            status="closed",
            plan="docs/plans/2026-07-05-source-body-ingestion-controlled-lane.md",
            first_milestone="SBI1 source class selection and authorization boundary",
        ),
        HorizonCandidate(
            order=3,
            horizon_id="workflow-coverage-expansion",
            weakness="Automation proof is concentrated in a narrow set of standards and review-pack surfaces.",
            product_value="Expands the firm-service map into another testable accountant workflow and updates coverage evidence.",
            status="closed",
            plan="docs/plans/2026-07-05-workflow-coverage-expansion.md",
            first_milestone="WCE1 coverage gap ranking",
        ),
        HorizonCandidate(
            order=4,
            horizon_id="runtime-retriever-promotion-gate",
            weakness="The strongest retriever remains opt-in and has not been converted into a reversible product-default decision.",
            product_value="Creates a promote/defer/rollback gate for runtime retrieval quality.",
            status="closed",
            plan="docs/plans/2026-07-05-runtime-retriever-promotion-gate.md",
            first_milestone="RPG1 promotion evidence inventory",
        ),
        HorizonCandidate(
            order=5,
            horizon_id="operator-experience-hardening",
            weakness="The toolkit has many scripts and reports, but the operator path is difficult to discover and recover.",
            product_value="Turns the local toolkit into a run, diagnose, navigate, and recover experience.",
            status="closed",
            plan="docs/plans/2026-07-05-operator-experience-hardening.md",
            first_milestone="OEH1 operator command inventory",
        ),
    ]
    return {
        "title": "Product Weakness Horizon Candidates",
        "objective": "Use the next five horizons to close the remaining product weaknesses before packaging or external PoC.",
        "active_horizon": "none",
        "candidates": [asdict(candidate) for candidate in candidates],
        "parked": [
            {
                "horizon_id": "end-to-end-demo-scenario",
                "reason": "Should integrate the five horizons above instead of preceding them.",
            },
            {
                "horizon_id": "real-accountant-session",
                "reason": "User-owned external outreach remains parked until explicitly reopened.",
            },
        ],
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: product weakness based horizon queue for the next Accounting Intelligence work.",
        "",
        "## Objective",
        "",
        result["objective"],
        "",
        "## Recommended Queue",
        "",
        "| # | Horizon | Weakness Closed | Product Value | Status | First Milestone |",
        "|---|---|---|---|---|---|",
    ]
    for candidate in result["candidates"]:
        lines.append(
            "| {order} | `{horizon_id}` | {weakness} | {product_value} | {status} | {first_milestone} |".format(
                **candidate
            )
        )
    lines.extend(
        [
            "",
            "## Parked",
            "",
        ]
    )
    for item in result["parked"]:
        lines.append(f"- `{item['horizon_id']}` — {item['reason']}")
    lines.extend(
        [
            "",
            "## Decision",
            "",
            "- `real-local-parser-prototype` is closed.",
            "- `source-body-ingestion-controlled-lane` is closed.",
            "- `workflow-coverage-expansion` is closed.",
            "- `runtime-retriever-promotion-gate` is closed.",
            "- `operator-experience-hardening` is closed.",
            "- The current five-horizon product weakness queue is closed.",
            "- Do not reopen actual outreach or feedback capture unless the user explicitly asks.",
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
    result = build_candidates()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Render product weakness horizon candidates.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_candidates()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- active horizon: {result['active_horizon']}")
        for candidate in result["candidates"]:
            print(f"- {candidate['order']}. {candidate['horizon_id']}: {candidate['status']}")


if __name__ == "__main__":
    main()
