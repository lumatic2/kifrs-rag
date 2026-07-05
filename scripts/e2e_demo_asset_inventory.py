from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-e2e1-demo-asset-inventory.md"

PROTECTED_TERMS = (
    "api_key",
    "token",
    "secret",
    "password",
    "data/dogfood",
    "data/standards",
    "embedding",
    "kifrs.db",
)


def build_demo_asset_inventory() -> dict[str, Any]:
    stages = [
        _stage(
            order=1,
            stage_id="parser",
            title="Local Parser Prototype",
            operator_question="Can the toolkit ingest local accounting files without exposing protected content?",
            evidence="docs/reports/2026-07-05-real-local-parser-prototype-close-report.md",
            demo_point="A local-safe fixture parser path exists with deletion simulation and leak checks.",
            next_step="Move parsed structured facts into authorized evidence lanes.",
        ),
        _stage(
            order=2,
            stage_id="source_lane",
            title="Controlled Source Lane",
            operator_question="Can non-IFRS source material be handled as an authorized RAG lane?",
            evidence="docs/reports/2026-07-05-source-body-ingestion-controlled-lane-close-report.md",
            demo_point="A controlled synthetic source lane has policy, chunking, retrieval, and close evidence.",
            next_step="Use the source lane as supporting evidence for workflow output.",
        ),
        _stage(
            order=3,
            stage_id="workflow",
            title="Workflow Coverage Expansion",
            operator_question="Can the system produce decision-prep output beyond the original 1109/1116 path?",
            evidence="docs/reports/2026-07-05-workflow-coverage-expansion-close-report.md",
            demo_point="A 1037 provisions workflow adapter produces conditional decision-prep evidence.",
            next_step="Show the output as review-ready draft material, not final accounting judgment.",
        ),
        _stage(
            order=4,
            stage_id="retriever",
            title="Runtime Retriever Promotion Gate",
            operator_question="Does the demo explain why the stronger retriever is not default yet?",
            evidence="docs/reports/2026-07-05-runtime-retriever-promotion-gate-close-report.md",
            demo_point="Default promotion is deliberately deferred with regression, latency, and rollback evidence.",
            next_step="Keep the demo honest about quality boundaries and explicit promotion authorization.",
        ),
        _stage(
            order=5,
            stage_id="operator",
            title="Operator Experience Hardening",
            operator_question="Can an operator discover commands, diagnose failures, navigate reports, and recover?",
            evidence="docs/reports/2026-07-05-operator-experience-hardening-close-report.md",
            demo_point="Command inventory, run doctor, report manifest, and recovery playbook are available.",
            next_step="Build one scenario contract and packet from these pieces.",
        ),
    ]
    checks = {
        "stage_ordered": [stage["order"] for stage in stages] == sorted(stage["order"] for stage in stages),
        "stage_ids_unique": len({stage["stage_id"] for stage in stages}) == len(stages),
        "all_evidence_exists": all(stage["evidence_exists"] for stage in stages),
        "all_operator_questions_present": all(stage["operator_question"] for stage in stages),
        "all_demo_points_present": all(stage["demo_point"] for stage in stages),
        "protected_paths_absent": all(_is_public_safe_reference(stage["evidence"]) for stage in stages),
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "E2E1 Demo Asset Inventory And Storyboard",
        "ok": not errors,
        "horizon": "end-to-end-demo-scenario",
        "completed_milestone": "E2E1",
        "storyboard": {
            "one_line": (
                "A firm-facing operator can show local-safe intake, controlled source evidence, "
                "decision-prep workflow output, conservative retriever promotion, and recoverable "
                "operator navigation as one demo."
            ),
            "audience": "Accounting Advisory / Financial Statement support operator",
            "boundary": "public-safe reports only; no protected local data or final accounting judgment",
        },
        "stages": stages,
        "checks": checks,
        "errors": errors,
        "next_leaf": "E2E2_scenario_contract",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    story = result["storyboard"]
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: public-safe inventory of the reports needed for one firm-facing end-to-end demo.",
        "",
        "## 한 줄 결론",
        "",
        story["one_line"],
        "",
        "## Demo Storyboard",
        "",
        f"- Audience: {story['audience']}",
        f"- Boundary: {story['boundary']}",
        "",
        "| Order | Stage | Operator Question | Evidence | Exists | Demo Point |",
        "|---:|---|---|---|---|---|",
    ]
    for stage in result["stages"]:
        lines.append(
            "| {order} | {title} | {question} | `{evidence}` | {exists} | {point} |".format(
                order=stage["order"],
                title=stage["title"],
                question=stage["operator_question"],
                evidence=stage["evidence"],
                exists=stage["evidence_exists"],
                point=stage["demo_point"],
            )
        )
    lines.extend(["", "## Checks", "", "| Check | OK |", "|---|---|"])
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
    result = build_demo_asset_inventory()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _stage(
    *,
    order: int,
    stage_id: str,
    title: str,
    operator_question: str,
    evidence: str,
    demo_point: str,
    next_step: str,
) -> dict[str, Any]:
    return {
        "order": order,
        "stage_id": stage_id,
        "title": title,
        "operator_question": operator_question,
        "evidence": evidence,
        "evidence_exists": (ROOT / evidence).exists(),
        "demo_point": demo_point,
        "next_step": next_step,
    }


def _is_public_safe_reference(value: str) -> bool:
    normalized = value.replace("\\", "/").lower()
    return not any(term in normalized for term in PROTECTED_TERMS)


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build E2E1 demo asset inventory and storyboard.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_demo_asset_inventory()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- stages: {len(result['stages'])}")
        print(f"- next leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
