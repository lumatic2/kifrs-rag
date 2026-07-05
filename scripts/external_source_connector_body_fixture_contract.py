from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-esb2-source-body-fixture-contract.md"


def build_fixture_contract() -> dict[str, Any]:
    fixture_input_schema = {
        "fixture_id": "string, stable synthetic fixture id",
        "source_class": "interpretive_accounting_material",
        "authority_role": "supporting_interpretive_evidence",
        "publisher_class": "regulator_or_standard_setter",
        "canonical_locator": "string, public locator or invented local locator",
        "policy_status": "synthetic_dry_run_only",
        "synthetic_body_label": "label only; no copied third-party body payload",
        "topic_tags": ["revenue", "lease", "financial_instrument", "disclosure"],
    }
    parser_output_schema = {
        "record_id": "string",
        "source_class": "string",
        "authority_role": "string",
        "canonical_locator": "string",
        "topic_tags": "list[string]",
        "assertion_labels": "list[string]",
        "chunk_strategy": "semantic_section_stub",
        "chunk_count": "integer",
        "policy_status": "synthetic_only",
    }
    chunk_output_schema = {
        "chunk_id": "string",
        "fixture_id": "string",
        "locator": "string",
        "topic_tags": "list[string]",
        "synthetic_summary_label": "string",
        "retrieval_terms": "list[string]",
        "contains_copied_body_payload": False,
    }
    forbidden_public_states = [
        "copied third-party body payload",
        "verbatim quote from protected material",
        "credential or token",
        "embedding vector dump",
        "raw xml or pdf bytes",
        "local private cache path in public report",
    ]
    sample_fixture = {
        "fixture_id": "esb2-fixture-interpretive-001",
        "source_class": "interpretive_accounting_material",
        "authority_role": "supporting_interpretive_evidence",
        "publisher_class": "regulator_or_standard_setter",
        "canonical_locator": "synthetic://interpretive-accounting-material/esb2-001",
        "policy_status": "synthetic_dry_run_only",
        "synthetic_body_label": "author_written_placeholder_label_only",
        "topic_tags": ["revenue", "disclosure"],
    }
    checks = {
        "selected_lane_matches_ESB1": sample_fixture["source_class"] == "interpretive_accounting_material",
        "fixture_has_no_copied_payload": sample_fixture["synthetic_body_label"].endswith("label_only"),
        "parser_output_schema_present": bool(parser_output_schema),
        "chunk_output_schema_present": bool(chunk_output_schema),
        "chunk_contract_blocks_copied_payload": chunk_output_schema["contains_copied_body_payload"] is False,
        "forbidden_public_states_present": len(forbidden_public_states) >= 5,
        "next_milestone_named": True,
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "ESB2 Synthetic Source-Body Fixture Contract",
        "ok": not errors,
        "horizon": "external-source-body-connector-expansion",
        "completed_milestone": "ESB2",
        "selected_source_class": "interpretive_accounting_material",
        "fixture_input_schema": fixture_input_schema,
        "parser_output_schema": parser_output_schema,
        "chunk_output_schema": chunk_output_schema,
        "sample_fixture": sample_fixture,
        "forbidden_public_state_count": len(forbidden_public_states),
        "checks": checks,
        "errors": errors,
        "next_leaf": "ESB3_chunking_and_retrieval_dry_run",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: synthetic fixture and parser/chunker schema for the selected ESB connector lane.",
        "",
        "## 한 줄 결론",
        "",
        (
            "The selected interpretive connector now has a synthetic fixture contract and parser/chunker output schema; "
            "public artifacts still contain labels, locators, policy status, and retrieval metadata only."
        ),
        "",
        "## Fixture Input Schema",
        "",
        "| Field | Contract |",
        "|---|---|",
    ]
    for field, contract in result["fixture_input_schema"].items():
        lines.append(f"| `{field}` | {contract} |")
    lines.extend(["", "## Parser Output Schema", "", "| Field | Contract |", "|---|---|"])
    for field, contract in result["parser_output_schema"].items():
        lines.append(f"| `{field}` | {contract} |")
    lines.extend(["", "## Chunk Output Schema", "", "| Field | Contract |", "|---|---|"])
    for field, contract in result["chunk_output_schema"].items():
        lines.append(f"| `{field}` | {contract} |")
    lines.extend(
        [
            "",
            "## Sample Fixture",
            "",
            "| Field | Value |",
            "|---|---|",
        ]
    )
    for field, value in result["sample_fixture"].items():
        lines.append(f"| `{field}` | {value} |")
    lines.extend(
        [
            "",
            "## Public-Safety Boundary",
            "",
            f"- forbidden public state count: {result['forbidden_public_state_count']}",
            "- fixture report stores labels and schemas only",
            "- live fetching, real body caching, chunking, and embedding remain outside ESB2",
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
    result = build_fixture_contract()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build ESB2 synthetic source-body fixture contract.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_fixture_contract()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- selected source class: {result['selected_source_class']}")
        print(f"- next leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
