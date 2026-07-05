from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.workflow_coverage_gap_ranking import build_workflow_coverage_gap_ranking  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-wce2-first-workflow-contract.md"


def build_first_workflow_contract() -> dict[str, Any]:
    ranking = build_workflow_coverage_gap_ranking()
    selected = ranking["recommended_candidate"]
    contract = {
        "workflow_id": selected,
        "service_line": "F-ACC / F-AUD",
        "standard_scope": ["KIFRS1037"],
        "workflow_name": "Provision recognition and measurement decision-prep memo",
        "purpose": "Prepare a bounded accountant-review draft for provision recognition, measurement, journal-entry cues, and missing-facts review questions.",
        "inputs": [
            {
                "name": "obligating_event",
                "required": True,
                "source": "structured local facts",
                "description": "Past event or condition that may create a present obligation.",
            },
            {
                "name": "obligation_type",
                "required": True,
                "source": "structured local facts",
                "description": "Legal, constructive, onerous contract, restructuring, restoration, or other provision category.",
            },
            {
                "name": "outflow_probability",
                "required": True,
                "source": "structured local facts",
                "description": "Management-assessed likelihood bucket; the AI does not invent probability.",
            },
            {
                "name": "estimate_basis",
                "required": False,
                "source": "structured local facts",
                "description": "Management estimate, range, expected value, present-value assumption, or missing estimate marker.",
            },
            {
                "name": "discounting_indicator",
                "required": False,
                "source": "structured local facts",
                "description": "Whether time value of money is material and requires present-value review.",
            },
        ],
        "outputs": [
            "recognition_assessment",
            "measurement_summary",
            "journal_entry_cue",
            "missing_facts",
            "human_review_checklist",
            "authority_panel",
        ],
        "evidence_roles": [
            {
                "role": "primary_kifrs",
                "allowed_sources": ["KIFRS1037"],
                "purpose": "recognition, measurement, disclosure, and present-value boundary",
            },
            {
                "role": "supporting_interpretation",
                "allowed_sources": ["controlled interpretive lane"],
                "purpose": "non-primary explanation only; cannot override K-IFRS",
            },
            {
                "role": "client_private_fact",
                "allowed_sources": ["structured local facts only"],
                "purpose": "facts used by the workflow; not persisted in public output",
            },
        ],
        "human_review_boundary": [
            "final recognition conclusion",
            "probability assessment when not supplied",
            "best estimate, range, and discount rate judgment",
            "legal interpretation of contract enforceability",
            "financial statement materiality and presentation conclusion",
        ],
        "not_implemented": [
            "contract OCR",
            "legal enforceability opinion",
            "automatic best-estimate calculation from raw evidence",
            "default retriever promotion",
            "live external source fetch",
        ],
        "wce1_evidence": ranking["report_path"],
        "next_adapter": "minimal_workflow_review_pack_adapter",
    }
    errors = _validate_contract(contract, expected_workflow_id=selected)
    return {
        "title": "WCE2 First Workflow Candidate Contract",
        "ok": not errors,
        "horizon": "workflow-coverage-expansion",
        "completed_milestone": "WCE2",
        "selected_candidate": selected,
        "contract": contract,
        "errors": errors,
        "report_path": _display_path(REPORT_PATH),
    }


def _validate_contract(contract: dict[str, Any], expected_workflow_id: str) -> list[str]:
    errors: list[str] = []
    if contract.get("workflow_id") != expected_workflow_id:
        errors.append("workflow_id does not match WCE1 recommendation")
    if not contract.get("inputs"):
        errors.append("inputs are required")
    if not contract.get("outputs"):
        errors.append("outputs are required")
    if not any(role.get("role") == "primary_kifrs" for role in contract.get("evidence_roles", [])):
        errors.append("primary_kifrs evidence role is required")
    if not contract.get("human_review_boundary"):
        errors.append("human review boundary is required")
    if "final recognition conclusion" not in contract.get("human_review_boundary", []):
        errors.append("final recognition conclusion must remain human-reviewed")
    if "contract OCR" not in contract.get("not_implemented", []):
        errors.append("contract OCR must remain out of scope for this contract")
    return errors


def render_markdown(result: dict[str, Any]) -> str:
    contract = result["contract"]
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: WCE2 contract for the workflow selected by WCE1.",
        "",
        "## 한 줄 결론",
        "",
        "`1037_provisions` is now a bounded decision-prep workflow contract: it can draft recognition/measurement review material, but final conclusion and estimate judgment stay with the accountant.",
        "",
        "## Contract",
        "",
        f"- workflow id: `{contract['workflow_id']}`",
        f"- service line: {contract['service_line']}",
        f"- standard scope: {', '.join(contract['standard_scope'])}",
        f"- workflow name: {contract['workflow_name']}",
        f"- purpose: {contract['purpose']}",
        "",
        "## Inputs",
        "",
        "| Name | Required | Source | Description |",
        "|---|---|---|---|",
    ]
    for item in contract["inputs"]:
        lines.append(f"| {item['name']} | {item['required']} | {item['source']} | {item['description']} |")
    lines.extend(["", "## Outputs", ""])
    lines.extend(f"- {output}" for output in contract["outputs"])
    lines.extend(["", "## Evidence Roles", "", "| Role | Allowed Sources | Purpose |", "|---|---|---|"])
    for role in contract["evidence_roles"]:
        lines.append(f"| {role['role']} | {', '.join(role['allowed_sources'])} | {role['purpose']} |")
    lines.extend(["", "## Human Review Boundary", ""])
    lines.extend(f"- {item}" for item in contract["human_review_boundary"])
    lines.extend(["", "## Not Implemented", ""])
    lines.extend(f"- {item}" for item in contract["not_implemented"])
    lines.extend(["", "## Errors", ""])
    lines.extend(f"- {error}" for error in result["errors"]) if result["errors"] else lines.append("- none")
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
    result = build_first_workflow_contract()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build WCE2 first workflow contract.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_first_workflow_contract()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- selected candidate: {result['selected_candidate']}")
        print(f"- next adapter: {result['contract']['next_adapter']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
