"""Public-safe transaction PoC bridge from anonymized case intake to review pack.

This module keeps the real-case loop metadata-only. It accepts structured,
sanitized facts and delegates accounting judgment to the existing KIFRS1116
review-pack pipeline.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from kifrs.workflows.kifrs1116.review_pack import (
    ReviewPack,
    generate_review_pack,
    render_review_pack_markdown,
)
from kifrs.workflows.kifrs1116.schema import Lease1116

from .case_intake import CaseIntake, ReviewerCorrection, route_case, validate_case_intake
from .queue import FeedbackQueueRecord, make_queue_record, render_queue_report


SUPPORTED_POC_ROUTE = "kifrs1116_review_pack"


@dataclass(frozen=True)
class TransactionPoCPackage:
    case: CaseIntake
    correction: ReviewerCorrection
    review_pack: ReviewPack
    review_pack_markdown: str
    queue_record: FeedbackQueueRecord
    input_card_markdown: str
    queue_report_markdown: str


def build_transaction_poc_package(
    case: CaseIntake,
    correction: ReviewerCorrection,
    *,
    source: str = "real-transaction-poc-sample",
) -> TransactionPoCPackage:
    """Build a public-safe PoC package for one anonymized KIFRS1116 case."""
    lease = case_to_lease1116(case)
    pack = generate_review_pack(lease)
    queue_record = make_queue_record(case, correction, source=source)
    return TransactionPoCPackage(
        case=case,
        correction=correction,
        review_pack=pack,
        review_pack_markdown=render_review_pack_markdown(pack),
        queue_record=queue_record,
        input_card_markdown=render_anonymized_input_card(case),
        queue_report_markdown=render_queue_report([queue_record], title="Real Transaction PoC Feedback Queue"),
    )


def case_to_lease1116(case: CaseIntake) -> Lease1116:
    """Convert a validated anonymized case card into the existing 1116 schema."""
    issues = validate_case_intake(case)
    if issues:
        joined = "; ".join(f"{issue.path}: {issue.message}" for issue in issues)
        raise ValueError(f"invalid anonymized case: {joined}")

    route = route_case(case)
    if route.status != "candidate" or route.route != SUPPORTED_POC_ROUTE:
        raise ValueError(f"case is not a supported 1116 review-pack candidate: {route.status} / {route.route}")

    facts = dict(case.structured_facts)
    required = [
        "party",
        "lease_term_years",
        "annual_payment",
        "discount_rate",
        "annuity_factor",
    ]
    missing = [key for key in required if key not in facts]
    if missing:
        raise ValueError(f"missing numeric 1116 facts for PoC adapter: {', '.join(missing)}")

    party = _string_fact(facts, "party")
    if party not in {"lessee", "lessor"}:
        raise ValueError("party must be 'lessee' or 'lessor'")

    payment_timing = _string_fact(facts, "payment_timing", default="arrears")
    if payment_timing not in {"arrears", "advance"}:
        raise ValueError("payment_timing must be 'arrears' or 'advance'")

    return Lease1116(
        label=case.case_id,
        party=party,
        annual_payment=_float_fact(facts, "annual_payment"),
        lease_term_years=_int_fact(facts, "lease_term_years"),
        discount_rate=_float_fact(facts, "discount_rate"),
        annuity_factor=_float_fact(facts, "annuity_factor"),
        payment_timing=payment_timing,
        identified_asset=_bool_fact(facts, "identified_asset", default=True),
        supplier_substantive_substitution_right=_bool_fact(
            facts, "supplier_substantive_substitution_right", default=False
        ),
        lessee_gets_economic_benefits=_bool_fact(facts, "lessee_gets_economic_benefits", default=True),
        lessee_directs_use=_bool_fact(facts, "lessee_directs_use", default=True),
        prepaid_lease_payment=_float_fact(facts, "prepaid_lease_payment", default=0.0),
        lease_incentive_received=_float_fact(facts, "lease_incentive_received", default=0.0),
        initial_direct_costs=_float_fact(facts, "initial_direct_costs", default=0.0),
    )


def render_anonymized_input_card(case: CaseIntake) -> str:
    """Render the sanitized input card without private payloads."""
    route = route_case(case)
    lines = [
        f"# Anonymized Transaction Input Card - {case.case_id}",
        "",
        f"- Domain: {case.domain_hint.upper()}",
        f"- Route: {route.route}",
        f"- Route status: {route.status}",
        f"- Title: {case.anonymized_title}",
        f"- Summary: {case.fact_pattern_summary}",
        "",
        "## Structured Facts",
        "",
        "| Field | Value |",
        "|---|---|",
    ]
    for key, value in sorted(case.structured_facts.items()):
        lines.append(f"| {key} | {_display_value(value)} |")

    lines.extend(["", "## Requested Outputs", ""])
    if case.requested_outputs:
        lines.extend(f"- {item}" for item in case.requested_outputs)
    else:
        lines.append("- none")

    lines.extend(["", "## Source Boundary", ""])
    if case.source_boundaries:
        lines.extend(f"- {item}" for item in case.source_boundaries)
    else:
        lines.append("- Only structured, sanitized facts are stored.")

    lines.extend([
        "",
        "## Reviewer Questions",
        "",
    ])
    if case.reviewer_questions:
        lines.extend(f"- {item}" for item in case.reviewer_questions)
    else:
        lines.append("- none")

    lines.extend([
        "",
        "## Boundary",
        "",
        "- This card stores structured facts only.",
        "- It does not store copied contract text, customer identifiers, private filings, parsed standards, embeddings, or workpaper payloads.",
    ])
    return "\n".join(lines) + "\n"


def _float_fact(facts: dict[str, Any], key: str, *, default: float | None = None) -> float:
    value = facts.get(key, default)
    if value is None:
        raise ValueError(f"{key} is required")
    if isinstance(value, bool):
        raise ValueError(f"{key} must be numeric")
    return float(value)


def _int_fact(facts: dict[str, Any], key: str) -> int:
    value = facts.get(key)
    if value is None or isinstance(value, bool):
        raise ValueError(f"{key} must be an integer")
    return int(value)


def _bool_fact(facts: dict[str, Any], key: str, *, default: bool) -> bool:
    value = facts.get(key, default)
    if not isinstance(value, bool):
        raise ValueError(f"{key} must be a boolean")
    return value


def _string_fact(facts: dict[str, Any], key: str, *, default: str | None = None) -> str:
    value = facts.get(key, default)
    if not isinstance(value, str):
        raise ValueError(f"{key} must be a string")
    return value


def _display_value(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:g}"
    return str(value)
