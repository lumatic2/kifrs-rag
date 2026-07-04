from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs.feedback.incorporation import (
    render_incorporation_report,
    render_review_question_supplement,
)
from kifrs.feedback.queue import load_queue


DEFAULT_QUEUE = Path("docs/reports/real-transaction-poc/feedback-queue.jsonl")
DEFAULT_OUT = Path("docs/reports/2026-07-05-af3-feedback-incorporation-report.md")
DEFAULT_QUESTIONS_OUT = Path("docs/reports/field-feedback/2026-07-05-incorporated-review-questions.md")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate an accountant feedback incorporation report.")
    parser.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--questions-out", type=Path, default=DEFAULT_QUESTIONS_OUT)
    args = parser.parse_args()

    records = load_queue(args.queue)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.questions_out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render_incorporation_report(records), encoding="utf-8")
    args.questions_out.write_text(render_review_question_supplement(records), encoding="utf-8")
    print(f"wrote {args.out}")
    print(f"wrote {args.questions_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
