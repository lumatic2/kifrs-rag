from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from kifrs.feedback.queue import load_queue
    from scripts.quality_preflight import run_preflight
    from scripts.real_accountant_notes_check import check_actual_notes
    from scripts.real_accountant_outreach_check import check_outreach
    from scripts.real_accountant_session_check import check_session_manifest
except ModuleNotFoundError:
    import sys

    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from kifrs.feedback.queue import load_queue
    try:
        from scripts.quality_preflight import run_preflight
        from scripts.real_accountant_notes_check import check_actual_notes
        from scripts.real_accountant_outreach_check import check_outreach
        from scripts.real_accountant_session_check import check_session_manifest
    except ModuleNotFoundError:
        from quality_preflight import run_preflight
        from real_accountant_notes_check import check_actual_notes
        from real_accountant_outreach_check import check_outreach
        from real_accountant_session_check import check_session_manifest


def check_close_gate(
    *,
    root: Path,
    manifest_path: Path,
    outreach_ledger: Path,
    run_quality: bool = False,
    quality_timeout: int = 240,
) -> tuple[bool, list[str], dict[str, Any]]:
    errors: list[str] = []
    evidence: dict[str, Any] = {}

    ok, session_errors, mode = check_session_manifest(manifest_path, root=root)
    evidence["session_mode"] = mode
    if not ok:
        errors.extend(f"session_manifest: {error}" for error in session_errors)
    if mode != "actual_feedback":
        errors.append(f"session_manifest: mode must be actual_feedback, got {mode}")

    manifest = _read_json(manifest_path, errors, "session_manifest")
    notes_file = manifest.get("notes_file") if manifest else None
    if notes_file:
        notes_ok, notes_errors = check_actual_notes(root / str(notes_file))
        evidence["notes_public_safe"] = notes_ok
        if not notes_ok:
            errors.extend(f"notes: {error}" for error in notes_errors)
    else:
        errors.append("session_manifest: missing notes_file")

    queue_jsonl = manifest.get("queue_jsonl") if manifest else None
    if queue_jsonl:
        try:
            queue_records = load_queue(root / str(queue_jsonl))
            evidence["queue_records"] = len(queue_records)
            if not queue_records:
                errors.append("queue_jsonl: at least one queue record is required")
        except Exception as exc:  # noqa: BLE001 - CLI should surface parser failures directly.
            errors.append(f"queue_jsonl: {exc}")
    else:
        errors.append("session_manifest: missing queue_jsonl")

    outreach_ok, outreach_errors, outreach_counts = check_outreach(outreach_ledger)
    evidence["outreach_counts"] = outreach_counts
    if not outreach_ok:
        errors.extend(f"outreach: {error}" for error in outreach_errors)
    if outreach_counts.get("completed", 0) < 1:
        errors.append("outreach: at least one completed reviewer session is required")

    if run_quality:
        preflight = run_preflight(timeout=quality_timeout)
        evidence["quality_preflight"] = {
            "ok": preflight["ok"],
            "public_safe": preflight["public_safe"],
            "protected_assets_required": preflight["protected_assets_required"],
        }
        if not preflight["ok"]:
            errors.append("quality_preflight: failed")
        if not preflight["public_safe"] or preflight["protected_assets_required"]:
            errors.append("quality_preflight: public-safe boundary failed")
    else:
        evidence["quality_preflight"] = "not_run"

    return not errors, errors, evidence


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


def main() -> int:
    parser = argparse.ArgumentParser(description="Check whether the real accountant session horizon can close.")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--outreach-ledger", type=Path, required=True)
    parser.add_argument("--run-quality-preflight", action="store_true")
    parser.add_argument("--quality-timeout", type=int, default=240)
    args = parser.parse_args()

    ok, errors, evidence = check_close_gate(
        root=args.root,
        manifest_path=args.manifest,
        outreach_ledger=args.outreach_ledger,
        run_quality=args.run_quality_preflight,
        quality_timeout=args.quality_timeout,
    )
    print(f"ok: {ok}")
    print(f"evidence: {json.dumps(evidence, ensure_ascii=False, sort_keys=True)}")
    for error in errors:
        print(f"- {error}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
