from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-e2e2-scenario-contract.md"


def build_scenario_contract() -> dict[str, Any]:
    stages = [
        _contract_stage(
            stage_id="parser",
            input_signal="Local-safe accounting document fixture or extracted structured facts",
            evidence="docs/reports/2026-07-05-real-local-parser-prototype-close-report.md",
            output="Structured facts and deletion/leak-check evidence",
            review_checkpoint="Confirm no protected local payload is displayed in the demo output.",
            operator_command="python scripts\\parser_prototype_asset_inventory.py --format text",
            failure_boundary="If local fixture evidence is missing, stop before claiming real-file parser readiness.",
        ),
        _contract_stage(
            stage_id="source_lane",
            input_signal="Authorized synthetic interpretive source record",
            evidence="docs/reports/2026-07-05-source-body-ingestion-controlled-lane-close-report.md",
            output="Controlled source policy, chunking, and retrieval gate evidence",
            review_checkpoint="Confirm source use is authorized and synthetic/public-safe.",
            operator_command="python scripts\\controlled_lane_close_gate.py --format text",
            failure_boundary="If source authorization is absent, do not run ingestion or retrieval claims.",
        ),
        _contract_stage(
            stage_id="workflow",
            input_signal="Provision workflow fixture and authority-separated evidence",
            evidence="docs/reports/2026-07-05-workflow-coverage-expansion-close-report.md",
            output="Conditional decision-prep adapter output and coverage metric update",
            review_checkpoint="Confirm output is review-ready draft material, not final accounting judgment.",
            operator_command="python scripts\\workflow_coverage_close_gate.py --format text",
            failure_boundary="If required evidence is incomplete, label the workflow partial and route to human review.",
        ),
        _contract_stage(
            stage_id="retriever",
            input_signal="Opt-in repair retriever evaluation and rollback evidence",
            evidence="docs/reports/2026-07-05-runtime-retriever-promotion-gate-close-report.md",
            output="Promotion result, regression/latency status, and rollback policy",
            review_checkpoint="Confirm default promotion remains deferred without explicit authorization.",
            operator_command="python scripts\\runtime_retriever_promotion_close_gate.py --format text",
            failure_boundary="If regression or rollback evidence is weak, keep current default retriever.",
        ),
        _contract_stage(
            stage_id="operator",
            input_signal="Command inventory, run doctor, report manifest, and recovery playbook",
            evidence="docs/reports/2026-07-05-operator-experience-hardening-close-report.md",
            output="Run, diagnose, navigate, and recover operator path",
            review_checkpoint="Confirm the operator can recover from missing reports with explicit rerun commands.",
            operator_command="python scripts\\operator_experience_close_gate.py --format text",
            failure_boundary="If commands or reports are not discoverable, demo packet is not ready.",
        ),
    ]
    required_keys = {
        "stage_id",
        "input_signal",
        "evidence",
        "evidence_exists",
        "output",
        "review_checkpoint",
        "operator_command",
        "failure_boundary",
    }
    checks = {
        "all_stages_have_required_keys": all(required_keys.issubset(stage) for stage in stages),
        "all_evidence_exists": all(stage["evidence_exists"] for stage in stages),
        "all_review_checkpoints_present": all(stage["review_checkpoint"] for stage in stages),
        "all_failure_boundaries_present": all(stage["failure_boundary"] for stage in stages),
        "all_operator_commands_present": all(stage["operator_command"] for stage in stages),
        "final_judgment_boundary_present": any("not final accounting judgment" in stage["review_checkpoint"] for stage in stages),
        "authorization_boundary_present": any("authorization" in stage["failure_boundary"].lower() for stage in stages),
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "E2E2 Scenario Contract",
        "ok": not errors,
        "horizon": "end-to-end-demo-scenario",
        "completed_milestone": "E2E2",
        "contract": {
            "scenario_id": "public_safe_firm_demo_v1",
            "audience": "Accounting Advisory / Financial Statement support operator",
            "claim": "The toolkit can walk a public-safe accounting decision-prep demo from local intake boundary to operator recovery.",
            "non_claims": [
                "It does not replace final accounting judgment.",
                "It does not prove production deployment readiness.",
                "It does not expose protected local data.",
            ],
        },
        "stages": stages,
        "checks": checks,
        "errors": errors,
        "next_leaf": "E2E3_demo_packet_builder",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    contract = result["contract"]
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: stage-level contract for the end-to-end public-safe firm demo.",
        "",
        "## 한 줄 결론",
        "",
        contract["claim"],
        "",
        "## Contract",
        "",
        f"- Scenario: `{contract['scenario_id']}`",
        f"- Audience: {contract['audience']}",
        "",
        "## Non-Claims",
        "",
    ]
    lines.extend(f"- {item}" for item in contract["non_claims"])
    lines.extend(
        [
            "",
            "## Stages",
            "",
            "| Stage | Input | Evidence | Output | Review Checkpoint | Failure Boundary |",
            "|---|---|---|---|---|---|",
        ]
    )
    for stage in result["stages"]:
        lines.append(
            "| {stage} | {input_signal} | `{evidence}` | {output} | {review} | {failure} |".format(
                stage=stage["stage_id"],
                input_signal=stage["input_signal"],
                evidence=stage["evidence"],
                output=stage["output"],
                review=stage["review_checkpoint"],
                failure=stage["failure_boundary"],
            )
        )
    lines.extend(["", "## Operator Commands", "", "| Stage | Command |", "|---|---|"])
    for stage in result["stages"]:
        lines.append(f"| {stage['stage_id']} | `{stage['operator_command']}` |")
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
    result = build_scenario_contract()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _contract_stage(
    *,
    stage_id: str,
    input_signal: str,
    evidence: str,
    output: str,
    review_checkpoint: str,
    operator_command: str,
    failure_boundary: str,
) -> dict[str, Any]:
    return {
        "stage_id": stage_id,
        "input_signal": input_signal,
        "evidence": evidence,
        "evidence_exists": (ROOT / evidence).exists(),
        "output": output,
        "review_checkpoint": review_checkpoint,
        "operator_command": operator_command,
        "failure_boundary": failure_boundary,
    }


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build E2E2 scenario contract.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_scenario_contract()
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
