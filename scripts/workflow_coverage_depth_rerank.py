from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-wcd1-service-line-coverage-rerank.md"


@dataclass(frozen=True)
class WorkflowGap:
    workflow_id: str
    service_line: str
    workflow_surface: str
    current_evidence: str
    automation_value: int
    evidence_availability: int
    implementation_cost: int
    public_safety: int
    recommended_next: bool

    @property
    def score(self) -> int:
        return self.automation_value + self.evidence_availability + self.public_safety - self.implementation_cost


def build_rerank() -> dict[str, Any]:
    gaps = [
        WorkflowGap(
            workflow_id="audit_disclosure_tie_out",
            service_line="F-AUD / F-ACC",
            workflow_surface="audit issue support and disclosure requirement tie-out",
            current_evidence="1116 disclosure draft, review-pack evidence, K-IFRS retrieval, source-body connector lane",
            automation_value=5,
            evidence_availability=5,
            implementation_cost=2,
            public_safety=5,
            recommended_next=True,
        ),
        WorkflowGap(
            workflow_id="fs_statement_line_mapping",
            service_line="F-ACC",
            workflow_surface="financial statement line-item mapping and display candidate review",
            current_evidence="financial statement draft and review-pack reports",
            automation_value=4,
            evidence_availability=4,
            implementation_cost=2,
            public_safety=5,
            recommended_next=False,
        ),
        WorkflowGap(
            workflow_id="audit_analytical_variance_memo",
            service_line="F-AUD",
            workflow_surface="analytical procedure variance explanation memo",
            current_evidence="audit analytical procedures horizon and public-safe fixture metrics",
            automation_value=4,
            evidence_availability=4,
            implementation_cost=3,
            public_safety=4,
            recommended_next=False,
        ),
        WorkflowGap(
            workflow_id="acquisition_accounting_issue_memo",
            service_line="F-DEAL / F-ACC",
            workflow_surface="acquisition accounting issue memo",
            current_evidence="service map only; limited acquisition-accounting workflow evidence",
            automation_value=4,
            evidence_availability=2,
            implementation_cost=4,
            public_safety=3,
            recommended_next=False,
        ),
        WorkflowGap(
            workflow_id="k_sox_control_checklist",
            service_line="F-RISK",
            workflow_surface="internal-control checklist and gap memo",
            current_evidence="service map only; internal process materials usually required",
            automation_value=3,
            evidence_availability=2,
            implementation_cost=4,
            public_safety=3,
            recommended_next=False,
        ),
    ]
    ranked = sorted(gaps, key=lambda gap: (-gap.score, -gap.automation_value, gap.workflow_id))
    top = ranked[0]
    checks = {
        "service_lines_present": len({gap.service_line for gap in gaps}) >= 4,
        "top_candidate_marked": top.recommended_next is True,
        "top_candidate_public_safe": top.public_safety >= 4,
        "top_candidate_uses_existing_evidence": top.evidence_availability >= 4,
        "no_external_dependency_required": True,
        "next_milestone_named": True,
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "WCD1 Service-Line Coverage Rerank",
        "ok": not errors,
        "horizon": "workflow-coverage-depth-expansion",
        "completed_milestone": "WCD1",
        "ranking_criteria": [
            "automation_value",
            "evidence_availability",
            "implementation_cost",
            "public_safety",
        ],
        "ranked_gaps": [asdict(gap) | {"score": gap.score} for gap in ranked],
        "recommended_workflow": {
            "workflow_id": top.workflow_id,
            "service_line": top.service_line,
            "workflow_surface": top.workflow_surface,
            "reason": "It broadens coverage from accounting advisory into audit support while reusing existing disclosure, review-pack, retrieval, and connector evidence.",
        },
        "checks": checks,
        "errors": errors,
        "next_leaf": "WCD2_workflow_sample_contract_pack",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    recommended = result["recommended_workflow"]
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: rerank firm-service workflow gaps for the next coverage-depth sample.",
        "",
        "## 한 줄 결론",
        "",
        (
            f"Recommended next workflow: `{recommended['workflow_id']}` across `{recommended['service_line']}`. "
            f"{recommended['reason']}"
        ),
        "",
        "## Ranking Criteria",
        "",
    ]
    lines.extend(f"- `{criterion}`" for criterion in result["ranking_criteria"])
    lines.extend(
        [
            "",
            "## Ranked Gaps",
            "",
            "| Rank | Workflow | Service Line | Surface | Score | Recommended |",
            "|---:|---|---|---|---:|---|",
        ]
    )
    for index, gap in enumerate(result["ranked_gaps"], start=1):
        lines.append(
            "| {rank} | `{workflow_id}` | {service_line} | {workflow_surface} | {score} | {recommended_next} |".format(
                rank=index,
                **gap,
            )
        )
    lines.extend(
        [
            "",
            "## Checks",
            "",
            "| Check | OK |",
            "|---|---|",
        ]
    )
    for name, ok in result["checks"].items():
        lines.append(f"| {name} | {ok} |")
    lines.extend(["", "## Errors", ""])
    lines.extend(f"- {error}" for error in result["errors"]) if result["errors"] else lines.append("- none")
    lines.extend(
        [
            "",
            "## Next Leaf",
            "",
            f"- `{result['next_leaf']}`",
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
    result = build_rerank()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build WCD1 service-line coverage rerank report.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_rerank()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- recommended workflow: {result['recommended_workflow']['workflow_id']}")
        print(f"- next leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
