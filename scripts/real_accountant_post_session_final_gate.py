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
from scripts.real_accountant_notes_check import check_actual_notes  # noqa: E402
from scripts.real_accountant_notes_quality_gate import DEFAULT_NOTES, check_notes_quality  # noqa: E402
from scripts.real_accountant_outreach_update import upsert_outreach  # noqa: E402
from scripts.real_accountant_session_check import check_session_manifest  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "real-accountant-session" / "2026-07-05-post-session-final-gate.md"
DEFAULT_LEDGER = ROOT / "docs" / "reports" / "real-accountant-session" / "outreach-log.sample.jsonl"


def check_post_session_final_gate(*, notes: Path = DEFAULT_NOTES) -> dict[str, Any]:
    mode = "repo_actual_notes" if notes.exists() else "synthetic_readiness"
    result = _simulate_or_check_post_session(notes=notes, use_synthetic=not notes.exists())
    return {
        "ok": result["ok"],
        "errors": result["errors"],
        "gate_id": "rs3-rs4-post-session-final-gate",
        "mode": mode,
        "notes_path": _display_path(notes),
        "result": result,
        "boundary": [
            "This gate does not create or edit repo actual-feedback-notes.md when it is absent.",
            "Synthetic mode writes only to a temporary directory.",
            "Repo actual-notes mode still writes derived capture artifacts only when explicitly pointed at an existing notes file.",
            "The real outreach ledger is not marked completed by this gate.",
        ],
        "report_path": _display_path(REPORT_PATH),
        "next_leaf": "after actual session, run this gate on actual notes, then update real outreach ledger to completed and run close gate",
    }


def render_report(result: dict[str, Any]) -> str:
    flow = result["result"]
    lines = [
        "# RS3/RS4 Post-Session Final Gate",
        "",
        "> Scope: verify the full post-session path from public-safe notes to capture artifacts, actual session manifest, completed copied outreach, and close gate.",
        "",
        "## 한 줄 결론",
        "",
        "The post-session path is ready: notes must pass safety and quality gates, capture must produce queue records, manifest build must produce `actual_feedback`, and close gate must pass only with completed outreach.",
        "",
        "## Current Result",
        "",
        f"- ok: {result['ok']}",
        f"- mode: {result['mode']}",
        f"- notes path: `{result['notes_path']}`",
        f"- notes safety ok: {flow['notes_safety_ok']}",
        f"- notes quality ok: {flow['notes_quality_ok']}",
        f"- queue records: {flow['queue_records']}",
        f"- manifest mode: {flow['manifest_mode']}",
        f"- close ready with completed copied ledger: {flow['close_ready']}",
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
    result = check_post_session_final_gate()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_report(result), encoding="utf-8")
    return result


def _simulate_or_check_post_session(*, notes: Path, use_synthetic: bool) -> dict[str, Any]:
    errors: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        working_notes = root / "actual-feedback-notes.md"
        if use_synthetic:
            working_notes.write_text(_synthetic_actual_notes(), encoding="utf-8")
        else:
            shutil.copyfile(notes, working_notes)

        capture_out = root / "capture"
        actual_manifest = root / "session_manifest.json"
        ledger = root / "outreach-log.sample.jsonl"
        shutil.copyfile(DEFAULT_LEDGER, ledger)

        notes_safety_ok, notes_safety_errors = check_actual_notes(working_notes)
        if not notes_safety_ok:
            errors.extend(f"notes_safety: {error}" for error in notes_safety_errors)

        notes_quality_ok, notes_quality_errors, notes_quality_evidence = check_notes_quality(working_notes)
        if not notes_quality_ok:
            errors.extend(f"notes_quality: {error}" for error in notes_quality_errors)

        capture_paths: dict[str, Path] = {}
        queue_records = 0
        manifest_mode = "not_built"
        close_ready = False
        close_errors: list[str] = []
        close_evidence: dict[str, Any] = {}
        if notes_safety_ok and notes_quality_ok:
            capture_paths = capture_actual_notes(working_notes, capture_out, root=root)
            capture_manifest = json.loads(capture_paths["manifest"].read_text(encoding="utf-8"))
            queue_records = int(capture_manifest["queue_records"])
            built_manifest = build_actual_manifest(
                root=root,
                out=actual_manifest,
                notes=working_notes,
                capture_manifest=capture_paths["manifest"],
                queue_jsonl=capture_paths["queue_jsonl"],
                reviewer_role="CPA reviewer",
                reviewer_service_line="F-ACC",
                reviewer_experience_context="reviewed accounting advisory workpapers",
            )
            manifest_ok, manifest_errors, manifest_mode = check_session_manifest(actual_manifest, root=root)
            if not manifest_ok:
                errors.extend(f"session_manifest: {error}" for error in manifest_errors)
            if built_manifest["queue_records"] != queue_records:
                errors.append("manifest queue record count does not match capture manifest")
            upsert_outreach(
                ledger,
                reviewer_alias="reviewer-001",
                status="completed",
                channel="manual",
                contacted_at="2026-07-05",
                follow_up_by="2026-07-08",
                notes="post-session final gate completed copied ledger",
            )
            close_ready, close_errors, close_evidence = check_close_gate(
                root=root,
                manifest_path=actual_manifest,
                outreach_ledger=ledger,
                run_quality=False,
            )
            if not close_ready:
                errors.extend(f"close_gate: {error}" for error in close_errors)

        return {
            "ok": not errors,
            "errors": errors,
            "notes_safety_ok": notes_safety_ok,
            "notes_quality_ok": notes_quality_ok,
            "notes_quality_evidence": notes_quality_evidence,
            "capture_files": {key: path.relative_to(root).as_posix() for key, path in capture_paths.items()},
            "queue_records": queue_records,
            "manifest_mode": manifest_mode,
            "close_ready": close_ready,
            "close_errors": close_errors,
            "close_evidence": close_evidence,
        }


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run post-session final gate for real accountant session evidence.")
    parser.add_argument("--notes", type=Path, default=DEFAULT_NOTES)
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = check_post_session_final_gate(notes=args.notes)
    if args.write:
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.write_text(render_report(result), encoding="utf-8")
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"mode: {result['mode']}")
        print(f"result: {result['result']}")
        print(f"next_leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
