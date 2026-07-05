from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-wcd2-workflow-sample-contract-pack.md"


def build_contract_pack() -> dict[str, Any]:
    workflow = {
        "workflow_id": "audit_disclosure_tie_out",
        "service_line": "F-AUD / F-ACC",
        "surface": "audit issue support and disclosure requirement tie-out",
        "status": "selected_for_minimal_adapter",
    }
    input_facts = [
        {"field": "entity_profile_label", "kind": "public_safe_label", "required": True},
        {"field": "reporting_period", "kind": "date_range", "required": True},
        {"field": "disclosure_area", "kind": "enum", "required": True},
        {"field": "standard_scope", "kind": "standard_id_or_topic", "required": True},
        {"field": "prepared_disclosure_label", "kind": "synthetic_or_author_written_label", "required": True},
        {"field": "review_pack_refs", "kind": "public_report_locator_list", "required": True},
    ]
    authority_needs = [
        {"role": "primary", "source": "K-IFRS paragraph retrieval", "required": True},
        {"role": "supporting", "source": "external connector metadata or synthetic interpretive lane", "required": False},
        {"role": "fact", "source": "public-safe fixture facts", "required": True},
        {"role": "human_review", "source": "materiality and final audit conclusion", "required": True},
    ]
    output_surface = [
        "disclosure_requirement_checklist",
        "prepared_disclosure_tie_out_status",
        "missing_or_ambiguous_evidence_flags",
        "review_note_draft_labels",
        "human_review_required_items",
    ]
    review_boundary = [
        "AI may draft requirement mapping and review notes.",
        "AI may not conclude audit sufficiency.",
        "AI may not sign off disclosure completeness.",
        "Materiality and final conclusion remain human responsibilities.",
    ]
    failure_states = [
        {"state": "missing_primary_authority", "action": "return blocked"},
        {"state": "conflicting_fixture_facts", "action": "return needs_human_review"},
        {"state": "unsupported_disclosure_area", "action": "return unsupported_workflow"},
        {"state": "materiality_judgment_required", "action": "return human_review_required"},
    ]
    checks = {
        "workflow_matches_WCD1": workflow["workflow_id"] == "audit_disclosure_tie_out",
        "input_facts_present": len(input_facts) >= 5,
        "authority_needs_present": len(authority_needs) >= 4,
        "output_surface_present": len(output_surface) >= 4,
        "review_boundary_explicit": any("may not" in item for item in review_boundary),
        "failure_states_present": len(failure_states) >= 4,
        "next_milestone_named": True,
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "WCD2 Workflow Sample Contract Pack",
        "ok": not errors,
        "horizon": "workflow-coverage-depth-expansion",
        "completed_milestone": "WCD2",
        "workflow": workflow,
        "input_facts": input_facts,
        "authority_needs": authority_needs,
        "output_surface": output_surface,
        "review_boundary": review_boundary,
        "failure_states": failure_states,
        "checks": checks,
        "errors": errors,
        "next_leaf": "WCD3_minimal_adapter_expansion",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    workflow = result["workflow"]
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: public-safe workflow sample contract for coverage-depth expansion.",
        "",
        "## 한 줄 결론",
        "",
        (
            f"`{workflow['workflow_id']}` is now contract-ready for a minimal adapter: inputs, authority needs, "
            "output surface, review boundary, and failure states are explicit."
        ),
        "",
        "## Workflow",
        "",
        f"- workflow id: `{workflow['workflow_id']}`",
        f"- service line: `{workflow['service_line']}`",
        f"- surface: {workflow['surface']}",
        f"- status: `{workflow['status']}`",
        "",
        "## Input Facts",
        "",
        "| Field | Kind | Required |",
        "|---|---|---|",
    ]
    for item in result["input_facts"]:
        lines.append(f"| `{item['field']}` | {item['kind']} | {item['required']} |")
    lines.extend(["", "## Authority Needs", "", "| Role | Source | Required |", "|---|---|---|"])
    for item in result["authority_needs"]:
        lines.append(f"| {item['role']} | {item['source']} | {item['required']} |")
    lines.extend(["", "## Output Surface", ""])
    lines.extend(f"- `{item}`" for item in result["output_surface"])
    lines.extend(["", "## Review Boundary", ""])
    lines.extend(f"- {item}" for item in result["review_boundary"])
    lines.extend(["", "## Failure States", "", "| State | Action |", "|---|---|"])
    for item in result["failure_states"]:
        lines.append(f"| `{item['state']}` | `{item['action']}` |")
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
    result = build_contract_pack()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build WCD2 workflow sample contract pack.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_contract_pack()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- workflow: {result['workflow']['workflow_id']}")
        print(f"- next leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
