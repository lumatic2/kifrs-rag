from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.client_private_local_parser_adapter_contract_check import (  # noqa: E402
    check_local_parser_adapter_contract,
)
from scripts.client_private_local_parser_adapter_dry_run_gate import (  # noqa: E402
    check_local_parser_adapter_dry_run_gate,
)
from scripts.client_private_local_parser_adapter_scaffold import (  # noqa: E402
    check_local_parser_adapter_scaffold,
)
from scripts.client_private_parser_dry_run_fixture_check import (  # noqa: E402
    check_parser_dry_run_fixture,
)
from scripts.client_private_upload_storage_policy_check import check_upload_storage_policy  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-lpor1-local-parser-operator-runbook.md"

REQUIRED_REPORTS = {
    "upload_storage_policy": ROOT / "docs" / "reports" / "2026-07-05-cpu1-client-private-upload-storage-policy.md",
    "parser_dry_run_fixture": ROOT / "docs" / "reports" / "2026-07-05-pdf1-private-parser-dry-run-fixture.md",
    "adapter_contract": ROOT / "docs" / "reports" / "2026-07-05-lpa1-local-parser-adapter-contract.md",
    "adapter_dry_run_gate": ROOT / "docs" / "reports" / "2026-07-05-lpad1-local-parser-adapter-dry-run-gate.md",
    "adapter_scaffold": ROOT / "docs" / "reports" / "2026-07-05-lpas1-local-parser-adapter-scaffold.md",
}


@dataclass(frozen=True)
class OperatorRunbookStep:
    step_id: str
    title: str
    command: str
    purpose: str
    success_signal: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


def operator_runbook_steps() -> list[OperatorRunbookStep]:
    return [
        OperatorRunbookStep(
            step_id="LPOR1-1",
            title="Confirm upload/storage policy",
            command="python scripts\\client_private_upload_storage_policy_check.py --format text --write",
            purpose="Verify local ephemeral quarantine, structured-facts-only parser mode, manual deletion, and public artifact limits.",
            success_signal="ok: True",
        ),
        OperatorRunbookStep(
            step_id="LPOR1-2",
            title="Confirm parser dry-run fixture",
            command="python scripts\\client_private_parser_dry_run_fixture_check.py --format text --write",
            purpose="Verify synthetic private-parser fixture shape routes to a review-pack candidate without source payloads.",
            success_signal="route_status: candidate",
        ),
        OperatorRunbookStep(
            step_id="LPOR1-3",
            title="Confirm adapter contract",
            command="python scripts\\client_private_local_parser_adapter_contract_check.py --format text --write",
            purpose="Verify adapter output schema, forbidden outputs, required operator checks, and prototype handoff.",
            success_signal="route_status: candidate",
        ),
        OperatorRunbookStep(
            step_id="LPOR1-4",
            title="Run adapter dry-run gate",
            command="python scripts\\client_private_local_parser_adapter_dry_run_gate.py --format text --write",
            purpose="Verify multiple synthetic structured-fact cases pass contract handoff and candidate routing.",
            success_signal="failed: 0",
        ),
        OperatorRunbookStep(
            step_id="LPOR1-5",
            title="Run adapter scaffold",
            command="python scripts\\client_private_local_parser_adapter_scaffold.py --format text --write",
            purpose="Verify the operator-facing entrypoint refuses raw paths, OCR, source-body parsing/persistence, and private embeddings.",
            success_signal="real_adapter_implemented: False",
        ),
        OperatorRunbookStep(
            step_id="LPOR1-6",
            title="Run public-safe preflight",
            command="python scripts\\quality_preflight.py --format text",
            purpose="Verify no protected source assets are required for the public artifact set.",
            success_signal="public_safe: True",
        ),
    ]


def check_required_reports(required_reports: dict[str, Path] | None = None) -> tuple[list[str], list[str]]:
    reports = required_reports or REQUIRED_REPORTS
    missing = [name for name, path in reports.items() if not path.exists()]
    present = [name for name, path in reports.items() if path.exists()]
    return present, missing


