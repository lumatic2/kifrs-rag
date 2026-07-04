from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from kifrs.feedback.queue import load_queue
    from scripts.real_accountant_notes_check import check_actual_notes
    from scripts.real_accountant_session_check import check_session_manifest
except ModuleNotFoundError:
    import sys

    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from kifrs.feedback.queue import load_queue
    from scripts.real_accountant_notes_check import check_actual_notes
    from scripts.real_accountant_session_check import check_session_manifest


def build_actual_manifest(
    *,
    root: Path,
    out: Path,
    notes: Path,
    capture_manifest: Path,
    queue_jsonl: Path,
    reviewer_role: str,
    reviewer_service_line: str,
    reviewer_experience_context: str,
    allow_empty_queue: bool = False,
) -> dict[str, Any]:
    errors: list[str] = []

    notes_ok, notes_errors = check_actual_notes(notes)
    if not notes_ok:
        errors.extend(f"notes: {error}" for error in notes_errors)

    capture = _read_json(capture_manifest, errors, "capture_manifest")
    if capture and capture.get("actual_feedback_evidence") is not True:
        errors.append("capture_manifest: actual_feedback_evidence must be true")

    if not queue_jsonl.exists():
        errors.append(f"queue_jsonl: missing file: {queue_jsonl}")
        queue_records = []
    else:
        try:
            queue_records = load_queue(queue_jsonl)
        except Exception as exc:  # noqa: BLE001 - CLI should surface parser failures directly.
            errors.append(f"queue_jsonl: {exc}")
            queue_records = []
        if not allow_empty_queue and not queue_records:
            errors.append("queue_jsonl: at least one queue record is required")

    reviewer_metadata = {
        "role": reviewer_role.strip(),
        "service_line": reviewer_service_line.strip(),
        "experience_context": reviewer_experience_context.strip(),
    }
    for key, value in reviewer_metadata.items():
        if not value:
            errors.append(f"reviewer_metadata.{key}: required")

    if errors:
        raise ValueError("; ".join(errors))

    manifest = {
        "version": 1,
        "name": "real-accountant-session",
        "status": "actual_feedback",
        "actual_feedback_evidence": True,
        "reviewer_metadata": reviewer_metadata,
        "notes_file": _relative_to_root(root, notes),
        "capture_manifest": _relative_to_root(root, capture_manifest),
        "queue_jsonl": _relative_to_root(root, queue_jsonl),
        "queue_records": len(queue_records),
        "public_safe_checks": {
            "notes": True,
            "capture_manifest_actual": True,
            "queue_jsonl_valid": True,
        },
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    ok, session_errors, mode = check_session_manifest(out, root=root)
    if not ok or mode != "actual_feedback":
        raise ValueError("; ".join(session_errors) or f"unexpected manifest mode: {mode}")
    return manifest


def _read_json(path: Path, errors: list[str], label: str) -> dict[str, Any]:
    if not path.exists():
        errors.append(f"{label}: missing file: {path}")
        return {}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{label}: invalid JSON: {exc}")
        return {}
    if not isinstance(raw, dict):
        errors.append(f"{label}: JSON object required")
        return {}
    return raw


def _relative_to_root(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build an actual-feedback real accountant session manifest.")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--notes", type=Path, required=True)
    parser.add_argument("--capture-manifest", type=Path, required=True)
    parser.add_argument("--queue-jsonl", type=Path, required=True)
    parser.add_argument("--reviewer-role", required=True)
    parser.add_argument("--reviewer-service-line", required=True)
    parser.add_argument("--reviewer-experience-context", required=True)
    parser.add_argument("--allow-empty-queue", action="store_true")
    args = parser.parse_args()

    manifest = build_actual_manifest(
        root=args.root,
        out=args.out,
        notes=args.notes,
        capture_manifest=args.capture_manifest,
        queue_jsonl=args.queue_jsonl,
        reviewer_role=args.reviewer_role,
        reviewer_service_line=args.reviewer_service_line,
        reviewer_experience_context=args.reviewer_experience_context,
        allow_empty_queue=args.allow_empty_queue,
    )
    print(json.dumps(manifest, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
