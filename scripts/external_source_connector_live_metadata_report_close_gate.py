from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.external_source_connector_live_metadata_report_fixture import (  # noqa: E402
    build_live_metadata_report_fixture,
    render_report as render_fixture_report,
)


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-eslrc1-external-source-connector-live-metadata-report-close-gate.md"


def check_live_metadata_report_close_gate(*, run_quality_preflight: bool = False) -> dict[str, Any]:
    fixture = build_live_metadata_report_fixture()
    rendered_fixture = render_fixture_report(fixture)
    quality = _run_quality_preflight() if run_quality_preflight else {"ran": False, "ok": None, "public_safe": None, "errors": []}
    errors: list[str] = []

    if fixture["ok"] is not True:
        errors.extend(f"report_fixture: {error}" for error in fixture["errors"])
    if fixture["public_safe_report_fixture_created"] is not True:
        errors.append("report_fixture: public-safe report fixture must be created")
    if fixture["record_count"] != 2:
        errors.append(f"report_fixture: expected 2 records, got {fixture['record_count']}")
    if "ESLR1 External Source Connector Live-Metadata Report Fixture" not in rendered_fixture:
        errors.append("report_fixture: rendered report title missing")
    if "metadata-only records" not in rendered_fixture:
        errors.append("report_fixture: rendered report must state metadata-only records")

    for flag in (
        "network_checked",
        "body_text_stored",
        "body_cache_created",
        "chunks_created",
        "embeddings_created",
        "index_created",
        "answer_time_body_use_enabled",
    ):
        if fixture.get(flag) is not False:
            errors.append(f"report_fixture: {flag} must be false")

    for idx, row in enumerate(fixture["fixture_rows"]):
        prefix = f"fixture_rows[{idx}]"
        if row.get("network_checked") is not False:
            errors.append(f"{prefix}: network_checked must be false")
        if row.get("body_text_stored") is not False:
            errors.append(f"{prefix}: body_text_stored must be false")
        if not row.get("locator"):
            errors.append(f"{prefix}: locator is required")

    if run_quality_preflight and quality["ok"] is not True:
        errors.extend(f"quality_preflight: {error}" for error in quality["errors"])
    if run_quality_preflight and quality["public_safe"] is not True:
        errors.append("quality_preflight: public_safe must be true")

    return {
        "ok": not errors,
        "errors": errors,
        "close_gate_id": "eslrc1-external-source-connector-live-metadata-report-close-gate",
        "connector_id": "kasb-fss-interpretive-catalog",
        "closed_scope": [
            "live-metadata report fixture",
            "metadata-only report rendering",
            "fixture row guards for locator/status/network/body flags",
        ],
        "still_not_implemented": [
            "source body fetching/crawling",
            "source body cache",
            "source-specific live chunks",
            "external source embeddings",
            "external source body index namespace",
            "answer-time use of external source body text",
        ],
        "report_fixture": {
            "ok": fixture["ok"],
            "report_path": fixture["report_path"],
            "record_count": fixture["record_count"],
            "network_checked": fixture["network_checked"],
            "body_text_stored": fixture["body_text_stored"],
            "body_cache_created": fixture["body_cache_created"],
            "chunks_created": fixture["chunks_created"],
            "embeddings_created": fixture["embeddings_created"],
            "index_created": fixture["index_created"],
            "answer_time_body_use_enabled": fixture["answer_time_body_use_enabled"],
        },
        "quality_preflight": quality,
        "report_path": str(REPORT_PATH.relative_to(ROOT)),
        "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or external source connector demo-index bridge",
    }


def render_report(result: dict[str, Any]) -> str:
    lines = [
        "# ESLRC1 External Source Connector Live-Metadata Report Close Gate",
        "",
        "> Scope: close gate for the KASB/FSS live-metadata report fixture.",
        "",
        "## 한 줄 결론",
        "",
        "`kasb-fss-interpretive-catalog` is closed at the live-metadata report fixture level. The product can show external source locator readiness in a public-safe report, while external source body ingestion and answer-time body use remain unimplemented.",
        "",
        "## Close Result",
        "",
        f"- ok: {result['ok']}",
        f"- connector id: `{result['connector_id']}`",
        f"- fixture report: `{result['report_fixture']['report_path']}`",
        f"- fixture record count: {result['report_fixture']['record_count']}",
        f"- network checked by fixture: {result['report_fixture']['network_checked']}",
        f"- body text stored: {result['report_fixture']['body_text_stored']}",
        f"- body cache created: {result['report_fixture']['body_cache_created']}",
        f"- chunks created: {result['report_fixture']['chunks_created']}",
        f"- embeddings created: {result['report_fixture']['embeddings_created']}",
        f"- index created: {result['report_fixture']['index_created']}",
        "",
        "## Closed Scope",
        "",
    ]
    lines.extend(f"- {item}" for item in result["closed_scope"])
    lines.extend([
        "",
        "## Still Not Implemented",
        "",
    ])
    lines.extend(f"- {item}" for item in result["still_not_implemented"])
    lines.extend([
        "",
        "## Quality Preflight",
        "",
        f"- ran: {result['quality_preflight']['ran']}",
        f"- ok: {result['quality_preflight']['ok']}",
        f"- public_safe: {result['quality_preflight']['public_safe']}",
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
    ])
    return "\n".join(lines) + "\n"


def write_report(*, run_quality_preflight: bool = False) -> dict[str, Any]:
    result = check_live_metadata_report_close_gate(run_quality_preflight=run_quality_preflight)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_report(result), encoding="utf-8")
    return result


def _run_quality_preflight() -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, "scripts/quality_preflight.py", "--format", "json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        return {
            "ran": True,
            "ok": False,
            "public_safe": None,
            "errors": [completed.stderr.strip() or completed.stdout.strip() or f"exit {completed.returncode}"],
        }
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        return {"ran": True, "ok": False, "public_safe": None, "errors": [f"invalid quality_preflight json: {exc}"]}
    return {
        "ran": True,
        "ok": payload.get("ok") is True,
        "public_safe": payload.get("public_safe") is True,
        "errors": payload.get("errors", []),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Close KASB/FSS live-metadata report fixture lane.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--run-quality-preflight", action="store_true")
    args = parser.parse_args()

    result = (
        write_report(run_quality_preflight=args.run_quality_preflight)
        if args.write
        else check_live_metadata_report_close_gate(run_quality_preflight=args.run_quality_preflight)
    )
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"connector_id: {result['connector_id']}")
        print(f"record_count: {result['report_fixture']['record_count']}")
        print(f"network_checked: {result['report_fixture']['network_checked']}")
        print(f"body_text_stored: {result['report_fixture']['body_text_stored']}")
        print(f"body_cache_created: {result['report_fixture']['body_cache_created']}")
        print(f"chunks_created: {result['report_fixture']['chunks_created']}")
        print(f"embeddings_created: {result['report_fixture']['embeddings_created']}")
        print(f"index_created: {result['report_fixture']['index_created']}")
        print(f"quality_preflight: {result['quality_preflight']}")
        print(f"next_leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
