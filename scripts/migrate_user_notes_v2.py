from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs import store
from kifrs.user_notes import NOTE_TYPES, parse_user_note


def ensure_schema() -> None:
    with store._conn() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS user_note_v2 (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            legacy_id   INTEGER,
            standard    TEXT NOT NULL,
            no          TEXT NOT NULL,
            type        TEXT NOT NULL,
            trigger     TEXT NOT NULL,
            expansion   TEXT NOT NULL,
            source      TEXT,
            rationale   TEXT,
            active      INTEGER NOT NULL DEFAULT 1,
            confidence  REAL NOT NULL DEFAULT 1.0,
            created_at  TEXT,
            migrated_at TEXT,
            UNIQUE(legacy_id),
            FOREIGN KEY (legacy_id) REFERENCES user_note(id)
        );
        """)


def planned_rows() -> list[dict]:
    ensure_schema()
    with store._conn() as conn:
        rows = conn.execute(
            """
            SELECT id, standard, no, note, created_at
            FROM user_note
            WHERE id NOT IN (
                SELECT legacy_id FROM user_note_v2 WHERE legacy_id IS NOT NULL
            )
            ORDER BY id
            """
        ).fetchall()
    planned = []
    for row in rows:
        parsed = parse_user_note(row["standard"], row["no"], row["note"], row["created_at"])
        missing = [
            field for field in ("type", "trigger", "expansion")
            if not getattr(parsed, field)
        ]
        if missing or parsed.type not in NOTE_TYPES:
            planned.append({
                "legacy_id": row["id"],
                "status": "skipped",
                "reason": f"missing/invalid fields: {missing or parsed.type}",
            })
            continue
        planned.append({
            "legacy_id": row["id"],
            "status": "ready",
            "standard": parsed.standard,
            "no": parsed.no,
            "type": parsed.type,
            "trigger": parsed.trigger,
            "expansion": parsed.expansion,
            "source": parsed.source,
            "rationale": parsed.rationale,
            "created_at": parsed.created_at,
        })
    return planned


def apply_migration(rows: list[dict]) -> int:
    ready = [row for row in rows if row["status"] == "ready"]
    if not ready:
        return 0
    now = datetime.now().isoformat(timespec="seconds")
    with store._conn() as conn:
        conn.executemany(
            """
            INSERT OR IGNORE INTO user_note_v2
            (legacy_id, standard, no, type, trigger, expansion, source, rationale, active, confidence, created_at, migrated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, 1.0, ?, ?)
            """,
            [
                (
                    row["legacy_id"], row["standard"], row["no"], row["type"],
                    row["trigger"], row["expansion"], row["source"], row["rationale"],
                    row["created_at"], now,
                )
                for row in ready
            ],
        )
        return conn.total_changes


def main() -> None:
    parser = argparse.ArgumentParser(description="Backfill typed user_note_v2 rows from legacy user_note.")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--format", choices=["json", "text"], default="json")
    args = parser.parse_args()

    rows = planned_rows()
    inserted = apply_migration(rows) if args.apply else 0
    payload = {
        "apply": args.apply,
        "planned": len(rows),
        "ready": sum(1 for row in rows if row["status"] == "ready"),
        "skipped": [row for row in rows if row["status"] == "skipped"],
        "inserted": inserted,
    }
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"apply: {payload['apply']}")
        print(f"planned: {payload['planned']}")
        print(f"ready: {payload['ready']}")
        print(f"inserted: {payload['inserted']}")
        print(f"skipped: {len(payload['skipped'])}")


if __name__ == "__main__":
    main()
