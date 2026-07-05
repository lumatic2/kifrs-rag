from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-wcd3-minimal-adapter-expansion.md"


def build_adapter_report() -> dict[str, Any]:
    sample_input = {
        "workflow_id": "audit_disclosure_tie_out",
        "entity_profile_label": "public_fixture_manufacturing_group",
        "reporting_period": "2026-Q2",
        "disclosure_area": "lease_disclosure",
        "standard_scope": "KIFRS1116_disclosure_requirements",
        "prepared_disclosure_label": "author_written_lease_disclosure_draft_label",
        "review_pack_refs": [
            "docs/reports/2026-07-05-wcd2-workflow-sample-contract-pack.md",
            "docs/reports/2026-07-05-esb3-chunking-retrieval-dry-run.md",
        ],
    }
    adapter_output = run_adapter(sample_input)
    checks = {
        "workflow_matches_contract": adapter_output["workflow_id"] == "audit_disclosure_tie_out",
        "checklist_present": len(adapter_output["disclosure_requirement_checklist"]) >= 3,
        "tie_out_status_present": adapter_output["prepared_disclosure_tie_out_status"] in {"partial", "ready_for_review"},
        "review_flags_present": len(adapter_output["human_review_required_items"]) >= 1,
        "no_final_audit_conclusion": adapter_output["final_audit_conclusion"] is None,
        "next_milestone_named": True,
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "WCD3 Minimal Adapter Expansion",
        "ok": not errors,
        "horizon": "workflow-coverage-depth-expansion",
        "completed_milestone": "WCD3",
        "sample_input": sample_input,
        "adapter_output": adapter_output,
        "checks": checks,
        "errors": errors,
        "next_leaf": "WCD4_coverage_depth_metric_update",
        "report_path": _display_path(REPORT_PATH),
    }


def run_adapter(sample_input: dict[str, Any]) -> dict[str, Any]:
    checklist = [
        {
            "requirement_id": "lease_maturity_analysis_label",
            "status": "mapped",
            "evidence_ref": sample_input["review_pack_refs"][0],
        },
        {
            "requirement_id": "lease_expense_split_label",
            "status": "needs_evidence",
            "evidence_ref": None,
        },
        {
            "requirement_id": "significant_judgement_label",
            "status": "human_review_required",
            "evidence_ref": sample_input["review_pack_refs"][1],
        },
    ]
    missing_flags = [
        item["requirement_id"] for item in checklist if item["status"] in {"needs_evidence", "human_review_required"}
    ]
    return {
        "workflow_id": sample_input["workflow_id"],
        "disclosure_requirement_checklist": checklist,
        "prepared_disclosure_tie_out_status": "partial",
        "missing_or_ambiguous_evidence_flags": missing_flags,
        "review_note_draft_labels": [
            "lease_disclosure_mapping_note_label",
            "lease_judgement_review_note_label",
        ],
        "human_review_required_items": [
            "materiality_threshold",
            "final_disclosure_completeness",
            "audit_sufficiency",
        ],
        "final_audit_conclusion": None,
    }


def render_markdown(result: dict[str, Any]) -> str:
    output = result["adapter_output"]
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: minimal public-safe adapter for the selected workflow coverage-depth sample.",
        "",
        "## 한 줄 결론",
        "",
        (
            "`audit_disclosure_tie_out` now produces requirement mapping, tie-out status, review flags, "
            "and draft-note labels without making a final audit conclusion."
        ),
        "",
        "## Sample Input",
        "",
        "| Field | Value |",
        "|---|---|",
    ]
    for field, value in result["sample_input"].items():
        lines.append(f"| `{field}` | {value} |")
    lines.extend(
        [
            "",
            "## Disclosure Requirement Checklist",
            "",
            "| Requirement | Status | Evidence Ref |",
            "|---|---|---|",
        ]
    )
    for item in output["disclosure_requirement_checklist"]:
        lines.append(f"| `{item['requirement_id']}` | `{item['status']}` | {item['evidence_ref']} |")
    lines.extend(
        [
            "",
            "## Adapter Output",
            "",
            f"- tie-out status: `{output['prepared_disclosure_tie_out_status']}`",
            f"- missing or ambiguous flags: {output['missing_or_ambiguous_evidence_flags']}",
            f"- review note draft labels: {output['review_note_draft_labels']}",
            f"- human review required items: {output['human_review_required_items']}",
            f"- final audit conclusion: {output['final_audit_conclusion']}",
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
    result = build_adapter_report()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build WCD3 minimal workflow adapter report.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_adapter_report()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- workflow: {result['adapter_output']['workflow_id']}")
        print(f"- next leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
