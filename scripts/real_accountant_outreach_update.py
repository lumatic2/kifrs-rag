from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from scripts.real_accountant_outreach_check import ALLOWED_STATUS, check_outreach, load_outreach
except ModuleNotFoundError:
    from real_accountant_outreach_check import ALLOWED_STATUS, check_outreach, load_outreach


INVITE_SENT_STATUSES = {"sent", "responded", "scheduled", "completed"}


def upsert_outreach(
    path: Path,
    *,
    reviewer_alias: str,
    status: str,
    channel: str,
    contacted_at: str,
    follow_up_by: str,
    notes: str = "",
) -> dict[str, Any]:
    if status not in ALLOWED_STATUS:
        raise ValueError(f"unsupported status: {status}")
    if not reviewer_alias.startswith("reviewer-"):
        raise ValueError("reviewer_alias must be a public-safe alias like reviewer-001")

    rows = [{key: value for key, value in row.items() if key != "_line_no"} for row in load_outreach(path)] if path.exists() else []
    invite_sent = status in INVITE_SENT_STATUSES
    replacement = {
        "reviewer_alias": reviewer_alias,
        "status": status,
        "invite_sent": invite_sent,
        "channel": channel,
        "contacted_at": contacted_at,
        "follow_up_by": follow_up_by,
    }
    if notes:
        replacement["notes"] = notes

    updated = False
    for index, row in enumerate(rows):
        if row.get("reviewer_alias") == reviewer_alias:
            rows[index] = replacement
            updated = True
            break
    if not updated:
        rows.append(replacement)

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows) + "\n",
        encoding="utf-8",
    )
    ok, errors, _counts = check_outreach(path)
    if not ok:
        raise ValueError("; ".join(errors))
    return replacement


def main() -> int:
    parser = argparse.ArgumentParser(description="Append/update a public-safe real accountant outreach ledger row.")
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--reviewer-alias", required=True)
    parser.add_argument("--status", required=True, choices=sorted(ALLOWED_STATUS))
    parser.add_argument("--channel", default="manual")
    parser.add_argument("--contacted-at", required=True)
    parser.add_argument("--follow-up-by", required=True)
    parser.add_argument("--notes", default="")
    args = parser.parse_args()

    row = upsert_outreach(
        args.ledger,
        reviewer_alias=args.reviewer_alias,
        status=args.status,
        channel=args.channel,
        contacted_at=args.contacted_at,
        follow_up_by=args.follow_up_by,
        notes=args.notes,
    )
    print(json.dumps(row, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
