from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs.feedback import (  # noqa: E402
    LocalPrivateParserPrototypeInput,
    render_local_private_parser_prototype_result,
    run_local_private_parser_prototype,
    validate_local_private_parser_prototype_input,
)
from scripts.client_private_upload_storage_policy_check import default_policy  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-lpp1-local-parser-prototype-spike.md"


def default_parser_input() -> LocalPrivateParserPrototypeInput:
    return LocalPrivateParserPrototypeInput(
        parser_run_id="lpp1-synthetic-lease-parser-prototype",
        source_stub="local-private://dry-run/synthetic-lease-parser-prototype",
        document_type="contract",
        expected_domain="KIFRS1116",
        extracted_fields={
            "party": "lessee",
            "lease_term": "5 years",
            "payment_schedule": "monthly fixed payments",
        },
        parser_mode="structured_facts_only",
        allowed_output_level="review_pack_summary",
        redaction_status="reviewed_public_safe",
        reviewer_original_document_check=True,
        raw_file_present=False,
        parsed_body_present=False,
        ocr_text_present=False,
        embedding_present=False,
    )


def check_local_parser_prototype() -> dict[str, object]:
    policy = default_policy()
    parser_input = default_parser_input()
    input_issues = validate_local_private_parser_prototype_input(parser_input, policy)
    result = run_local_private_parser_prototype(parser_input, policy) if not input_issues else None
    route = result.route.to_dict() if result is not None else {}
    return {
        "ok": not input_issues and result is not None and result.route.status == "candidate",
        "errors": [f"{issue.path}: {issue.message}" for issue in input_issues],
        "policy_id": policy.policy_id,
        "parser_input": parser_input.to_dict(),
        "prototype_result": result.to_dict() if result is not None else {},
        "route": route,
        "report_path": str(REPORT_PATH.relative_to(ROOT)),
        "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or local parser prototype close gate",
    }


def render_report(result: dict[str, object]) -> str:
    prototype_markdown = ""
    if result["prototype_result"]:
        prototype = run_local_private_parser_prototype(
            LocalPrivateParserPrototypeInput(**result["parser_input"]),
            default_policy(),
        )
        prototype_markdown = render_local_private_parser_prototype_result(prototype).rstrip()
        prototype_markdown = prototype_markdown.replace(
            "# Local Parser Prototype Result",
            "### Local Parser Prototype Result",
            1,
        )
    lines = [
        "# LPP1 Local Parser Prototype Spike",
        "",
        "> Scope: first synthetic local parser prototype that converts parser-shaped input into public-safe structured facts.",
        "",
        "## 한 줄 결론",
        "",
        "A first local parser prototype now exists at the synthetic contract level: it accepts parser-shaped structured input, produces a redacted client-private summary, routes it to a KIFRS1116 review-pack candidate, and emits deletion attestation. It still does not read real files, run OCR, parse source bodies, delete files, or create private embeddings.",
        "",
        "## Prototype Result",
        "",
        prototype_markdown or "- prototype did not run",
        "",
        "## What This Enables",
        "",
        "- The next implementation can replace synthetic extracted fields with a local-only parser adapter.",
        "- Review-pack routing can be tested from parser-shaped output without touching private source documents.",
        "- Public artifacts can prove the parser contract without storing raw payloads.",
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
    result = check_local_parser_prototype()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_report(result), encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Run first client-private local parser prototype spike.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = write_report() if args.write else check_local_parser_prototype()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"parser_run_id: {result['parser_input']['parser_run_id']}")
        print(f"route: {result['route'].get('route')}")
        print(f"route_status: {result['route'].get('status')}")
        print(f"next_leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
