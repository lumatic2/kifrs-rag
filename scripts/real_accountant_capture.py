from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

try:
    from kifrs.feedback.capture import CapturedCorrection, FeedbackSessionNotes, build_feedback_capture_package
    from kifrs.feedback.queue import write_queue
    from scripts.real_accountant_notes_check import check_actual_notes
    from scripts.real_transaction_poc import sample_case
except ModuleNotFoundError:
    import sys

    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from kifrs.feedback.capture import CapturedCorrection, FeedbackSessionNotes, build_feedback_capture_package
    from kifrs.feedback.queue import write_queue
    from scripts.real_accountant_notes_check import check_actual_notes
    from scripts.real_transaction_poc import sample_case


DEFAULT_NOTES = Path("docs/reports/real-accountant-session/actual-feedback-notes.md")
DEFAULT_OUT = Path("docs/reports/real-accountant-session")


def capture_actual_notes(notes_path: Path, out: Path, *, root: Path | None = None) -> dict[str, Path]:
    root = root or Path.cwd()
    ok, errors = check_actual_notes(notes_path)
    if not ok:
        raise ValueError("; ".join(errors))

    notes = parse_actual_notes(notes_path)
    case = sample_case()
    package = build_feedback_capture_package(
        notes,
        {case.case_id: case},
        source="real-accountant-session",
    )

    out.mkdir(parents=True, exist_ok=True)
    paths = {
        "capture_report": out / "capture-report.md",
        "queue_jsonl": out / "feedback-queue.jsonl",
        "queue_report": out / "feedback-queue-report.md",
        "manifest": out / "capture-manifest.json",
    }
    paths["capture_report"].write_text(package.capture_report_markdown, encoding="utf-8")
    write_queue(paths["queue_jsonl"], package.queue_records)
    paths["queue_report"].write_text(package.queue_report_markdown, encoding="utf-8")
    paths["manifest"].write_text(
        json.dumps(
            {
                "actual_feedback_evidence": True,
                "case_ids": sorted({record.case_id for record in package.queue_records}),
                "files": {key: _relative_to_root(root, path) for key, path in paths.items() if key != "manifest"},
                "notes_file": _relative_to_root(root, notes_path),
                "public_safe": True,
                "queue_records": len(package.queue_records),
                "session_id": notes.session_id,
                "source": notes.source,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return paths


def parse_actual_notes(path: Path) -> FeedbackSessionNotes:
    text = path.read_text(encoding="utf-8")
    metadata = _metadata(text)
    corrections = _corrections(text)
    return FeedbackSessionNotes(
        session_id=_session_id(metadata["Date"]),
        reviewer_role=metadata["Reviewer role"],
        service_line=metadata["Reviewer service-line"],
        source="field_session",
        scores=_scores(text),
        top_positive=_section_text(text, "## Top Positive"),
        top_risk=_section_text(text, "## Top Risk"),
        required_input_additions=_bullets(text, "## Missing Inputs"),
        review_question_additions=_bullets(text, "## Review Question Additions"),
        corrections=corrections,
        boundary_notes=["Actual accountant feedback notes passed public-safe checker."],
    )


def _metadata(text: str) -> dict[str, str]:
    required = ["Date", "Reviewer role", "Reviewer service-line", "Reviewer experience context", "Session mode"]
    data: dict[str, str] = {}
    for key in required:
        value = _line_value(text, f"- {key}:")
        if not value:
            raise ValueError(f"missing metadata: {key}")
        data[key] = value
    return data


def _scores(text: str) -> dict[str, int]:
    mapping = {
        "Workflow fit (1-5)": "workflow_fit",
        "Evidence boundary clarity (1-5)": "evidence_boundary_clarity",
        "Review pack usefulness (1-5)": "review_pack_usefulness",
        "Human-review boundary clarity (1-5)": "human_review_boundary",
        "Real-case PoC willingness (1-5)": "real_case_poc_willingness",
    }
    scores: dict[str, int] = {}
    for label, key in mapping.items():
        value = _line_value(text, f"- {label}:")
        if value:
            scores[key] = int(value)
    return scores


def _corrections(text: str) -> list[CapturedCorrection]:
    section = _section_raw(text, "## Safe Correction Candidates")
    chunks = re.split(r"^###\s+", section, flags=re.MULTILINE)
    corrections: list[CapturedCorrection] = []
    for chunk in chunks:
        if not chunk.strip() or chunk.strip().startswith("Candidate") is False:
            continue
        fields = _candidate_fields(chunk)
        corrections.append(
            CapturedCorrection(
                case_id=fields["Case id"],
                issue=fields["Issue"],
                severity=fields["Severity"],
                suggested_fix=fields["Suggested fix"],
                missing_evidence=_split_list(fields["Missing evidence"]),
                disposition=fields["Disposition"],
                affected_outputs=_split_list(fields["Affected outputs"]),
            )
        )
    if not corrections:
        raise ValueError("at least one safe correction candidate is required")
    return corrections


def _candidate_fields(chunk: str) -> dict[str, str]:
    required = ["Case id", "Issue", "Severity", "Suggested fix", "Missing evidence", "Disposition", "Affected outputs"]
    fields: dict[str, str] = {}
    for key in required:
        value = _line_value(chunk, f"- {key}:")
        if not value:
            raise ValueError(f"missing correction field: {key}")
        fields[key] = value
    return fields


def _section_raw(text: str, heading: str) -> str:
    lines = text.splitlines()
    try:
        start = lines.index(heading) + 1
    except ValueError as exc:
        raise ValueError(f"missing section: {heading}") from exc
    section: list[str] = []
    for line in lines[start:]:
        if line.startswith("## ") and section:
            break
        section.append(line)
    return "\n".join(section).strip()


def _section_text(text: str, heading: str) -> str:
    section = _section_raw(text, heading)
    return "\n".join(line for line in section.splitlines() if line.strip()).strip()


def _bullets(text: str, heading: str) -> list[str]:
    section = _section_raw(text, heading)
    return [line[2:].strip() for line in section.splitlines() if line.startswith("- ") and line[2:].strip()]


def _line_value(text: str, prefix: str) -> str:
    for line in text.splitlines():
        if line.startswith(prefix):
            return line[len(prefix) :].strip()
    return ""


def _split_list(value: str) -> list[str]:
    return [item.strip() for item in re.split(r",|;", value) if item.strip()]


def _session_id(date: str) -> str:
    return "real-accountant-session-" + re.sub(r"[^0-9A-Za-z]+", "-", date).strip("-")


def _relative_to_root(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Capture public-safe actual accountant notes into queue artifacts.")
    parser.add_argument("--notes", type=Path, default=DEFAULT_NOTES)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()

    paths = capture_actual_notes(args.notes, args.out, root=args.root)
    print(json.dumps({key: path.as_posix() for key, path in paths.items()}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
