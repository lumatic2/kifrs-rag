from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs.feedback import (  # noqa: E402
    LocalFixtureParserAdapterInput,
    render_local_fixture_parser_adapter_result,
    run_local_fixture_parser_adapter,
    validate_local_fixture_parser_adapter_input,
)
from scripts.client_private_local_parser_adapter_contract_check import default_adapter_contract  # noqa: E402
from scripts.client_private_upload_storage_policy_check import default_policy  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-rlp2-local-fixture-parser-adapter.md"


def default_fixture_adapter_input() -> LocalFixtureParserAdapterInput:
    return LocalFixtureParserAdapterInput(
        adapter_run_id="rlp2-local-fixture-lease-contract",
        source_stub="local-private://fixture/rlp2-local-fixture-lease-contract",
        document_type="contract",
        expected_domain="KIFRS1116",
        structured_fact_candidates={
            "party": "lessee",
            "lease_term": "5 years with renewal option excluded from structured facts",
            "payment_schedule": "monthly fixed payments",
            "ignored_note": "operator-only note intentionally excluded from structured facts",
        },
        operator_ack="fixture-structured-facts-only-public-safe",
        raw_fixture_text_present=False,
        ocr_text_present=False,
        source_excerpt_present=False,
        embedding_present=False,
    )


def check_local_fixture_parser_adapter() -> dict[str, object]:
    policy = default_policy()
    contract = default_adapter_contract()
    adapter_input = default_fixture_adapter_input()
    issues = validate_local_fixture_parser_adapter_input(adapter_input, contract, policy)
    adapter_result = run_local_fixture_parser_adapter(adapter_input, contract, policy)
    route = adapter_result.prototype_result.route.to_dict()
    return {
        "ok": not issues and adapter_result.ok,
        "errors": [f"{issue.path}: {issue.message}" for issue in issues] + list(adapter_result.errors),
        "policy_id": policy.policy_id,
        "contract_id": contract.adapter_id,
        "adapter_input": adapter_input.to_dict(),
        "adapter_result": adapter_result.to_dict(),
        "route": route,
        "review_questions": list(adapter_result.review_questions),
        "structured_fact_keys": sorted(adapter_result.structured_facts),
        "report_path": str(REPORT_PATH.relative_to(ROOT)),
        "next_leaf": "RLP3_deletion_automation_simulation",
    }


def render_report(result: dict[str, object]) -> str:
    policy = default_policy()
    contract = default_adapter_contract()
    adapter_input = LocalFixtureParserAdapterInput(**result["adapter_input"])
    adapter_result = run_local_fixture_parser_adapter(adapter_input, contract, policy)
    adapter_markdown = render_local_fixture_parser_adapter_result(adapter_result).rstrip()
    adapter_markdown = adapter_markdown.replace(
        "# Local Fixture Parser Adapter Result",
        "### Local Fixture Parser Adapter Result",
        1,
    )
    lines = [
        "# RLP2 Local Fixture Parser Adapter",
        "",
        "> Scope: local-safe fixture adapter that converts fixture-like input into structured facts and review questions.",
        "",
        "## 한 줄 결론",
        "",
        "RLP2 adds a local fixture adapter path. It accepts fixture-shaped structured facts, strips extra operator-only candidates, emits the contract-required structured facts, generates review questions, and routes the case through the existing local parser prototype. It still does not read real files, copy raw text, run OCR, include source excerpts, or create private embeddings.",
        "",
        "## Adapter Result",
        "",
        adapter_markdown,
        "",
        "## What Changed From RLP1",
        "",
        "- RLP1 only inventoried reusable parser assets.",
        "- RLP2 now proves a fixture-like input can become structured facts plus human review questions.",
        "- The output is still public-safe and structured-facts-only.",
        "",
        "## Still Not Implemented",
        "",
        "- real private-file parser",
        "- OCR",
        "- upload UI",
        "- private embedding/index namespace",
        "- deletion automation beyond the existing attestation contract",
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
    result = check_local_fixture_parser_adapter()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_report(result), encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Run RLP2 local fixture parser adapter.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = write_report() if args.write else check_local_fixture_parser_adapter()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"route: {result['route']['route']}")
        print(f"route_status: {result['route']['status']}")
        print(f"structured_fact_keys: {', '.join(result['structured_fact_keys'])}")
        print(f"review_questions: {len(result['review_questions'])}")
        print(f"next_leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
