from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs import store
from kifrs.user_notes import audit_user_notes, parse_user_note, parse_user_note_v2


def load_legacy_notes():
    with store._conn() as conn:
        rows = conn.execute(
            "SELECT id, standard, no, note, created_at FROM user_note ORDER BY id"
        ).fetchall()
    return [
        parse_user_note(
            row["standard"], row["no"], row["note"], row["created_at"],
            note_id=row["id"], legacy_id=row["id"],
        )
        for row in rows
    ]


def load_v2_notes():
    with store._conn() as conn:
        rows = conn.execute(
            """
            SELECT id, legacy_id, standard, no, type, trigger, expansion, source, rationale,
                   active, confidence, created_at, migrated_at
            FROM user_note_v2
            WHERE active=1
            ORDER BY id
            """
        ).fetchall()
    return [parse_user_note_v2(row) for row in rows]


def load_notes(source: str):
    if source == "legacy":
        return load_legacy_notes()
    if source == "v2":
        return load_v2_notes()
    v2_notes = load_v2_notes()
    return v2_notes if v2_notes else load_legacy_notes()


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit typed user_note rows.")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--source", choices=["auto", "legacy", "v2"], default="auto")
    args = parser.parse_args()

    notes = load_notes(args.source)
    result = audit_user_notes(
        notes,
        paragraph_exists=lambda standard, no: store.get_paragraph(standard, no) is not None,
    )
    result["source"] = args.source
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print(f"user_note source: {args.source}")
    print(f"user_note rows: {result['total']}")
    print(f"ok: {result['ok']}")
    for key in ("missing_required", "invalid_type", "dead_anchor", "conflicting_trigger"):
        print(f"{key}: {len(result[key])}")
    if result["duplicate_trigger"]:
        print(f"duplicate_trigger: {len(result['duplicate_trigger'])} (informational)")


if __name__ == "__main__":
    main()
