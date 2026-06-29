"""Typed helpers for local user_note operations.

The SQLite table intentionally stores a compact string so it can stay backward
compatible with earlier Phase 4 seeds. This module provides the typed layer used
by runtime lookup, audits, and smoke tests.
"""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any, Callable, Iterable


NOTE_TYPES = {
    "term_bridge",
    "retriever_policy",
    "exam_convention",
    "interpretation_note",
}


@dataclass(frozen=True)
class ParsedUserNote:
    id: int | None
    legacy_id: int | None
    standard: str
    no: str
    type: str | None
    trigger: str | None
    expansion: str | None
    source: str | None
    rationale: str | None
    active: int = 1
    confidence: float = 1.0
    created_at: str | None = None
    migrated_at: str | None = None
    raw: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def note_field(note: str, key: str) -> str | None:
    """Extract one structured field from the semicolon-delimited note string."""
    next_keys = {
        "type": "trigger",
        "trigger": "expansion",
        "expansion": "source",
        "source": "rationale",
    }
    next_key = next_keys.get(key)
    if next_key:
        pattern = rf"(?:^|;\s*){re.escape(key)}=(.*?);\s*{re.escape(next_key)}="
    else:
        pattern = rf"(?:^|;\s*){re.escape(key)}=(.*)$"
    m = re.search(pattern, note)
    return m.group(1).strip() if m else None


def parse_user_note(
    standard: str,
    no: str,
    note: str,
    created_at: str | None = None,
    *,
    note_id: int | None = None,
    legacy_id: int | None = None,
) -> ParsedUserNote:
    return ParsedUserNote(
        id=note_id,
        legacy_id=legacy_id,
        standard=standard,
        no=no,
        type=note_field(note, "type"),
        trigger=note_field(note, "trigger"),
        expansion=note_field(note, "expansion"),
        source=note_field(note, "source"),
        rationale=note_field(note, "rationale"),
        created_at=created_at,
        raw=note,
    )


def parse_user_note_v2(row: Any) -> ParsedUserNote:
    """Build a typed note from a `user_note_v2` row-like object."""
    return ParsedUserNote(
        id=row["id"] if "id" in row.keys() else None,
        legacy_id=row["legacy_id"] if "legacy_id" in row.keys() else None,
        standard=row["standard"],
        no=row["no"],
        type=row["type"],
        trigger=row["trigger"],
        expansion=row["expansion"],
        source=row["source"],
        rationale=row["rationale"],
        active=row["active"] if "active" in row.keys() else 1,
        confidence=row["confidence"] if "confidence" in row.keys() else 1.0,
        created_at=row["created_at"] if "created_at" in row.keys() else None,
        migrated_at=row["migrated_at"] if "migrated_at" in row.keys() else None,
        raw=format_user_note(
            row["type"], row["trigger"], row["expansion"], row["source"], row["rationale"]
        ),
    )


def format_user_note(
    note_type: str,
    trigger: str,
    expansion: str,
    source: str | None,
    rationale: str | None,
) -> str:
    """Serialize a typed note into the legacy compact string format."""
    return (
        f"type={note_type}; trigger={trigger}; expansion={expansion}; "
        f"source={source or ''}; rationale={rationale or ''}"
    )


def audit_user_notes(
    notes: Iterable[ParsedUserNote],
    paragraph_exists: Callable[[str, str], bool],
) -> dict[str, Any]:
    """Audit note structure, anchor presence, and duplicate/conflicting triggers."""
    parsed = list(notes)
    missing_required: list[dict[str, Any]] = []
    invalid_type: list[dict[str, Any]] = []
    dead_anchor: list[dict[str, Any]] = []
    duplicate_trigger: list[dict[str, Any]] = []
    conflicting_trigger: list[dict[str, Any]] = []

    by_trigger: dict[tuple[str | None, str | None], list[ParsedUserNote]] = {}
    for note in parsed:
        missing = [
            key for key, value in {
                "type": note.type,
                "trigger": note.trigger,
                "expansion": note.expansion,
                "source": note.source,
                "rationale": note.rationale,
            }.items()
            if not value
        ]
        if missing:
            missing_required.append({**note.to_dict(), "missing": missing})
        if note.type and note.type not in NOTE_TYPES:
            invalid_type.append(note.to_dict())
        if not paragraph_exists(note.standard, note.no):
            dead_anchor.append(note.to_dict())
        by_trigger.setdefault((note.type, note.trigger), []).append(note)

    for (note_type, trigger), group in by_trigger.items():
        if not trigger or len(group) <= 1:
            continue
        expansions = {g.expansion for g in group}
        payload = {
            "type": note_type,
            "trigger": trigger,
            "anchors": [(g.standard, g.no) for g in group],
            "expansions": sorted(x for x in expansions if x),
        }
        duplicate_trigger.append(payload)
        if len(expansions) > 1:
            conflicting_trigger.append(payload)

    return {
        "total": len(parsed),
        "ok": not (missing_required or invalid_type or dead_anchor or conflicting_trigger),
        "missing_required": missing_required,
        "invalid_type": invalid_type,
        "dead_anchor": dead_anchor,
        "duplicate_trigger": duplicate_trigger,
        "conflicting_trigger": conflicting_trigger,
    }
