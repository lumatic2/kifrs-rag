from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs.feedback import (  # noqa: E402
    ClientPrivateParserDryRunFixture,
    render_client_private_parser_dry_run_fixture,
    route_redacted_client_private_summary,
    redact_local_private_case_for_public,
    validate_client_private_parser_dry_run_fixture,
)
from scripts.client_private_upload_storage_policy_check import default_policy  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-pdf1-private-parser-dry-run-fixture.md"


def default_fixture() -> ClientPrivateParserDryRunFixture:
    return ClientPrivateParserDryRunFixture(
        fixture_id="pdf1-synthetic-lease-contract-dry-run",
        parser_mode="structured_facts_only",
        document_type="contract",
        source_stub="local-private://dry-run/synthetic-lease-contract",
        expected_domain="KIFRS1116",
        structured_facts={
            "party": "lessee",
            "lease_term": "5 years",
            "payment_schedule": "monthly fixed payments",
        },
        allowed_output_level="review_pack_summary",
        redaction_status="reviewed_public_safe",
        reviewer_original_document_check=True,
        deletion_attestation="synthetic dry-run raw file deleted before report write",
    )


def check_parser_dry_run_fixture() -> dict[str, object]:
    policy = default_policy()
    fixture = default_fixture()
    issues = validate_client_private_parser_dry_run_fixture(fixture, policy)
    summary = redact_local_private_case_for_public(fixture.to_local_private_case())
    route = route_redacted_client_private_summary(summary, domain_hint=fixture.expected_domain)
    return {
        "ok": not issues,
        "errors": [f"{issue.path}: {issue.message}" for issue in issues],
        "policy_id": policy.policy_id,
        "fixture": fixture.to_dict(),
        "redacted_summary": summary.to_dict(),
        "route": route.to_dict(),
        "report_path": str(REPORT_PATH.relative_to(ROOT)),
        "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or local deletion attestation gate",
    }


def render_report(result: dict[str, object]) -> str:
    fixture = ClientPrivateParserDryRunFixture(**result["fixture"])
    policy = default_policy()
    fixture_markdown = render_client_private_parser_dry_run_fixture(fixture, policy).rstrip()
    fixture_markdown = fixture_markdown.replace(
        "# Client-Private Parser Dry-Run Fixture",
        "### Client-Private Parser Dry-Run Fixture",
        1,
    )
    lines = [
        "# PDF1 Private Parser Dry-Run Fixture",
        "",
        "> Scope: synthetic, public-safe parser input/output contract for future client-private parser work.",
        "",
        "## 한 줄 결론",
        "",
        "A future private parser now has a dry-run fixture contract: it may output redacted structured facts that route to a review-pack candidate, but it still may not store raw files, OCR text, parsed bodies, identifiers, or embeddings.",
        "",
        "## Fixture",
        "",
        fixture_markdown,
        "",
        "## Route Result",
        "",
        f"- Route: {result['route']['route']}",
        f"- Status: {result['route']['status']}",
        f"- Missing facts: {result['route']['missing_facts']}",
        "",
        "## What This Enables",
        "",
        "- A future local parser can be tested against a known output contract before touching private files.",
        "- The review-pack routing bridge can be checked from parser-shaped structured facts.",
        "- The public repo keeps only synthetic fixture metadata and redacted output.",
        "",
        "## Still Not Implemented",
        "",
        "- file upload UI",
        "- OCR",
        "- real private document parser",
        "- local deletion attestation automation",
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
    result = check_parser_dry_run_fixture()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_report(result), encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Check client-private parser dry-run fixture contract.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = write_report() if args.write else check_parser_dry_run_fixture()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"fixture_id: {result['fixture']['fixture_id']}")
        print(f"parser_mode: {result['fixture']['parser_mode']}")
        print(f"route: {result['route']['route']}")
        print(f"route_status: {result['route']['status']}")
        print(f"next_leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
