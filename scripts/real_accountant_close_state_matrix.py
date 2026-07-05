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
from scripts.real_accountant_capture_readiness_gate import _synthetic_actual_notes  # noqa: E402
from scripts.real_accountant_close_check import check_close_gate  # noqa: E402
from scripts.real_accountant_manifest_build import build_actual_manifest  # noqa: E402
from scripts.real_accountant_outreach_update import upsert_outreach  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "real-accountant-session" / "2026-07-05-close-state-matrix.md"
READY_MANIFEST = ROOT / "docs" / "reports" / "real-accountant-session" / "session_manifest.json"
DEFAULT_LEDGER = ROOT / "docs" / "reports" / "real-accountant-session" / "outreach-log.sample.jsonl"
OUTREACH_STATES = ("not_sent", "sent", "scheduled", "completed")


def build_close_state_matrix() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    errors: list[str] = []

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        ready_manifest = root / "ready-session-manifest.json"
        actual_manifest = root / "actual-session-manifest.json"
        shutil.copyfile(READY_MANIFEST, ready_manifest)
        _build_actual_feedback_inputs(root, actual_manifest)

        for manifest_mode, manifest_path in (
            ("ready_to_schedule", ready_manifest),
            ("actual_feedback", actual_manifest),
        ):
            for outreach_state in OUTREACH_STATES:
                ledger = root / f"outreach-{manifest_mode}-{outreach_state}.jsonl"
                shutil.copyfile(DEFAULT_LEDGER, ledger)
                if outreach_state != "not_sent":
                    upsert_outreach(
                        ledger,
                        reviewer_alias="reviewer-001",
                        status=outreach_state,
                        channel="manual",
                        contacted_at="2026-07-05",
                        follow_up_by="2026-07-08",
                        notes=f"matrix {outreach_state}",
                    )
                close_root = ROOT if manifest_mode == "ready_to_schedule" else root
                close_ok, close_errors, close_evidence = check_close_gate(
                    root=close_root,
                    manifest_path=manifest_path,
                    outreach_ledger=ledger,
                    run_quality=False,
                )
                expected_close = manifest_mode == "actual_feedback" and outreach_state == "completed"
                if close_ok != expected_close:
                    errors.append(
                        f"unexpected close result for manifest={manifest_mode}, outreach={outreach_state}: "
                        f"expected {expected_close}, got {close_ok}"
                    )
                rows.append(
                    {
                        "manifest_mode": manifest_mode,
                        "outreach_state": outreach_state,
                        "expected_close": expected_close,
                        "close_ready": close_ok,
                        "primary_blockers": _primary_blockers(close_errors),
                        "evidence": close_evidence,
                    }
                )

    return {
        "ok": not errors,
        "errors": errors,
        "gate_id": "rs4-close-state-matrix",
        "rows": rows,
        "summary": {
            "total_rows": len(rows),
            "passing_close_rows": sum(1 for row in rows if row["close_ready"]),
            "blocked_rows": sum(1 for row in rows if not row["close_ready"]),
            "only_actual_feedback_completed_closes": all(
                row["close_ready"] == (row["manifest_mode"] == "actual_feedback" and row["outreach_state"] == "completed")
                for row in rows
            ),
        },
        "boundary": [
            "This matrix uses copied ledgers and temporary synthetic actual-feedback inputs only.",
            "It does not update the real session manifest, outreach ledger, notes, capture manifest, or queue JSONL.",
            "Close is expected only when actual-feedback manifest evidence and completed outreach are both present.",
        ],
        "report_path": _display_path(REPORT_PATH),
        "next_leaf": "operator sends invite; after real notes exist, use the close matrix expectation to verify RS4 close conditions",
    }


def render_report(matrix: dict[str, Any]) -> str:
    lines = [
        "# RS4 Close State Matrix",
        "",
        "> Scope: prove which real-accountant-session state combinations must remain blocked and which combination can close.",
        "",
        "## 한 줄 결론",
        "",
        "The close gate behaves correctly across the state matrix: every pre-actual or pre-completed combination stays blocked, and only `actual_feedback` plus `completed` outreach is close-ready.",
        "",
        "## Summary",
        "",
        f"- ok: {matrix['ok']}",
        f"- total rows: {matrix['summary']['total_rows']}",
        f"- blocked rows: {matrix['summary']['blocked_rows']}",
        f"- passing close rows: {matrix['summary']['passing_close_rows']}",
        f"- only actual_feedback+completed closes: {matrix['summary']['only_actual_feedback_completed_closes']}",
        "",
        "## Matrix",
        "",
        "| Manifest | Outreach | Expected close | Actual close | Primary blockers |",
        "|---|---|---:|---:|---|",
    ]
    for row in matrix["rows"]:
        blockers = "; ".join(row["primary_blockers"]) if row["primary_blockers"] else "none"
        lines.append(
            f"| {row['manifest_mode']} | {row['outreach_state']} | {row['expected_close']} | {row['close_ready']} | {blockers} |"
        )
    lines.extend(["", "## Boundary", ""])
    lines.extend(f"- {item}" for item in matrix["boundary"])
    lines.extend(
        [
            "",
            "## Next Leaf",
            "",
            str(matrix["next_leaf"]),
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps(matrix, ensure_ascii=False, indent=2, default=str),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report() -> dict[str, Any]:
    matrix = build_close_state_matrix()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_report(matrix), encoding="utf-8")
    return matrix


def _build_actual_feedback_inputs(root: Path, manifest: Path) -> None:
    notes = root / "actual-feedback-notes.md"
    capture_out = root / "capture"
    notes.write_text(_synthetic_actual_notes(), encoding="utf-8")
    paths = capture_actual_notes(notes, capture_out, root=root)
    build_actual_manifest(
        root=root,
        out=manifest,
        notes=notes,
        capture_manifest=paths["manifest"],
        queue_jsonl=paths["queue_jsonl"],
        reviewer_role="CPA reviewer",
        reviewer_service_line="F-ACC",
        reviewer_experience_context="reviewed accounting advisory workpapers",
    )


def _primary_blockers(errors: list[str]) -> list[str]:
    blockers: list[str] = []
    for error in errors:
        if error.startswith("session_manifest: mode must be actual_feedback"):
            blockers.append("manifest_not_actual_feedback")
        elif error.startswith("session_manifest: missing notes_file"):
            blockers.append("missing_notes_file")
        elif error.startswith("session_manifest: missing queue_jsonl"):
            blockers.append("missing_queue_jsonl")
        elif error.startswith("outreach: at least one completed"):
            blockers.append("no_completed_outreach")
        elif error.startswith("notes:"):
            blockers.append("notes_not_public_safe")
        elif error.startswith("queue_jsonl:"):
            blockers.append("queue_not_ready")
        else:
            blockers.append(error)
    return list(dict.fromkeys(blockers))


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the real-accountant-session close state matrix.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    matrix = write_report() if args.write else build_close_state_matrix()
    if args.format == "json":
        print(json.dumps(matrix, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(matrix), end="")
    else:
        print(f"ok: {matrix['ok']}")
        print(f"summary: {matrix['summary']}")
        print(f"next_leaf: {matrix['next_leaf']}")
        for error in matrix["errors"]:
            print(f"- {error}")

    if not matrix["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
