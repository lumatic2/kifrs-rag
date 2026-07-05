from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-ppr2-fixture-adapter-contract.md"


def build_fixture_adapter_contract() -> dict[str, Any]:
    file_classes = [
        _file_class(
            class_id="lease_contract_fixture",
            source_kind="synthetic local fixture",
            accepted_extensions=[".md", ".txt", ".json"],
            structured_outputs=["contract_terms", "payment_schedule", "lease_term", "option_flags"],
        ),
        _file_class(
            class_id="trial_balance_fixture",
            source_kind="synthetic local fixture",
            accepted_extensions=[".csv", ".json"],
            structured_outputs=["account_code", "account_name", "debit", "credit", "period"],
        ),
        _file_class(
            class_id="accounting_policy_fixture",
            source_kind="synthetic local fixture",
            accepted_extensions=[".md", ".txt", ".json"],
            structured_outputs=["policy_area", "recognition_rule", "measurement_rule", "disclosure_note"],
        ),
    ]
    redaction_fields = [
        "counterparty_name",
        "employee_name",
        "registration_number",
        "bank_account",
        "contract_address",
        "raw_clause_text",
    ]
    failure_states = [
        {"state": "unsupported_file_type", "public_action": "report class and extension only"},
        {"state": "parse_confidence_low", "public_action": "emit structured error and require human review"},
        {"state": "redaction_required", "public_action": "drop raw field and emit redaction status"},
        {"state": "authorization_missing", "public_action": "do not parse; emit authorization-required status"},
    ]
    output_schema = {
        "fixture_id": "string",
        "file_class": "enum",
        "parser_status": "parsed | partial | rejected",
        "structured_facts": "list[public_safe_fact]",
        "redactions": "list[redaction_status]",
        "needs_human_review": "boolean",
        "retention_state": "retained | delete_pending | deleted",
    }
    evidence = [
        _evidence("ppr1_authorization_plan", "docs/reports/2026-07-05-ppr1-authorization-safe-adapter-proof.md"),
        _evidence("local_parser_plan", "docs/reports/2026-07-05-local-parser-real-adapter-implementation-plan.md"),
        _evidence("parser_prototype_close", "docs/reports/2026-07-05-real-local-parser-prototype-close-report.md"),
    ]
    checks = {
        "all_evidence_exists": all(item["exists"] for item in evidence),
        "file_classes_defined": len(file_classes) >= 3,
        "redaction_fields_defined": len(redaction_fields) >= 5,
        "failure_states_defined": len(failure_states) >= 4,
        "raw_payload_not_output": "raw_payload" not in output_schema,
        "human_review_flag_present": "needs_human_review" in output_schema,
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "PPR2 Realistic Local Fixture Adapter Contract",
        "ok": not errors,
        "horizon": "private-parser-realism-hardening",
        "completed_milestone": "PPR2",
        "file_classes": file_classes,
        "output_schema": output_schema,
        "redaction_fields": redaction_fields,
        "failure_states": failure_states,
        "evidence": evidence,
        "checks": checks,
        "errors": errors,
        "next_leaf": "PPR3_deletion_and_retention_rehearsal",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: public-safe contract for realistic local fixture parser adapter work.",
        "",
        "## 한 줄 결론",
        "",
        "The next parser adapter may handle synthetic local fixtures through structured facts, redaction states, and explicit failure states only.",
        "",
        "## File Classes",
        "",
        "| Class | Source Kind | Extensions | Structured Outputs |",
        "|---|---|---|---|",
    ]
    for item in result["file_classes"]:
        lines.append(
            f"| {item['class_id']} | {item['source_kind']} | {', '.join(item['accepted_extensions'])} | {', '.join(item['structured_outputs'])} |"
        )
    lines.extend(["", "## Output Schema", "", "| Field | Type |", "|---|---|"])
    for field, type_name in result["output_schema"].items():
        lines.append(f"| {field} | {type_name} |")
    lines.extend(["", "## Redaction Fields", ""])
    lines.extend(f"- {item}" for item in result["redaction_fields"])
    lines.extend(["", "## Failure States", "", "| State | Public Action |", "|---|---|"])
    for item in result["failure_states"]:
        lines.append(f"| {item['state']} | {item['public_action']} |")
    lines.extend(["", "## Evidence", "", "| ID | Path | Exists |", "|---|---|---|"])
    for item in result["evidence"]:
        lines.append(f"| {item['id']} | `{item['path']}` | {item['exists']} |")
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
    result = build_fixture_adapter_contract()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _file_class(class_id: str, source_kind: str, accepted_extensions: list[str], structured_outputs: list[str]) -> dict[str, Any]:
    return {
        "class_id": class_id,
        "source_kind": source_kind,
        "accepted_extensions": accepted_extensions,
        "structured_outputs": structured_outputs,
    }


def _evidence(id_: str, path: str) -> dict[str, Any]:
    return {"id": id_, "path": path, "exists": (ROOT / path).exists()}


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build PPR2 fixture adapter contract.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_fixture_adapter_contract()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- file classes: {len(result['file_classes'])}")
        print(f"- next leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
