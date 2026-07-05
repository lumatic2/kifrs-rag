from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.client_private_local_parser_operator_runbook import check_local_parser_operator_runbook  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-local-parser-real-adapter-implementation-plan.md"
REQUIRED_PHRASES = [
    "actual accountant feedback evidence",
    "explicit user authorization",
    "local ephemeral quarantine",
    "structured facts only",
    "no raw private file in public artifacts",
    "no OCR text in public artifacts",
    "delete quarantined files before report write",
    "no private embeddings before a separate namespace gate",
    "manual rollback",
    "quality_preflight",
]


def check_real_adapter_implementation_plan() -> dict[str, Any]:
    operator = check_local_parser_operator_runbook()
    errors: list[str] = []
    if operator["ok"] is not True:
        errors.extend(f"operator_runbook: {error}" for error in operator["errors"])

    plan_exists = REPORT_PATH.exists()
    plan_text = REPORT_PATH.read_text(encoding="utf-8") if plan_exists else ""
    if not plan_exists:
        errors.append(f"implementation plan is missing: {_display_path(REPORT_PATH)}")
    for phrase in REQUIRED_PHRASES:
        if phrase not in plan_text:
            errors.append(f"implementation plan missing phrase: {phrase}")

    return {
        "ok": not errors,
        "errors": errors,
        "plan_id": "lpip1-local-parser-real-adapter-implementation-plan",
        "plan_path": _display_path(REPORT_PATH),
        "operator_runbook_ok": bool(operator["ok"]),
        "required_preconditions": [
            "actual accountant feedback evidence",
            "explicit user authorization",
            "passing local parser operator runbook",
            "public-safe implementation plan",
        ],
        "implementation_slices": [
            "local quarantine path preflight",
            "parser adapter input envelope",
            "structured facts extraction handoff",
            "redaction and review-pack routing",
            "deletion attestation",
            "public-safe gates and rollback",
        ],
        "forbidden_until_separate_gate": [
            "cloud upload",
            "private embeddings",
            "answer-time use of private document body",
            "committing raw files or parsed bodies",
        ],
        "next_leaf": "real-accountant-session RS2/RS3 evidence capture, then explicit authorization before real adapter coding",
    }


