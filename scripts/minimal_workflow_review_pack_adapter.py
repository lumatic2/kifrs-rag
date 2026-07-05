from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.first_workflow_contract import build_first_workflow_contract  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-wce3-minimal-review-pack-adapter.md"


SAMPLE_FACTS = {
    "obligating_event": "board-approved restructuring plan communicated before reporting date",
    "obligation_type": "restructuring",
    "outflow_probability": "probable",
    "estimate_basis": "management provided expected direct exit costs as a bounded amount",
    "discounting_indicator": "not material for this synthetic fixture",
}


def build_minimal_review_pack_adapter(facts: dict[str, str] | None = None) -> dict[str, Any]:
    contract_result = build_first_workflow_contract()
    contract = contract_result["contract"]
    input_facts = facts or SAMPLE_FACTS
    missing_required = [
        item["name"]
        for item in contract["inputs"]
        if item["required"] and not input_facts.get(item["name"])
    ]
    output = _build_output(contract, input_facts, missing_required)
    errors = []
    if contract_result["selected_candidate"] != "1037_provisions":
        errors.append("WCE2 selected candidate is not 1037_provisions")
    if missing_required:
        errors.append(f"missing required inputs: {missing_required}")
    if not output["human_review_checklist"]:
        errors.append("human_review_checklist is required")
    if not output["structured_summary"]:
        errors.append("structured_summary is required")
    return {
        "title": "WCE3 Minimal Review-Pack Adapter",
        "ok": not errors,
        "horizon": "workflow-coverage-expansion",
        "completed_milestone": "WCE3",
        "workflow_id": contract["workflow_id"],
        "input_mode": "structured_local_facts",
        "input_facts": input_facts,
        "output": output,
        "errors": errors,
        "report_path": _display_path(REPORT_PATH),
    }


def _build_output(
    contract: dict[str, Any], input_facts: dict[str, str], missing_required: list[str]
) -> dict[str, Any]:
    recognition_status = "review_ready" if not missing_required else "insufficient_facts"
    has_estimate = bool(input_facts.get("estimate_basis"))
    measurement_status = "estimate_basis_supplied" if has_estimate else "estimate_basis_missing"
    structured_summary = {
        "workflow": contract["workflow_name"],
        "recognition_assessment": recognition_status,
        "measurement_summary": measurement_status,
        "journal_entry_cue": (
            "prepare journal entry cue for provision recognition if accountant confirms present obligation, probable outflow, and reliable estimate"
            if recognition_status == "review_ready"
            else "do not draft journal entry cue until required facts are supplied"
        ),
        "missing_facts": missing_required
        + ([] if has_estimate else ["estimate_basis or explicit no-estimate conclusion"]),
        "authority_panel": [
            {"role": role["role"], "purpose": role["purpose"]}
            for role in contract["evidence_roles"]
        ],
    }
    checklist = [
        "Confirm the event creates a present legal or constructive obligation.",
        "Confirm outflow probability; do not let the adapter infer probability from narrative alone.",
        "Review whether management's estimate is reliable and complete.",
        "Check whether discounting is material.",
        "Confirm final recognition, measurement, presentation, and disclosure with the accountant.",
    ]
    confidence = "medium" if recognition_status == "review_ready" and has_estimate else "low"
    return {
        "structured_summary": structured_summary,
        "human_review_checklist": checklist,
        "confidence": confidence,
        "limitations": contract["human_review_boundary"],
    }


def render_markdown(result: dict[str, Any]) -> str:
    output = result["output"]
    summary = output["structured_summary"]
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: minimal adapter output for the WCE2 1037 provisions workflow contract.",
        "",
        "## 한 줄 결론",
        "",
        "The 1037 provisions workflow now emits a structured review-pack draft from structured local facts, with final recognition and estimate judgment kept in human review.",
        "",
        "## Adapter Summary",
        "",
        f"- workflow id: `{result['workflow_id']}`",
        f"- input mode: `{result['input_mode']}`",
        f"- recognition assessment: `{summary['recognition_assessment']}`",
        f"- measurement summary: `{summary['measurement_summary']}`",
        f"- confidence: `{output['confidence']}`",
        f"- journal entry cue: {summary['journal_entry_cue']}",
        "",
        "## Missing Facts",
        "",
    ]
    lines.extend(f"- {item}" for item in summary["missing_facts"]) if summary["missing_facts"] else lines.append("- none")
    lines.extend(["", "## Authority Panel", "", "| Role | Purpose |", "|---|---|"])
    for role in summary["authority_panel"]:
        lines.append(f"| {role['role']} | {role['purpose']} |")
    lines.extend(["", "## Human Review Checklist", ""])
    lines.extend(f"- {item}" for item in output["human_review_checklist"])
    lines.extend(["", "## Limitations", ""])
    lines.extend(f"- {item}" for item in output["limitations"])
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
    result = build_minimal_review_pack_adapter()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build WCE3 minimal review-pack adapter output.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_minimal_review_pack_adapter()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- workflow id: {result['workflow_id']}")
        print(f"- confidence: {result['output']['confidence']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
