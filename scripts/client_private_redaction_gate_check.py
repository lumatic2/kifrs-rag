from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs.feedback import (  # noqa: E402
    LocalPrivateCaseIntake,
    redact_local_private_case_for_public,
    render_redacted_client_private_summary,
)


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-client-private-intake-readiness.md"


def check_client_private_redaction_gate() -> dict[str, object]:
    case = LocalPrivateCaseIntake(
        case_id="local-case-redaction-check",
        source_locator="local-private://cases/local-case-redaction-check/source",
        document_type="contract",
        redaction_status="reviewed_public_safe",
        allowed_output_level="review_pack_summary",
        structured_facts={"party": "lessee", "lease_term": "4 years"},
        reviewer_original_document_check=True,
        notes=["Private source note remains local-only."],
    )
    unreviewed = LocalPrivateCaseIntake(
        **{**case.to_dict(), "case_id": "bad-unreviewed", "reviewer_original_document_check": False}
    )

    errors: list[str] = []
    summary = redact_local_private_case_for_public(case)
    data = summary.to_dict()
    rendered = render_redacted_client_private_summary(summary)

    if "source_locator" in data:
        errors.append("redacted summary leaked source_locator field")
    if "notes" in data:
        errors.append("redacted summary leaked notes field")
    if "local-private://cases" in rendered:
        errors.append("rendered summary leaked local private locator")
    if "Private source note remains local-only." in rendered:
        errors.append("rendered summary leaked local-only note")

    try:
        redact_local_private_case_for_public(unreviewed)
    except ValueError as exc:
        rejected_unreviewed = "reviewer_original_document_check" in str(exc)
    else:
        rejected_unreviewed = False
    if not rejected_unreviewed:
        errors.append("redaction gate did not reject unreviewed original-document check")

    if not REPORT_PATH.exists():
        errors.append(f"missing report: {REPORT_PATH}")

    return {
        "ok": not errors,
        "errors": errors,
        "summary_keys": sorted(data),
        "rejected_unreviewed": rejected_unreviewed,
        "report_exists": REPORT_PATH.exists(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Check CP2 public-safe redaction gate.")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    result = check_client_private_redaction_gate()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"ok: {result['ok']}")
        print(f"summary_keys: {result['summary_keys']}")
        print(f"rejected_unreviewed: {result['rejected_unreviewed']}")
        print(f"report_exists: {result['report_exists']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
