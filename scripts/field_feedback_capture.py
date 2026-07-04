from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs.feedback.capture import (
    CapturedCorrection,
    FeedbackSessionNotes,
    build_feedback_capture_package,
)
from kifrs.feedback.queue import write_queue
from scripts.real_transaction_poc import sample_case


DEFAULT_OUT = Path("docs/reports/field-feedback-capture")


def sample_notes() -> FeedbackSessionNotes:
    return FeedbackSessionNotes(
        session_id="sample-session-001",
        reviewer_role="Accounting advisory reviewer",
        service_line="F-ACC",
        source="sample",
        scores={
            "workflow_fit": 4,
            "evidence_boundary_clarity": 4,
            "review_pack_usefulness": 4,
            "human_review_boundary": 5,
        },
        top_positive="Review pack order is close to a real workpaper.",
        top_risk="Lease term evidence can be under-specified.",
        required_input_additions=["lease term approval evidence"],
        review_question_additions=["Ask whether lease term approval evidence supports the stated term."],
        corrections=[
            CapturedCorrection(
                case_id="anon-lease-poc-001",
                issue="Lease term approval evidence should be requested explicitly",
                severity="medium",
                suggested_fix="Add a required reviewer question for lease term approval evidence.",
                disposition="eval_seed_candidate",
                affected_outputs=["human_review_questions", "review_pack"],
                missing_evidence=["lease term approval evidence"],
            )
        ],
        boundary_notes=["Sample notes only; not actual accountant review evidence."],
    )


def write_capture_package(out: Path) -> dict[str, Path]:
    case = sample_case()
    notes = sample_notes()
    package = build_feedback_capture_package(notes, {case.case_id: case})
    out.mkdir(parents=True, exist_ok=True)
    paths = {
        "index": out / "INDEX.md",
        "notes": out / "feedback-notes.sample.md",
        "capture_report": out / "capture-report.md",
        "queue_jsonl": out / "feedback-queue.jsonl",
        "queue_report": out / "feedback-queue-report.md",
        "manifest": out / "capture-manifest.json",
    }
    paths["notes"].write_text(package.notes_markdown, encoding="utf-8")
    paths["capture_report"].write_text(package.capture_report_markdown, encoding="utf-8")
    write_queue(paths["queue_jsonl"], package.queue_records)
    paths["queue_report"].write_text(package.queue_report_markdown, encoding="utf-8")
    paths["manifest"].write_text(
        json.dumps(
            {
                "session_id": notes.session_id,
                "source": notes.source,
                "case_id": case.case_id,
                "queue_records": len(package.queue_records),
                "public_safe": True,
                "actual_feedback_evidence": False,
                "files": {key: path.as_posix() for key, path in paths.items() if key != "index"},
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    paths["index"].write_text(render_index(paths), encoding="utf-8")
    return paths


def render_index(paths: dict[str, Path]) -> str:
    return "\n".join(
        [
            "# Field Feedback Capture Package",
            "",
            "> Public-safe sample capture package. This is not actual accountant feedback evidence.",
            "",
            "## Files",
            "",
            f"1. `{paths['notes'].name}` - sample structured feedback notes",
            f"2. `{paths['capture_report'].name}` - capture summary and next actions",
            f"3. `{paths['queue_jsonl'].name}` - queue records generated from safe corrections",
            f"4. `{paths['queue_report'].name}` - queue report",
            f"5. `{paths['manifest'].name}` - machine-readable capture manifest",
            "",
            "## Boundary",
            "",
            "- The sample notes are not actual accountant feedback.",
            "- Protected payloads are rejected before queue conversion.",
            "- Raw contracts, customer identifiers, copied source bodies, private filings, parsed standards, embeddings, and workpaper payloads are not stored.",
            "",
            "## Regeneration",
            "",
            "```powershell",
            "python scripts\\field_feedback_capture.py --out docs\\reports\\field-feedback-capture",
            "```",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a public-safe field feedback capture sample package.")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    paths = write_capture_package(args.out)
    print(f"wrote {paths['index'].parent}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
