from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs.feedback import (
    CaseIntake,
    ReviewerCorrection,
    case_to_eval_seed_candidate,
    render_feedback_summary_markdown,
    route_case,
    validate_case_intake,
    validate_reviewer_correction,
)


DEFAULT_OUT = Path("docs/reports/2026-07-05-rc4-real-case-feedback-loop-report.md")


def sample_case() -> CaseIntake:
    return CaseIntake(
        case_id="anon-case-lease-001",
        domain_hint="KIFRS1116",
        anonymized_title="Anonymized lease modification candidate",
        fact_pattern_summary=(
            "Sanitized lessee lease modification facts prepared for routing; "
            "no customer identifier or source body is stored."
        ),
        structured_facts={
            "party": "lessee",
            "lease_term": "remaining term and extension fact summarized",
            "payment_schedule": "periodic payments summarized",
            "modification_type": "extension candidate",
        },
        requested_outputs=["review_pack", "journal_entry_draft", "human_review_questions"],
        source_boundaries=[
            "contract clauses are summarized as structured facts, not copied",
            "reviewer must inspect the original contract outside this repo",
        ],
        reviewer_questions=[
            "Is the extension reasonably certain based on management evidence?",
            "Does the modification require separate lease treatment?",
        ],
    )


def sample_correction() -> ReviewerCorrection:
    return ReviewerCorrection(
        case_id="anon-case-lease-001",
        issue="Renewal certainty evidence should be explicit before drafting the review pack.",
        severity="medium",
        suggested_fix="Add a required evidence question for management's renewal assessment.",
        missing_evidence=["management renewal assessment", "approved modification date"],
        disposition="eval_seed_candidate",
        affected_outputs=["review_pack", "human_review_questions"],
    )


def render_report() -> str:
    case = sample_case()
    correction = sample_correction()
    case_issues = validate_case_intake(case)
    correction_issues = validate_reviewer_correction(correction)
    route = route_case(case)
    seed = case_to_eval_seed_candidate(case, correction)

    lines = [
        "# RC4 Real Case Feedback Loop Report",
        "",
        "> This is a public-safe sample. It is not an actual client case.",
        "",
        "## Validation",
        "",
        f"- Case validation issues: {len(case_issues)}",
        f"- Correction validation issues: {len(correction_issues)}",
        f"- Route: {route.route}",
        f"- Route status: {route.status}",
        "",
        "## Eval Seed Candidate",
        "",
        "| Field | Value |",
        "|---|---|",
    ]
    for key in ("case_id", "domain", "route", "status", "severity"):
        lines.append(f"| {key} | {seed[key]} |")
    lines.extend([
        f"| issue | {seed['issue']} |",
        f"| expected_improvement | {seed['expected_improvement']} |",
        "",
        "## Feedback Summary",
        "",
        render_feedback_summary_markdown(case, correction).rstrip(),
        "",
        "## Boundary",
        "",
        "- No raw contract, customer identifier, copied source body, private filing, parsed standard, embedding, or workpaper payload is stored.",
        "- The route is a candidate, not a final accounting conclusion.",
        "- Reviewer correction becomes an eval/backlog candidate only after validation.",
    ])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a public-safe real-case feedback loop sample report.")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render_report(), encoding="utf-8")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
