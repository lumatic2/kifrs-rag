from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs.feedback import (  # noqa: E402
    LocalPrivateParserAdapterContract,
    contract_to_local_private_parser_prototype_input,
    render_local_private_parser_adapter_contract,
    render_local_private_parser_prototype_result,
    run_local_private_parser_prototype,
    validate_local_private_parser_adapter_contract,
)
from scripts.client_private_upload_storage_policy_check import default_policy  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-lpa1-local-parser-adapter-contract.md"


def default_adapter_contract() -> LocalPrivateParserAdapterContract:
    return LocalPrivateParserAdapterContract(
        adapter_id="lpa1-synthetic-local-parser-adapter-contract",
        source_kind="synthetic_fixture",
        output_mode="structured_facts_only",
        handoff_target="local_parser_prototype_input",
        allowed_document_types=["contract"],
        allowed_domains=["KIFRS1116"],
        required_extracted_fields=["party", "lease_term", "payment_schedule"],
        forbidden_outputs=[
            "raw private file",
            "parsed private body",
            "OCR text",
            "private embedding",
            "source document excerpt",
        ],
        required_operator_checks=[
            "verify local-only paths are gitignored before receiving any file",
            "delete quarantined raw files before close",
            "record deletion attestation without source body text",
            "run public-safe gate before committing any derived artifact",
        ],
        reads_real_files=False,
        runs_ocr=False,
        stores_source_body=False,
        stores_private_embedding=False,
        deletion_automation=False,
    )


def default_extracted_fields() -> dict[str, str]:
    return {
        "party": "lessee",
        "lease_term": "5 years",
        "payment_schedule": "monthly fixed payments",
    }


def check_local_parser_adapter_contract() -> dict[str, object]:
    policy = default_policy()
    contract = default_adapter_contract()
    contract_issues = validate_local_private_parser_adapter_contract(contract, policy)
    prototype_input = None
    prototype_result = None
    handoff_errors: list[str] = []
    if not contract_issues:
        try:
            prototype_input = contract_to_local_private_parser_prototype_input(
                contract,
                policy,
                parser_run_id="lpa1-contract-handoff-1116",
                source_stub="local-private://dry-run/lpa1-contract-handoff-1116",
                document_type="contract",
                expected_domain="KIFRS1116",
                extracted_fields=default_extracted_fields(),
            )
            prototype_result = run_local_private_parser_prototype(prototype_input, policy)
        except ValueError as exc:
            handoff_errors.append(str(exc))

    route = prototype_result.route.to_dict() if prototype_result is not None else {}
    errors = [f"{issue.path}: {issue.message}" for issue in contract_issues] + handoff_errors
    return {
        "ok": not errors and prototype_result is not None and prototype_result.route.status == "candidate",
        "errors": errors,
        "policy_id": policy.policy_id,
        "contract": contract.to_dict(),
        "prototype_input": prototype_input.to_dict() if prototype_input is not None else {},
        "prototype_result": prototype_result.to_dict() if prototype_result is not None else {},
        "route": route,
        "report_path": str(REPORT_PATH.relative_to(ROOT)),
        "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or local parser adapter dry-run gate",
    }


def render_report(result: dict[str, object]) -> str:
    policy = default_policy()
    contract = LocalPrivateParserAdapterContract(**result["contract"])
    contract_markdown = render_local_private_parser_adapter_contract(contract, policy).rstrip()
    contract_markdown = contract_markdown.replace(
        "# Local Parser Adapter Contract",
        "### Local Parser Adapter Contract",
        1,
    )
    prototype_markdown = ""
    if result["prototype_input"]:
        prototype_input = contract_to_local_private_parser_prototype_input(
            contract,
            policy,
            parser_run_id=result["prototype_input"]["parser_run_id"],
            source_stub=result["prototype_input"]["source_stub"],
            document_type=result["prototype_input"]["document_type"],
            expected_domain=result["prototype_input"]["expected_domain"],
            extracted_fields=result["prototype_input"]["extracted_fields"],
        )
        prototype = run_local_private_parser_prototype(prototype_input, policy)
        prototype_markdown = render_local_private_parser_prototype_result(prototype).rstrip()
        prototype_markdown = prototype_markdown.replace(
            "# Local Parser Prototype Result",
            "### Local Parser Prototype Result",
            1,
        )

    lines = [
        "# LPA1 Local Parser Adapter Contract",
        "",
        "> Scope: public-safe adapter contract before any real local-only file/OCR/parser implementation.",
        "",
        "## 한 줄 결론",
        "",
        "A local parser adapter now has a fixed public-safe contract: it may hand off structured facts into the existing local parser prototype and route a KIFRS1116 contract to a review-pack candidate, but it still cannot read real files, run OCR, persist source bodies, create private embeddings, or claim deletion automation.",
        "",
        "## Contract",
        "",
        contract_markdown,
        "",
        "## Handoff Result",
        "",
        prototype_markdown or "- prototype handoff did not run",
        "",
        "## What This Enables",
        "",
        "- Future local-only parser adapters have a precise output schema and safety boundary.",
        "- Parser work can be tested through `LocalPrivateParserPrototypeInput` before private file handling exists.",
        "- Gap audit can separate adapter-contract readiness from real upload/OCR/parser implementation.",
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
    result = check_local_parser_adapter_contract()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_report(result), encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Check client-private local parser adapter contract.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = write_report() if args.write else check_local_parser_adapter_contract()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"adapter_id: {result['contract']['adapter_id']}")
        print(f"route: {result['route'].get('route')}")
        print(f"route_status: {result['route'].get('status')}")
        print(f"next_leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
