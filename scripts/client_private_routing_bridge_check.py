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
    route_redacted_client_private_summary,
)


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-client-private-intake-readiness.md"


def check_client_private_routing_bridge() -> dict[str, object]:
    case = LocalPrivateCaseIntake(
        case_id="local-case-routing-check",
        source_locator="local-private://cases/local-case-routing-check/source",
        document_type="contract",
        redaction_status="reviewed_public_safe",
        allowed_output_level="review_pack_summary",
        structured_facts={
            "party": "lessee",
            "lease_term": "4 years",
            "payment_schedule": "annual arrears",
        },
        reviewer_original_document_check=True,
    )
    schema_only = LocalPrivateCaseIntake(**{**case.to_dict(), "allowed_output_level": "schema_only"})

    summary = redact_local_private_case_for_public(case)
    route_1116 = route_redacted_client_private_summary(summary, domain_hint="KIFRS1116")
    route_1109 = route_redacted_client_private_summary(summary, domain_hint="KIFRS1109")
    route_blocked = route_redacted_client_private_summary(
        redact_local_private_case_for_public(schema_only),
        domain_hint="KIFRS1116",
    )

    errors: list[str] = []
    if route_1116.status != "candidate" or route_1116.route != "kifrs1116_review_pack":
        errors.append(f"1116 route not candidate: {route_1116.to_dict()}")
    if route_1109.status != "needs_more_facts":
        errors.append(f"1109 route should need more facts: {route_1109.to_dict()}")
    if route_blocked.status != "blocked":
        errors.append(f"schema-only route should be blocked: {route_blocked.to_dict()}")
    if not REPORT_PATH.exists():
        errors.append(f"missing report: {REPORT_PATH}")

    return {
        "ok": not errors,
        "errors": errors,
        "route_1116": route_1116.to_dict(),
        "route_1109": route_1109.to_dict(),
        "route_blocked": route_blocked.to_dict(),
        "report_exists": REPORT_PATH.exists(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Check CP3 client-private review-pack routing bridge.")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    result = check_client_private_routing_bridge()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"ok: {result['ok']}")
        print(f"route_1116_status: {result['route_1116']['status']}")
        print(f"route_1116: {result['route_1116']['route']}")
        print(f"route_1109_status: {result['route_1109']['status']}")
        print(f"route_blocked_status: {result['route_blocked']['status']}")
        print(f"report_exists: {result['report_exists']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
