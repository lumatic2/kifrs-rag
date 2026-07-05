from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.real_accountant_capture import parse_actual_notes  # noqa: E402
from scripts.real_accountant_capture_readiness_gate import _synthetic_actual_notes  # noqa: E402
from scripts.real_accountant_notes_check import check_actual_notes  # noqa: E402
from scripts.real_accountant_notes_scaffold import render_notes_scaffold  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "real-accountant-session" / "2026-07-05-notes-quality-gate.md"
DEFAULT_NOTES = ROOT / "docs" / "reports" / "real-accountant-session" / "actual-feedback-notes.md"
REQUIRED_SCORE_KEYS = {
    "workflow_fit",
    "evidence_boundary_clarity",
    "review_pack_usefulness",
    "human_review_boundary",
    "real_case_poc_willingness",
}
ALLOWED_SEVERITIES = {"low", "medium", "high", "blocker"}
ALLOWED_DISPOSITIONS = {"eval_seed_candidate", "backlog_candidate", "no_action"}


def check_notes_quality(path: Path) -> tuple[bool, list[str], dict[str, Any]]:
    errors: list[str] = []
    safe_ok, safe_errors = check_actual_notes(path)
    if not safe_ok:
        errors.extend(f"safety: {error}" for error in safe_errors)
        return False, errors, {"safe_ok": False}

    try:
        notes = parse_actual_notes(path)
    except Exception as exc:  # noqa: BLE001 - gate should surface parse failures.
        return False, [f"parse: {exc}"], {"safe_ok": True}

    missing_scores = sorted(REQUIRED_SCORE_KEYS - set(notes.scores))
    if missing_scores:
        errors.append(f"missing scores: {', '.join(missing_scores)}")
    for key, score in notes.scores.items():
        if not isinstance(score, int) or score < 1 or score > 5:
            errors.append(f"score out of range: {key}={score}")

    if _word_count(notes.top_positive) < 6:
        errors.append("top_positive is too short to be actionable")
    if _word_count(notes.top_risk) < 6:
        errors.append("top_risk is too short to be actionable")
    if not notes.required_input_additions:
        errors.append("at least one missing input is required")
    if not notes.review_question_additions:
        errors.append("at least one review question addition is required")
    if not notes.corrections:
        errors.append("at least one safe correction candidate is required")

    for index, correction in enumerate(notes.corrections, start=1):
        if not correction.case_id.startswith("anon-"):
            errors.append(f"candidate {index}: case_id must be anonymized and start with anon-")
        if correction.severity not in ALLOWED_SEVERITIES:
            errors.append(f"candidate {index}: unsupported severity {correction.severity}")
        if correction.disposition not in ALLOWED_DISPOSITIONS:
            errors.append(f"candidate {index}: unsupported disposition {correction.disposition}")
        if _word_count(correction.issue) < 4:
            errors.append(f"candidate {index}: issue is too short")
        if _word_count(correction.suggested_fix) < 5:
            errors.append(f"candidate {index}: suggested fix is too short")
        if not correction.missing_evidence:
            errors.append(f"candidate {index}: missing evidence is required")
        if not correction.affected_outputs:
            errors.append(f"candidate {index}: affected outputs are required")

    evidence = {
        "safe_ok": safe_ok,
        "score_count": len(notes.scores),
        "scores": notes.scores,
        "top_positive_words": _word_count(notes.top_positive),
        "top_risk_words": _word_count(notes.top_risk),
        "missing_inputs": len(notes.required_input_additions),
        "review_question_additions": len(notes.review_question_additions),
        "correction_candidates": len(notes.corrections),
        "candidate_dispositions": [correction.disposition for correction in notes.corrections],
        "candidate_severities": [correction.severity for correction in notes.corrections],
    }
    return not errors, errors, evidence


def build_notes_quality_gate(*, notes: Path = DEFAULT_NOTES) -> dict[str, Any]:
    if notes.exists():
        ok, errors, evidence = check_notes_quality(notes)
        mode = "repo_actual_notes"
    else:
        ok, errors, evidence = _simulate_quality_gate()
        mode = "synthetic_readiness"

    return {
        "ok": ok,
        "errors": errors,
        "gate_id": "rs3-notes-quality-gate",
        "mode": mode,
        "notes_path": _display_path(notes),
        "evidence": evidence,
        "boundary": [
            "This gate does not create or edit actual-feedback-notes.md.",
            "If actual notes are absent, it validates the rubric against synthetic public-safe notes only.",
            "Actual notes must still pass this gate before capture and manifest build.",
        ],
        "report_path": _display_path(REPORT_PATH),
        "next_leaf": "after actual notes are written, run notes safety check, notes quality gate, capture, manifest build, and close gate",
    }


def render_report(result: dict[str, Any]) -> str:
    lines = [
        "# RS3 Notes Quality Gate",
        "",
        "> Scope: verify that actual accountant feedback notes are not only public-safe, but structured enough to drive capture, queue, and eval/backlog decisions.",
        "",
        "## 한 줄 결론",
        "",
        "The notes quality rubric is ready. It requires complete scores, actionable positive/risk summaries, at least one missing input, at least one review question addition, and at least one anonymized safe correction candidate.",
        "",
        "## Current Result",
        "",
        f"- ok: {result['ok']}",
        f"- mode: {result['mode']}",
        f"- notes path: `{result['notes_path']}`",
        f"- evidence: {result['evidence']}",
    ]
    if result["errors"]:
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in result["errors"])
    lines.extend(["", "## Boundary", ""])
    lines.extend(f"- {item}" for item in result["boundary"])
    lines.extend(
        [
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
    )
    return "\n".join(lines) + "\n"


def write_report() -> dict[str, Any]:
    result = build_notes_quality_gate()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_report(result), encoding="utf-8")
    return result


def _simulate_quality_gate() -> tuple[bool, list[str], dict[str, Any]]:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        good = root / "synthetic-good-notes.md"
        scaffold = root / "scaffold-notes.md"
        good.write_text(_synthetic_actual_notes(), encoding="utf-8")
        scaffold.write_text(
            render_notes_scaffold(
                date="2026-07-05",
                reviewer_role="CPA reviewer",
                reviewer_service_line="F-ACC",
                reviewer_experience_context="reviewed accounting advisory workpapers",
                session_mode="async review",
            ),
            encoding="utf-8",
        )
        good_ok, good_errors, good_evidence = check_notes_quality(good)
        scaffold_ok, scaffold_errors, _scaffold_evidence = check_notes_quality(scaffold)
        errors: list[str] = []
        if not good_ok:
            errors.extend(f"synthetic_good: {error}" for error in good_errors)
        if scaffold_ok:
            errors.append("scaffold notes unexpectedly passed quality gate")
        return (
            good_ok and not scaffold_ok and not errors,
            errors,
            {
                **good_evidence,
                "synthetic_good_ok": good_ok,
                "scaffold_rejected": not scaffold_ok,
                "scaffold_error_count": len(scaffold_errors),
            },
        )


def _word_count(text: str) -> int:
    return len([part for part in text.replace("\n", " ").split(" ") if part.strip()])


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Check actual accountant notes quality before capture.")
    parser.add_argument("--notes", type=Path, default=DEFAULT_NOTES)
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = write_report() if args.write and args.notes == DEFAULT_NOTES else build_notes_quality_gate(notes=args.notes)
    if args.write and args.notes != DEFAULT_NOTES:
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.write_text(render_report(result), encoding="utf-8")
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"mode: {result['mode']}")
        print(f"evidence: {result['evidence']}")
        print(f"next_leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
