from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs.feedback import (  # noqa: E402
    LocalPrivateParserAdapterScaffoldRequest,
    render_local_private_parser_adapter_scaffold_run,
    run_local_private_parser_adapter_scaffold,
    validate_local_private_parser_adapter_scaffold_request,
)
from scripts.client_private_local_parser_adapter_contract_check import default_adapter_contract  # noqa: E402
from scripts.client_private_upload_storage_policy_check import default_policy  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-lpas1-local-parser-adapter-scaffold.md"


def default_scaffold_request() -> LocalPrivateParserAdapterScaffoldRequest:
    return LocalPrivateParserAdapterScaffoldRequest(
        scaffold_run_id="lpas1-structured-facts-adapter-scaffold",
        source_kind="synthetic_fixture",
        source_stub="local-private://dry-run/lpas1-structured-facts-adapter-scaffold",
        document_type="contract",
        expected_domain="KIFRS1116",
        extracted_fields={
            "party": "lessee",
            "lease_term": "4 years",
            "payment_schedule": "quarterly fixed payments",
        },
        operator_ack="structured-facts-only-public-safe",
        raw_file_path="",
        ocr_enabled=False,
        parse_source_body=False,
        persist_source_body=False,
        create_private_embedding=False,
    )


def check_local_parser_adapter_scaffold() -> dict[str, object]:
    policy = default_policy()
    contract = default_adapter_contract()
    request = default_scaffold_request()
    request_issues = validate_local_private_parser_adapter_scaffold_request(request, contract, policy)
    scaffold_run = run_local_private_parser_adapter_scaffold(
        "lpas1-local-parser-adapter-scaffold",
        contract,
        policy,
        request,
    )
    return {
        "ok": not request_issues and scaffold_run.ok and not scaffold_run.real_adapter_implemented,
        "errors": [f"{issue.path}: {issue.message}" for issue in request_issues] + list(scaffold_run.errors),
        "policy_id": policy.policy_id,
        "contract_id": contract.adapter_id,
        "scaffold_run": scaffold_run.to_dict(),
        "report_path": str(REPORT_PATH.relative_to(ROOT)),
        "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or local parser operator runbook",
    }


def render_report(result: dict[str, object]) -> str:
    policy = default_policy()
    contract = default_adapter_contract()
    scaffold_run = run_local_private_parser_adapter_scaffold(
        result["scaffold_run"]["scaffold_id"],
        contract,
        policy,
        default_scaffold_request(),
    )
    scaffold_markdown = render_local_private_parser_adapter_scaffold_run(scaffold_run).rstrip()
    scaffold_markdown = scaffold_markdown.replace(
        "# Local Parser Adapter Scaffold Run",
        "### Local Parser Adapter Scaffold Run",
        1,
    )
    lines = [
        "# LPAS1 Local Parser Adapter Scaffold",
        "",
        "> Scope: adapter entrypoint scaffold for structured-facts-only local parser work before real file/OCR parsing exists.",
        "",
        "## 한 줄 결론",
        "",
        "A local parser adapter scaffold now exists. It accepts structured facts only, refuses raw file paths/OCR/source-body parsing/source persistence/private embeddings, and hands public-safe facts into the existing KIFRS1116 review-pack route. It is not a real private-file parser.",
        "",
        "## Scaffold Run",
        "",
        scaffold_markdown,
        "",
        "## What This Enables",
        "",
        "- Future real local-only parser work has a stable entrypoint and refusal behavior.",
        "- Operator-facing tooling can call one scaffold instead of reaching directly into prototype internals.",
        "- Gap audit can distinguish scaffold readiness from actual parser implementation.",
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
    result = check_local_parser_adapter_scaffold()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_report(result), encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Run local parser adapter scaffold check.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = write_report() if args.write else check_local_parser_adapter_scaffold()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"contract_id: {result['contract_id']}")
        print(f"scaffold_id: {result['scaffold_run']['scaffold_id']}")
        print(f"route: {result['scaffold_run']['prototype_result'].get('route', {}).get('route')}")
        print(f"route_status: {result['scaffold_run']['prototype_result'].get('route', {}).get('status')}")
        print(f"real_adapter_implemented: {result['scaffold_run']['real_adapter_implemented']}")
        print(f"next_leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