def check_local_parser_operator_runbook() -> dict[str, Any]:
    present_reports, missing_reports = check_required_reports()
    policy = check_upload_storage_policy()
    fixture = check_parser_dry_run_fixture()
    contract = check_local_parser_adapter_contract()
    dry_run = check_local_parser_adapter_dry_run_gate()
    scaffold = check_local_parser_adapter_scaffold()
    subchecks = {
        "upload_storage_policy": policy["ok"],
        "parser_dry_run_fixture": fixture["ok"],
        "adapter_contract": contract["ok"],
        "adapter_dry_run_gate": dry_run["ok"],
        "adapter_scaffold": scaffold["ok"],
    }
    errors: list[str] = []
    if missing_reports:
        errors.append(f"missing reports: {missing_reports}")
    errors.extend(f"{name}: subcheck failed" for name, ok in subchecks.items() if not ok)
    return {
        "ok": not errors,
        "errors": errors,
        "present_reports": present_reports,
        "missing_reports": missing_reports,
        "subchecks": subchecks,
        "steps": [step.to_dict() for step in operator_runbook_steps()],
        "report_path": str(REPORT_PATH.relative_to(ROOT)),
        "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or local parser real-adapter decision gate",
    }


def render_report(result: dict[str, Any]) -> str:
    lines = [
        "# LPOR1 Local Parser Operator Runbook",
        "",
        "> Scope: operator runbook for the local parser policy/contract/dry-run/scaffold chain before real private-file parsing exists.",
        "",
        "## 한 줄 결론",
        "",
        "The local parser operator path is now explicit: run storage policy, parser fixture, adapter contract, adapter dry-run gate, adapter scaffold, and public-safe preflight in order. This runbook still does not authorize real file upload, OCR, source-body parsing, deletion automation, or private embeddings.",
        "",
        "## Run Order",
        "",
    ]
    for step in result["steps"]:
        lines.extend([
            f"### {step['step_id']} {step['title']}",
            "",
            f"- Purpose: {step['purpose']}",
            f"- Command: `{step['command']}`",
            f"- Success signal: `{step['success_signal']}`",
            "",
        ])
    lines.extend([
        "## Current Gate Status",
        "",
        f"- OK: {result['ok']}",
        f"- Present reports: {', '.join(result['present_reports'])}",
        f"- Missing reports: {', '.join(result['missing_reports']) if result['missing_reports'] else 'none'}",
        "",
        "## Subchecks",
        "",
    ])
    lines.extend(f"- {name}: {ok}" for name, ok in result["subchecks"].items())
    lines.extend([
        "",
        "## Stop Conditions",
        "",
        "- Stop if any command above does not produce its success signal.",
        "- Stop if any raw file path, OCR text, source body, customer identifier, or private embedding appears in a public artifact.",
        "- Stop if the operator cannot confirm `structured-facts-only-public-safe` before running the scaffold.",
        "- Do not mark real parser readiness from this runbook; it is a pre-parser operator gate only.",
        "",
        "## Still Not Implemented",
        "",
        "- real file upload UI",
        "- OCR",
        "- real private document parsing",
        "- real file deletion automation",
        "- private embedding/index namespace",
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
    if result["errors"]:
        lines.extend([
            "",
            "## Errors",
            "",
        ])
        lines.extend(f"- {error}" for error in result["errors"])
    return "\n".join(lines) + "\n"


def write_report() -> dict[str, Any]:
    result = check_local_parser_operator_runbook()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_report(result), encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Render local parser operator runbook.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = write_report() if args.write else check_local_parser_operator_runbook()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"present_reports: {result['present_reports']}")
        print(f"missing_reports: {result['missing_reports']}")
        print(f"steps: {len(result['steps'])}")
        print(f"next_leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