def render_plan(result: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# LPIP1 Local Parser Real-Adapter Implementation Plan",
            "",
            "> Scope: implementation plan required before any real local-only private-file parser adapter coding.",
            "",
            "## 한 줄 결론",
            "",
            "Real adapter coding is still not authorized. This plan only defines the safe implementation order for a future local-only parser after actual accountant feedback evidence and explicit user authorization exist.",
            "",
            "## Preconditions",
            "",
            "- actual accountant feedback evidence exists and has passed the public-safe capture gate.",
            "- explicit user authorization is recorded for real local private-file parser work.",
            "- `python scripts\\client_private_local_parser_operator_runbook.py --format text --write` passes.",
            "- `python scripts\\client_private_local_parser_real_adapter_decision_gate.py --authorize-real-adapter --implementation-plan docs\\reports\\2026-07-05-local-parser-real-adapter-implementation-plan.md` returns `allowed_to_implement: True`.",
            "",
            "## Implementation Slices",
            "",
            "1. Local quarantine path preflight",
            "   - Accept only local ephemeral quarantine paths that are already gitignored.",
            "   - Reject cloud paths, network shares, and repo-tracked paths.",
            "   - no raw private file in public artifacts.",
            "2. Parser adapter input envelope",
            "   - Read from the local quarantine path only inside the authorized local run.",
            "   - Convert the private input into structured facts only.",
            "   - Keep raw content out of reports, JSONL, logs, tests, and commits.",
            "3. Optional OCR boundary",
            "   - OCR can run only inside the local quarantine flow if explicitly authorized.",
            "   - no OCR text in public artifacts.",
            "   - OCR output must be discarded or reduced to reviewed structured facts before report write.",
            "4. Review-pack handoff",
            "   - Reuse the existing `LocalPrivateParserPrototypeInput` and redaction route.",
            "   - Route only reviewed structured facts into review-pack candidates.",
            "   - Do not allow answer-time use of private document body.",
            "5. Deletion attestation",
            "   - delete quarantined files before report write.",
            "   - Record deletion status and operator check without source text.",
            "   - Fail close gates if raw, parsed, OCR, or embedding artifacts remain.",
            "6. Public-safe gates and rollback",
            "   - Run focused parser tests, `quality_preflight`, and gap audit before commit.",
            "   - manual rollback is deletion of quarantine files plus removal of derived structured facts from the run output.",
            "",
            "## Explicit Non-Goals",
            "",
            "- No cloud upload.",
            "- No private document persistence.",
            "- no private embeddings before a separate namespace gate.",
            "- No answer-time use of private source body.",
            "- No commit of raw files, parsed bodies, OCR text, customer identifiers, or private embeddings.",
            "",
            "## Verification Commands",
            "",
            "```powershell",
            "python scripts\\client_private_local_parser_real_adapter_implementation_plan.py --format text --write",
            "python scripts\\client_private_local_parser_real_adapter_decision_gate.py --format text --write",
            "python -m pytest tests\\test_client_private_local_parser_real_adapter_implementation_plan.py tests\\test_client_private_local_parser_real_adapter_decision_gate.py -q",
            "python scripts\\accounting_intelligence_gap_audit.py --format text --write",
            "python scripts\\quality_preflight.py --format text",
            "```",
            "",
            "## Next Leaf",
            "",
            str(result["next_leaf"]),
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps(result, ensure_ascii=False, indent=2, default=str),
            "```",
        ]
    ) + "\n"


def render_report(result: dict[str, Any]) -> str:
    lines = [
        "# LPIP1 Local Parser Real-Adapter Implementation Plan Gate",
        "",
        "> Scope: verify that a public-safe implementation plan exists before real adapter coding.",
        "",
        "## Result",
        "",
        f"- ok: {result['ok']}",
        f"- plan: `{result['plan_path']}`",
        f"- operator runbook ok: {result['operator_runbook_ok']}",
        "",
        "## Preconditions",
        "",
    ]
    lines.extend(f"- {item}" for item in result["required_preconditions"])
    lines.extend([
        "",
        "## Implementation Slices",
        "",
    ])
    lines.extend(f"- {item}" for item in result["implementation_slices"])
    lines.extend([
        "",
        "## Forbidden Until Separate Gate",
        "",
    ])
    lines.extend(f"- {item}" for item in result["forbidden_until_separate_gate"])
    lines.extend([
        "",
        "## Next Leaf",
        "",
        str(result["next_leaf"]),
        "",
        "## Machine Result",
        "",
        "```json",
        json.dumps(result, ensure_ascii=False, indent=2, default=str),
        "```",
    ])
    return "\n".join(lines) + "\n"


def write_plan() -> dict[str, Any]:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    provisional = {
        "ok": True,
        "errors": [],
        "plan_id": "lpip1-local-parser-real-adapter-implementation-plan",
        "plan_path": _display_path(REPORT_PATH),
        "operator_runbook_ok": True,
        "required_preconditions": [],
        "implementation_slices": [],
        "forbidden_until_separate_gate": [],
        "next_leaf": "real-accountant-session RS2/RS3 evidence capture, then explicit authorization before real adapter coding",
    }
    REPORT_PATH.write_text(render_plan(provisional), encoding="utf-8")
    result = check_real_adapter_implementation_plan()
    REPORT_PATH.write_text(render_plan(result), encoding="utf-8")
    return result


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Write/check the local parser real-adapter implementation plan.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = write_plan() if args.write else check_real_adapter_implementation_plan()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"plan_path: {result['plan_path']}")
        print(f"operator_runbook_ok: {result['operator_runbook_ok']}")
        print(f"next_leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
