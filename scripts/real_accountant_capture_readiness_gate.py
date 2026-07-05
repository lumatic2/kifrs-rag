from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.real_accountant_capture import capture_actual_notes  # noqa: E402
from scripts.real_accountant_close_check import check_close_gate  # noqa: E402
from scripts.real_accountant_manifest_build import build_actual_manifest  # noqa: E402
from scripts.real_accountant_notes_check import check_actual_notes  # noqa: E402
from scripts.real_accountant_outreach_update import upsert_outreach  # noqa: E402
from scripts.real_accountant_session_check import check_session_manifest  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "real-accountant-session" / "2026-07-05-rs3-capture-readiness-gate.md"
DEFAULT_LEDGER = ROOT / "docs" / "reports" / "real-accountant-session" / "outreach-log.sample.jsonl"


def check_capture_readiness_gate() -> dict[str, Any]:
    errors: list[str] = []
    simulation = _simulate_capture_to_close()
    if simulation["ok"] is not True:
        errors.extend(f"capture_simulation: {error}" for error in simulation["errors"])

    return {
        "ok": not errors,
        "errors": errors,
        "gate_id": "rs3-capture-readiness-gate",
        "simulation": simulation,
        "boundary": [
            "This gate uses synthetic public-safe notes in a temporary directory.",
            "It does not create actual-feedback-notes.md in the repo.",
            "It does not mark the real outreach ledger completed.",
            "It proves the RS3 capture and manifest path is ready once real public-safe notes exist.",
        ],
        "report_path": _display_path(REPORT_PATH),
        "next_leaf": "collect real public-safe accountant notes, run capture, build actual manifest, then close RS4",
    }


def render_report(result: dict[str, Any]) -> str:
    simulation = result["simulation"]
    lines = [
        "# RS3 Capture Readiness Gate",
        "",
        "> Scope: verify that public-safe accountant notes can become capture artifacts, feedback queue records, an actual-feedback session manifest, and close-gate evidence.",
        "",
        "## 한 줄 결론",
        "",
        "The RS3 pipeline is ready for real notes: a synthetic public-safe notes file passes the notes checker, produces capture artifacts and one queue record, builds an `actual_feedback` manifest, and passes close gate when paired with a completed copied outreach ledger.",
        "",
        "## Synthetic Capture Simulation",
        "",
        f"- ok: {simulation['ok']}",
        f"- notes ok: {simulation['notes_ok']}",
        f"- capture files: {simulation['capture_files']}",
        f"- queue records: {simulation['queue_records']}",
        f"- manifest mode: {simulation['manifest_mode']}",
        f"- close ready with completed copied ledger: {simulation['close_ready']}",
        f"- close errors: {simulation['close_errors']}",
        "",
        "## Boundary",
        "",
    ]
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
    result = check_capture_readiness_gate()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_report(result), encoding="utf-8")
    return result


def _simulate_capture_to_close() -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        notes = root / "actual-feedback-notes.md"
        out = root / "capture"
        manifest = root / "session_manifest.json"
        ledger = root / "outreach-log.sample.jsonl"
        notes.write_text(_synthetic_actual_notes(), encoding="utf-8")
        shutil.copyfile(DEFAULT_LEDGER, ledger)

        errors: list[str] = []
        notes_ok, notes_errors = check_actual_notes(notes)
        if not notes_ok:
            errors.extend(f"notes: {error}" for error in notes_errors)

        paths = capture_actual_notes(notes, out, root=root)
        capture_manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
        built_manifest = build_actual_manifest(
            root=root,
            out=manifest,
            notes=notes,
            capture_manifest=paths["manifest"],
            queue_jsonl=paths["queue_jsonl"],
            reviewer_role="CPA reviewer",
            reviewer_service_line="F-ACC",
            reviewer_experience_context="reviewed accounting advisory workpapers",
        )
        session_ok, session_errors, session_mode = check_session_manifest(manifest, root=root)
        if not session_ok:
            errors.extend(f"session_manifest: {error}" for error in session_errors)

        upsert_outreach(
            ledger,
            reviewer_alias="reviewer-001",
            status="completed",
            channel="manual",
            contacted_at="2026-07-05",
            follow_up_by="2026-07-08",
            notes="synthetic completed session for readiness gate",
        )
        close_ok, close_errors, close_evidence = check_close_gate(
            root=root,
            manifest_path=manifest,
            outreach_ledger=ledger,
            run_quality=False,
        )
        if not close_ok:
            errors.extend(f"close_gate: {error}" for error in close_errors)

        return {
            "ok": not errors,
            "errors": errors,
            "notes_ok": notes_ok,
            "capture_files": {key: path.relative_to(root).as_posix() for key, path in paths.items()},
            "queue_records": capture_manifest["queue_records"],
            "capture_manifest_actual": capture_manifest["actual_feedback_evidence"],
            "manifest_mode": session_mode,
            "manifest_queue_records": built_manifest["queue_records"],
            "close_ready": close_ok,
            "close_errors": close_errors,
            "close_evidence": close_evidence,
        }


def _synthetic_actual_notes() -> str:
    return """# Real Accountant Session Evidence

## Session Metadata

- Date: 2026-07-05
- Reviewer role: CPA reviewer
- Reviewer service-line: F-ACC
- Reviewer experience context: reviewed accounting advisory workpapers
- Session mode: async review
- Actual feedback evidence: true

## Scores

- Workflow fit (1-5): 4
- Evidence boundary clarity (1-5): 5
- Review pack usefulness (1-5): 4
- Human-review boundary clarity (1-5): 5
- Real-case PoC willingness (1-5): 3

## Top Positive

The review pack order is understandable and makes the human review boundary visible.

## Top Risk

Evidence requests need sharper wording before the package can be used with real workpapers.

## Missing Inputs

- approval memo existence

## Review Question Additions

- Ask whether approval memo evidence exists before classifying the review pack as complete.

## Safe Correction Candidates

### Candidate 1

- Case id: anon-lease-poc-001
- Issue: Reviewer question should mention approval memo evidence
- Severity: medium
- Suggested fix: Add approval memo evidence to the required human-review questions.
- Missing evidence: approval memo existence
- Disposition: eval_seed_candidate
- Affected outputs: human_review_questions, review_pack

## Boundary Confirmation

- [x] No raw contract copied
- [x] No customer/client/company identifier copied
- [x] No private filing body copied
- [x] No K-IFRS source text copied
- [x] Notes are safe to convert into queue candidates
"""


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Check RS3 capture readiness using synthetic public-safe notes.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = write_report() if args.write else check_capture_readiness_gate()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"simulation: {result['simulation']}")
        print(f"next_leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
