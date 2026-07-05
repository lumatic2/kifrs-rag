from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs.feedback import (  # noqa: E402
    LocalPrivateParserAdapterDryRunCase,
    render_local_private_parser_adapter_dry_run_gate,
    run_local_private_parser_adapter_dry_run_gate,
)
from scripts.client_private_local_parser_adapter_contract_check import default_adapter_contract  # noqa: E402
from scripts.client_private_upload_storage_policy_check import default_policy  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-lpad1-local-parser-adapter-dry-run-gate.md"


def default_dry_run_cases() -> list[LocalPrivateParserAdapterDryRunCase]:
    return [
        LocalPrivateParserAdapterDryRunCase(
            dry_run_id="lpad1-lease-contract-fixed-payments",
            source_stub="local-private://dry-run/lpad1-lease-contract-fixed-payments",
            document_type="contract",
            expected_domain="KIFRS1116",
            extracted_fields={
                "party": "lessee",
                "lease_term": "5 years",
                "payment_schedule": "monthly fixed payments",
            },
        ),
        LocalPrivateParserAdapterDryRunCase(
            dry_run_id="lpad1-lease-contract-variable-payments",
            source_stub="local-private://dry-run/lpad1-lease-contract-variable-payments",
            document_type="contract",
            expected_domain="KIFRS1116",
            extracted_fields={
                "party": "lessee",
                "lease_term": "3 years with renewal option excluded from dry-run facts",
                "payment_schedule": "monthly base rent plus usage-linked variable payments",
            },
        ),
    ]


def check_local_parser_adapter_dry_run_gate() -> dict[str, object]:
    policy = default_policy()
    contract = default_adapter_contract()
    gate = run_local_private_parser_adapter_dry_run_gate(
        "lpad1-local-parser-adapter-dry-run-gate",
        contract,
        policy,
        default_dry_run_cases(),
    )
    return {
        "ok": gate.ok,
        "errors": list(gate.errors),
        "policy_id": policy.policy_id,
        "contract_id": contract.adapter_id,
        "gate": gate.to_dict(),
        "report_path": str(REPORT_PATH.relative_to(ROOT)),
        "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or local parser adapter scaffold",
    }


def render_report(result: dict[str, object]) -> str:
    policy = default_policy()
    contract = default_adapter_contract()
    gate = run_local_private_parser_adapter_dry_run_gate(
        result["gate"]["gate_id"],
        contract,
        policy,
        default_dry_run_cases(),
    )
    gate_markdown = render_local_private_parser_adapter_dry_run_gate(gate).rstrip()
    gate_markdown = gate_markdown.replace(
        "# Local Parser Adapter Dry-Run Gate",
        "### Local Parser Adapter Dry-Run Gate",
        1,
    )
    lines = [
        "# LPAD1 Local Parser Adapter Dry-Run Gate",
        "",
        "> Scope: batch dry-run gate for adapter-shaped structured facts before real local-only file/OCR/parser implementation.",
        "",
        "## 한 줄 결론",
        "",
        "The local parser adapter contract now has a batch dry-run gate. Two synthetic KIFRS1116 lease-contract cases hand off through the adapter contract into the local parser prototype and route to review-pack candidates. This still does not read real files, run OCR, parse private source bodies, create private embeddings, or automate deletion.",
        "",
        "## Gate Result",
        "",
        gate_markdown,
        "",
        "## What This Enables",
        "",
        "- A future adapter scaffold can prove multiple structured-fact cases before touching private files.",
        "- Missing required fields, wrong source stubs, and non-candidate routes fail before report write.",
        "- Gap audit can distinguish contract readiness from dry-run execution readiness.",
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
    ]
    return "\n".join(lines) + "\n"


def write_report() -> dict[str, object]:
    result = check_local_parser_adapter_dry_run_gate()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_report(result), encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Run local parser adapter dry-run gate.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = write_report() if args.write else check_local_parser_adapter_dry_run_gate()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"contract_id: {result['contract_id']}")
        print(f"case_count: {result['gate']['case_count']}")
        print(f"passed: {len(result['gate']['passed_case_ids'])}")
        print(f"failed: {len(result['gate']['failed_case_ids'])}")
        print(f"next_leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
