from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs.feedback import (  # noqa: E402
    ClientPrivateDeletionAttestation,
    render_client_private_deletion_attestation,
    validate_client_private_deletion_attestation,
)
from scripts.client_private_parser_dry_run_fixture_check import default_fixture  # noqa: E402
from scripts.client_private_upload_storage_policy_check import default_policy  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-lda1-local-deletion-attestation-gate.md"


def default_attestation() -> ClientPrivateDeletionAttestation:
    fixture = default_fixture()
    policy = default_policy()
    return ClientPrivateDeletionAttestation(
        attestation_id="lda1-synthetic-lease-contract-deletion-attestation",
        fixture_id=fixture.fixture_id,
        source_stub=fixture.source_stub,
        deletion_status="deleted",
        deletion_mode=policy.deletion_mode,
        operator_check=(
            "operator verified gitignored local-only paths and checked the synthetic dry-run raw file was deleted "
            "before report write"
        ),
        allowed_public_artifact="deletion attestation",
        deleted_before_report_write=True,
        raw_file_present=False,
        parsed_body_present=False,
        ocr_text_present=False,
        embedding_present=False,
    )


def check_deletion_attestation() -> dict[str, object]:
    policy = default_policy()
    fixture = default_fixture()
    attestation = default_attestation()
    issues = validate_client_private_deletion_attestation(attestation, policy, fixture)
    return {
        "ok": not issues,
        "errors": [f"{issue.path}: {issue.message}" for issue in issues],
        "policy_id": policy.policy_id,
        "fixture_id": fixture.fixture_id,
        "attestation": attestation.to_dict(),
        "report_path": str(REPORT_PATH.relative_to(ROOT)),
        "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or client-private local parser close gate",
    }


def render_report(result: dict[str, object]) -> str:
    policy = default_policy()
    fixture = default_fixture()
    attestation = ClientPrivateDeletionAttestation(**result["attestation"])
    attestation_markdown = render_client_private_deletion_attestation(attestation, policy, fixture).rstrip()
    attestation_markdown = attestation_markdown.replace(
        "# Client-Private Deletion Attestation",
        "### Client-Private Deletion Attestation",
        1,
    )
    lines = [
        "# LDA1 Local Deletion Attestation Gate",
        "",
        "> Scope: public-safe deletion evidence contract for future local client-private parser work.",
        "",
        "## 한 줄 결론",
        "",
        "A future private parser now has a deletion attestation gate: public reports may record that a local-only dry-run source was deleted before report write, but they still may not store raw files, OCR text, parsed bodies, identifiers, or embeddings.",
        "",
        "## Attestation",
        "",
        attestation_markdown,
        "",
        "## What This Enables",
        "",
        "- A future local parser close gate can require deletion evidence without committing private payloads.",
        "- Gap audit can distinguish deletion-attestation readiness from actual deletion automation.",
        "- Operators get a concrete public-safe record shape for client-private dry runs.",
        "",
        "## Still Not Implemented",
        "",
        "- real file deletion automation",
        "- file upload UI",
        "- OCR",
        "- real private document parser",
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
    result = check_deletion_attestation()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_report(result), encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Check client-private local deletion attestation contract.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = write_report() if args.write else check_deletion_attestation()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"attestation_id: {result['attestation']['attestation_id']}")
        print(f"deletion_status: {result['attestation']['deletion_status']}")
        print(f"deleted_before_report_write: {result['attestation']['deleted_before_report_write']}")
        print(f"next_leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
