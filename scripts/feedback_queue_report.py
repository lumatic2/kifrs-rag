from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs.feedback import CaseIntake, ReviewerCorrection
from kifrs.feedback.queue import (
    load_queue,
    make_queue_record,
    render_queue_report,
    write_queue,
)


DEFAULT_QUEUE = Path("docs/feedback/feedback_queue.sample.jsonl")
DEFAULT_OUT = Path("docs/reports/2026-07-05-fi3-feedback-queue-report.md")


def sample_records():
    lease_case = CaseIntake(
        case_id="anon-case-lease-001",
        domain_hint="KIFRS1116",
        anonymized_title="Anonymized lease modification candidate",
        fact_pattern_summary="Sanitized lease facts for feedback queue sample.",
        structured_facts={
            "party": "lessee",
            "lease_term": "remaining term and extension fact summarized",
            "payment_schedule": "periodic payments summarized",
        },
        requested_outputs=["review_pack", "human_review_questions"],
    )
    lease_correction = ReviewerCorrection(
        case_id="anon-case-lease-001",
        issue="Renewal certainty evidence should be explicit.",
        severity="medium",
        suggested_fix="Add a required evidence question for management renewal assessment.",
        missing_evidence=["management renewal assessment"],
        disposition="eval_seed_candidate",
        affected_outputs=["human_review_questions"],
    )

    instrument_case = CaseIntake(
        case_id="anon-case-fi-001",
        domain_hint="KIFRS1109",
        anonymized_title="Anonymized financial instrument classification candidate",
        fact_pattern_summary="Sanitized financial instrument facts for backlog queue sample.",
        structured_facts={
            "instrument_type": "debt",
            "business_model": "hold to collect",
            "cash_flow_terms": "principal and interest only candidate",
        },
        requested_outputs=["review_pack"],
    )
    instrument_correction = ReviewerCorrection(
        case_id="anon-case-fi-001",
        issue="Business model evidence checklist should mention sale frequency.",
        severity="high",
        suggested_fix="Add sale frequency evidence to the 1109 human-review checklist.",
        missing_evidence=["sale frequency history"],
        disposition="backlog_candidate",
        affected_outputs=["review_pack"],
    )

    return [
        make_queue_record(lease_case, lease_correction, source="public-safe-sample"),
        make_queue_record(instrument_case, instrument_correction, source="public-safe-sample"),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate public-safe feedback queue sample and report.")
    parser.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--no-write-sample", action="store_true", help="Read existing queue instead of writing sample records.")
    args = parser.parse_args()

    if args.no_write_sample:
        records = load_queue(args.queue)
    else:
        records = sample_records()
        write_queue(args.queue, records)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render_queue_report(records, title="FI3 Feedback Queue Report"), encoding="utf-8")
    print(f"wrote {args.queue}")
    print(f"wrote {args.out}")
    print(f"records: {len(records)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
