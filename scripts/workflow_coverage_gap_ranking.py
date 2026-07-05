from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-wce1-coverage-gap-ranking.md"


@dataclass(frozen=True)
class WorkflowCandidate:
    candidate_id: str
    service_line: str
    workflow: str
    output: str
    firm_service_value: int
    data_availability: int
    determinism: int
    verification_cost_score: int
    existing_evidence: tuple[str, ...]
    limits: tuple[str, ...]

    @property
    def total_score(self) -> int:
        return (
            self.firm_service_value
            + self.data_availability
            + self.determinism
            + self.verification_cost_score
        )


def build_workflow_coverage_gap_ranking() -> dict[str, Any]:
    candidates = [
        WorkflowCandidate(
            candidate_id="1037_provisions",
            service_line="F-ACC / F-AUD",
            workflow="provision recognition and measurement memo",
            output="decision-prep memo, journal-entry cue, human-review checklist",
            firm_service_value=5,
            data_availability=4,
            determinism=5,
            verification_cost_score=5,
            existing_evidence=(
                "docs/practice-map/team-workflows.md",
                "docs/reports/2026-07-05-rq2-eval-coverage-refresh.md",
                "docs/reports/2026-07-05-source-routed-hybrid-implementation.md",
            ),
            limits=(
                "actual obligating event facts still need local structured input",
                "amount estimation remains human-reviewed unless provided as facts",
            ),
        ),
        WorkflowCandidate(
            candidate_id="disclosure_closing_support",
            service_line="F-ACC / F-AUD",
            workflow="disclosure checklist and closing support pack",
            output="closing checklist, disclosure gap list, review questions",
            firm_service_value=5,
            data_availability=5,
            determinism=4,
            verification_cost_score=4,
            existing_evidence=(
                "docs/practice-map/service-line-candidates.md",
                "docs/reports/2026-07-04-ae2-disclosure-coverage.md",
                "docs/reports/demo-poc/statement-candidates.md",
            ),
            limits=(
                "partly overlaps existing review-pack surfaces",
                "full DART or company note parsing remains outside this milestone",
            ),
        ),
        WorkflowCandidate(
            candidate_id="1036_impairment",
            service_line="F-ACC / F-AUD",
            workflow="impairment indicator and recoverable amount review memo",
            output="impairment trigger memo, missing-facts list, human-review checklist",
            firm_service_value=5,
            data_availability=3,
            determinism=3,
            verification_cost_score=3,
            existing_evidence=(
                "docs/plans/2026-06-30-phase4-content-axis.md",
                "docs/reports/2026-07-05-rq2-eval-coverage-refresh.md",
                "docs/reports/2026-07-05-ro2-term-bridge-candidate-eval.md",
            ),
            limits=(
                "valuation assumptions and cash-flow forecasts cannot be invented",
                "recoverable amount calculation needs external or client facts",
            ),
        ),
        WorkflowCandidate(
            candidate_id="1113_fair_value",
            service_line="F-ACC / F-DEAL",
            workflow="fair value hierarchy and input-level assessment memo",
            output="fair value classification memo and valuation input checklist",
            firm_service_value=5,
            data_availability=3,
            determinism=3,
            verification_cost_score=2,
            existing_evidence=(
                "docs/plans/2026-06-30-p4c4-fair-value-entry.md",
                "docs/OBJECTIVE.md",
                "docs/practice-map/service-line-candidates.md",
            ),
            limits=(
                "market data, model assumptions, and valuation technique selection need human review",
                "too much scope if DCF or option model validation is included now",
            ),
        ),
        WorkflowCandidate(
            candidate_id="1110_consolidation",
            service_line="F-ACC",
            workflow="control assessment and consolidation scope memo",
            output="control indicators matrix, consolidation-scope memo, review checklist",
            firm_service_value=5,
            data_availability=2,
            determinism=3,
            verification_cost_score=2,
            existing_evidence=(
                "docs/practice-map/team-workflows.md",
                "docs/reports/2026-07-05-current-capability-map.md",
            ),
            limits=(
                "group structure, voting rights, contracts, and de facto control facts are fixture-heavy",
                "not enough current repo evidence for a fast first WCE implementation",
            ),
        ),
    ]
    ranked = sorted(candidates, key=lambda item: (-item.total_score, item.candidate_id))
    recommended = ranked[0]
    return {
        "title": "WCE1 Coverage Gap Ranking",
        "ok": True,
        "horizon": "workflow-coverage-expansion",
        "completed_milestone": "WCE1",
        "ranking_basis": {
            "firm_service_value": "clear accounting-firm team, workflow, and output fit",
            "data_availability": "can be exercised with public-safe or synthetic structured facts",
            "determinism": "can produce a bounded decision-prep draft without inventing facts",
            "verification_cost_score": "higher means cheaper to verify locally",
        },
        "ranked_candidates": [
            _candidate_to_dict(candidate, rank=index + 1) for index, candidate in enumerate(ranked)
        ],
        "recommended_candidate": recommended.candidate_id,
        "recommended_next_contract": {
            "candidate_id": recommended.candidate_id,
            "workflow": recommended.workflow,
            "output": recommended.output,
            "reason": "It is a high-value F-ACC/F-AUD workflow, has existing 1037 retrieval/eval evidence, is deterministic enough for a decision-prep memo, and can be verified without live private data.",
        },
        "not_reopened": [
            "external accountant outreach",
            "actual feedback capture",
            "real client document intake",
        ],
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: rank the next accountant workflow candidate for workflow coverage expansion.",
        "",
        "## 한 줄 결론",
        "",
        (
            "`1037_provisions` should be the next workflow contract: it is valuable to F-ACC/F-AUD, bounded enough for decision-prep output, and cheap to verify with existing evidence."
        ),
        "",
        "## Ranking Basis",
        "",
        "| Criterion | Meaning |",
        "|---|---|",
    ]
    for name, meaning in result["ranking_basis"].items():
        lines.append(f"| {name} | {meaning} |")
    lines.extend(
        [
            "",
            "## Ranked Candidates",
            "",
            "| Rank | Candidate | Service Line | Workflow | Output | Value | Data | Determinism | Verification | Total |",
            "|---|---|---|---|---|---:|---:|---:|---:|---:|",
        ]
    )
    for candidate in result["ranked_candidates"]:
        lines.append(
            "| {rank} | `{candidate_id}` | {service_line} | {workflow} | {output} | {firm_service_value} | {data_availability} | {determinism} | {verification_cost_score} | {total_score} |".format(
                **candidate
            )
        )
    lines.extend(
        [
            "",
            "## Recommended Next Contract",
            "",
            f"- candidate: `{result['recommended_next_contract']['candidate_id']}`",
            f"- workflow: {result['recommended_next_contract']['workflow']}",
            f"- output: {result['recommended_next_contract']['output']}",
            f"- reason: {result['recommended_next_contract']['reason']}",
            "",
            "## Candidate Limits",
            "",
        ]
    )
    for candidate in result["ranked_candidates"]:
        lines.append(f"### {candidate['candidate_id']}")
        lines.extend(f"- {limit}" for limit in candidate["limits"])
        lines.append("")
    lines.extend(
        [
            "## Boundaries Not Reopened",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in result["not_reopened"])
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
    result = build_workflow_coverage_gap_ranking()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _candidate_to_dict(candidate: WorkflowCandidate, rank: int) -> dict[str, Any]:
    data = asdict(candidate)
    data["rank"] = rank
    data["total_score"] = candidate.total_score
    return data


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Rank WCE1 workflow coverage gap candidates.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_workflow_coverage_gap_ranking()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- recommended candidate: {result['recommended_candidate']}")
        print(f"- next contract: {result['recommended_next_contract']['workflow']}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
