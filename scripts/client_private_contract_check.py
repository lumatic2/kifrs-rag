from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs.feedback import (
    LocalPrivateCaseIntake,
    render_local_private_intake_card,
    validate_local_private_case_intake,
)


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-client-private-intake-readiness.md"


def check_client_private_contract() -> dict[str, object]:
    good = LocalPrivateCaseIntake(
        case_id="local-case-contract-check",
        source_locator="local-private://cases/local-case-contract-check/source",
        document_type="contract",
        redaction_status="reviewed_public_safe",
        allowed_output_level="review_pack_summary",
        structured_facts={"party": "lessee", "lease_term": "4 years"},
        reviewer_original_document_check=True,
        notes=["Original private document remains outside repo."],
    )
    bad = LocalPrivateCaseIntake(
        case_id="bad",
        source_locator="local-private://bad/source",
        document_type="contract",
        redaction_status="reviewed_public_safe",
        allowed_output_level="review_pack_summary",
        structured_facts={"raw_contract": "copied text"},
        reviewer_original_document_check=True,
    )

    good_issues = validate_local_private_case_intake(good)
    bad_issues = validate_local_private_case_intake(bad)
    card = render_local_private_intake_card(good)

    errors: list[str] = []
    if good_issues:
        errors.extend(f"good_case: {issue.path}: {issue.message}" for issue in good_issues)
    if not any(issue.path == "structured_facts.raw_contract" for issue in bad_issues):
        errors.append("bad_case did not reject structured_facts.raw_contract")
    if "Local-Only Client-Private Intake Card" not in card:
        errors.append("rendered card missing title")
    if "raw_contract" in card:
        errors.append("rendered card leaked raw_contract marker")
    if not REPORT_PATH.exists():
        errors.append(f"missing report: {REPORT_PATH}")

    return {
        "ok": not errors,
        "errors": errors,
        "good_issue_count": len(good_issues),
        "bad_issue_paths": [issue.path for issue in bad_issues],
        "report_exists": REPORT_PATH.exists(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Check CP1 local-only client-private intake contract.")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    result = check_client_private_contract()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"ok: {result['ok']}")
        print(f"good_issue_count: {result['good_issue_count']}")
        print(f"bad_issue_paths: {result['bad_issue_paths']}")
        print(f"report_exists: {result['report_exists']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
