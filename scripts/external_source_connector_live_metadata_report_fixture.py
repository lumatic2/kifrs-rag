from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.external_source_connector_live_metadata_close_gate import check_live_metadata_close_gate  # noqa: E402
from scripts.external_source_connector_live_metadata_decision_gate import ALLOWED_LIVE_METADATA_FIELDS  # noqa: E402
from scripts.external_source_connector_live_metadata_probe_scaffold import run_live_metadata_probe_scaffold  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-eslr1-external-source-connector-live-metadata-report-fixture.md"


def build_live_metadata_report_fixture() -> dict[str, Any]:
    close_gate = check_live_metadata_close_gate()
    scaffold = run_live_metadata_probe_scaffold(allow_network=False, checked_at="2026-07-05T13:00:00+09:00")
    errors: list[str] = []

    if close_gate["ok"] is not True:
        errors.extend(f"close_gate: {error}" for error in close_gate["errors"])
    if scaffold["ok"] is not True:
        errors.extend(f"probe_scaffold: {error}" for error in scaffold["errors"])
    if scaffold["record_count"] != 2:
        errors.append(f"probe_scaffold: expected 2 records, got {scaffold['record_count']}")
    if scaffold["allow_network"] is not False:
        errors.append("probe_scaffold: fixture must default to no network")

    fixture_rows = [_fixture_row(record) for record in scaffold["probe_records"]]
    for idx, record in enumerate(scaffold["probe_records"]):
        if set(record) != set(ALLOWED_LIVE_METADATA_FIELDS):
            errors.append(f"probe_records[{idx}]: record fields must equal allowed live metadata fields")
        if record.get("network_checked") is not False:
            errors.append(f"probe_records[{idx}]: network_checked must remain false in the fixture")
        if record.get("body_text_stored") is not False:
            errors.append(f"probe_records[{idx}]: body_text_stored must remain false")

    rendered_fixture = render_fixture_table(fixture_rows)
    if "copied excerpt" in rendered_fixture.lower():
        errors.append("fixture_markdown: copied excerpts must not appear")

    return {
        "ok": not errors,
        "errors": errors,
        "fixture_id": "eslr1-external-source-connector-live-metadata-report-fixture",
        "connector_id": "kasb-fss-interpretive-catalog",
        "public_safe_report_fixture_created": not errors,
        "network_checked": False,
        "record_count": len(fixture_rows),
        "body_text_stored": False,
        "body_cache_created": False,
        "chunks_created": False,
        "embeddings_created": False,
        "index_created": False,
        "answer_time_body_use_enabled": False,
        "close_gate": {
            "ok": close_gate["ok"],
            "report_path": close_gate["report_path"],
            "close_gate_id": close_gate["close_gate_id"],
        },
        "fixture_rows": fixture_rows,
        "report_path": str(REPORT_PATH.relative_to(ROOT)),
        "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or external source connector live-metadata report close gate",
    }


def render_fixture_table(rows: list[dict[str, Any]]) -> str:
    lines = [
        "| Item | Publisher | Locator | Status | Network | Body Stored |",
        "|---|---|---|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            "| "
            f"{row['item_id']} | {row['publisher']} | {row['locator']} | "
            f"{row['status_code']} | {row['network_checked']} | {row['body_text_stored']} |"
        )
    return "\n".join(lines)


def render_report(result: dict[str, Any]) -> str:
    lines = [
        "# ESLR1 External Source Connector Live-Metadata Report Fixture",
        "",
        "> Scope: render a public-safe review fixture from the KASB/FSS connector live-metadata scaffold.",
        "",
        "## 한 줄 결론",
        "",
        "`kasb-fss-interpretive-catalog` now has a human-readable report fixture built from metadata-only KASB/FSS connector records. The fixture proves we can show external source locator readiness without fetching or storing source text.",
        "",
        "## Fixture Result",
        "",
        f"- ok: {result['ok']}",
        f"- connector id: `{result['connector_id']}`",
        f"- public-safe report fixture created: {result['public_safe_report_fixture_created']}",
        f"- network checked by fixture: {result['network_checked']}",
        f"- record count: {result['record_count']}",
        f"- body text stored: {result['body_text_stored']}",
        f"- body cache created: {result['body_cache_created']}",
        f"- chunks created: {result['chunks_created']}",
        f"- embeddings created: {result['embeddings_created']}",
        f"- index created: {result['index_created']}",
        "",
        "## Review Fixture",
        "",
        render_fixture_table(result["fixture_rows"]),
        "",
        "## Boundary",
        "",
        "- This fixture is generated from metadata-only records.",
        "- It is suitable for showing connector readiness in a demo brief.",
        "- It does not enable external text as answer evidence.",
        "- K-IFRS paragraph DB remains the primary accounting evidence source.",
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
    return "\n".join(lines) + "\n"


def write_report() -> dict[str, Any]:
    result = build_live_metadata_report_fixture()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_report(result), encoding="utf-8")
    return result


def _fixture_row(record: dict[str, Any]) -> dict[str, Any]:
    locator = str(record.get("final_url") or record["url"])
    return {
        "item_id": record["item_id"],
        "source_id": record["source_id"],
        "publisher": record["publisher"],
        "allowed_use": record["allowed_use"],
        "locator": locator,
        "status_code": record["status_code"],
        "content_type": record["content_type"],
        "network_checked": record["network_checked"],
        "checked_at": record["checked_at"],
        "body_text_stored": record["body_text_stored"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Render KASB/FSS connector live-metadata report fixture.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = write_report() if args.write else build_live_metadata_report_fixture()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"connector_id: {result['connector_id']}")
        print(f"public_safe_report_fixture_created: {result['public_safe_report_fixture_created']}")
        print(f"network_checked: {result['network_checked']}")
        print(f"record_count: {result['record_count']}")
        print(f"body_text_stored: {result['body_text_stored']}")
        print(f"body_cache_created: {result['body_cache_created']}")
        print(f"chunks_created: {result['chunks_created']}")
        print(f"embeddings_created: {result['embeddings_created']}")
        print(f"index_created: {result['index_created']}")
        print(f"next_leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
