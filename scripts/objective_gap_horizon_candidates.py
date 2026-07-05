from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-objective-gap-horizon-candidates.md"


@dataclass(frozen=True)
class GapHorizon:
    order: int
    horizon_id: str
    objective_gap: str
    why_now: str
    status: str
    first_milestone: str
    evidence_target: str


def build_candidates() -> dict[str, Any]:
    candidates = [
        GapHorizon(
            order=1,
            horizon_id="rag-quality-fresh-validation",
            objective_gap="Default retrieval quality is still deferred; the strongest retriever is not yet trusted as a product default.",
            why_now="Every accountant-facing workflow depends on retrieval trust, so this should run before deeper source/parser expansion.",
            status="closed",
            first_milestone="RQF1 validation corpus and acceptance contract",
            evidence_target="docs/reports/2026-07-05-rqf1-validation-contract.md",
        ),
        GapHorizon(
            order=2,
            horizon_id="private-parser-realism-hardening",
            objective_gap="Local parser evidence is still fixture-heavy; actual local-file adapter evidence remains gated by explicit authorization.",
            why_now="The objective needs realistic client-input handling, but protected payloads must stay local and authorization-gated.",
            status="closed",
            first_milestone="PPR1 authorization-safe adapter proof plan",
            evidence_target="docs/reports/2026-07-05-ppr1-authorization-safe-adapter-proof.md",
        ),
        GapHorizon(
            order=3,
            horizon_id="external-source-body-connector-expansion",
            objective_gap="External sources have metadata/demo evidence, but broader source-body connector implementation is still missing.",
            why_now="Accounting work needs regulator, interpretive, legal, filing, and policy evidence beyond K-IFRS paragraphs.",
            status="closed",
            first_milestone="ESB1 source-body connector selection and policy gate",
            evidence_target="docs/reports/2026-07-05-esb1-source-body-connector-selection.md",
        ),
        GapHorizon(
            order=4,
            horizon_id="workflow-coverage-depth-expansion",
            objective_gap="Automation coverage is strong in selected workflows but still shallow against the full firm-service map.",
            why_now="The north-star question asks how far accountant work can be automated, which requires broader workflow sampling.",
            status="closed",
            first_milestone="WCD1 service-line coverage rerank",
            evidence_target="docs/reports/2026-07-05-wcd1-service-line-coverage-rerank.md",
        ),
        GapHorizon(
            order=5,
            horizon_id="demo-rehearsal-quality-loop",
            objective_gap="The demo packet is ready, but it has not been rehearsed into repeatable operator evidence and quality notes.",
            why_now="Before any external step, the local demo needs timed, repeatable, failure-aware rehearsal evidence.",
            status="closed",
            first_milestone="DRQ1 demo rehearsal script and timing gate",
            evidence_target="docs/reports/2026-07-05-drq1-demo-rehearsal-script.md",
        ),
    ]
    return {
        "title": "Objective Gap Horizon Candidates",
        "objective": "Group the remaining objective gaps into implementation horizons and run them with the product harness.",
        "active_horizon": "none",
        "candidates": [asdict(candidate) for candidate in candidates],
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: post-demo horizon queue derived from the current Objective gap audit.",
        "",
        "## Objective",
        "",
        result["objective"],
        "",
    ]
    lines.extend(
        [
            "## Recommended Horizon Queue",
            "",
            "| # | Horizon | Objective Gap | Why Now | Status | First Milestone | Evidence Target |",
            "|---:|---|---|---|---|---|---|",
        ]
    )
    for candidate in result["candidates"]:
        lines.append(
            "| {order} | `{horizon_id}` | {objective_gap} | {why_now} | {status} | {first_milestone} | `{evidence_target}` |".format(
                **candidate
            )
        )
    lines.extend(
        [
            "",
            "## Decision",
            "",
            f"- Active horizon: `{result['active_horizon']}`",
            "- The five-horizon objective gap queue is closed.",
            "- Keep the queue focused on internal product evidence, quality, and workflow coverage.",
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
    parser = argparse.ArgumentParser(description="Render Objective gap horizon candidates.")
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
