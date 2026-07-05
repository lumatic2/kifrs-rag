from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.external_source_connector_live_metadata_decision_gate import (  # noqa: E402
    ALLOWED_LIVE_METADATA_FIELDS,
    FORBIDDEN_LIVE_METADATA_FIELDS,
    check_live_metadata_decision_gate,
)
from scripts.live_external_source_validation import default_fetcher  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-eslp1-external-source-connector-live-metadata-probe-scaffold.md"


@dataclass(frozen=True)
class LiveMetadataProbeRecord:
    item_id: str
    source_id: str
    publisher: str
    allowed_use: str
    url: str
    status_code: int | None
    final_url: str
    content_type: str
    network_checked: bool
    checked_at: str
    body_text_stored: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def run_live_metadata_probe_scaffold(
    *,
    allow_network: bool = False,
    timeout: float = 10.0,
    checked_at: str | None = None,
    fetcher: Callable[[str, float], dict[str, object]] | None = None,
) -> dict[str, Any]:
    decision = check_live_metadata_decision_gate()
    errors: list[str] = []
    if decision["ok"] is not True:
        errors.extend(f"decision_gate: {error}" for error in decision["errors"])
    if decision["live_metadata_probe_allowed"] is not True:
        errors.append("decision_gate: live metadata probe is not allowed")
    if allow_network and decision["live_network_probe_allowed"] is not True:
        errors.append("decision_gate: live network probe is not allowed")

    timestamp = checked_at or datetime.now(timezone.utc).isoformat()
    fetch = fetcher or default_fetcher
    records: list[dict[str, Any]] = []

    for target in decision["live_contract"]["connector_targets"]:
        probe: dict[str, object]
        if allow_network:
            probe = fetch(str(target["url"]), timeout)
        else:
            probe = {
                "ok": None,
                "status_code": None,
                "final_url": "",
                "content_type": "",
                "error": "network_not_enabled",
            }

        record = LiveMetadataProbeRecord(
            item_id=str(target["item_id"]),
            source_id=str(target["source_id"]),
            publisher=str(target["publisher"]),
            allowed_use=str(target["allowed_use"]),
            url=str(target["url"]),
            status_code=probe.get("status_code") if isinstance(probe.get("status_code"), int) else None,
            final_url=str(probe.get("final_url") or ""),
            content_type=str(probe.get("content_type") or ""),
            network_checked=allow_network,
            checked_at=timestamp,
            body_text_stored=False,
        ).to_dict()
        records.append(record)

        if allow_network and probe.get("ok") is not True:
            errors.append(f"{record['item_id']}: live metadata probe failed: {probe.get('error') or probe.get('status_code')}")

    forbidden_paths = _find_forbidden_fields(records)
    if forbidden_paths:
        errors.extend(f"probe_records: {path} forbidden field" for path in forbidden_paths)

    extra_fields = _find_extra_fields(records)
    if extra_fields:
        errors.extend(f"probe_records: {field} is not in allowed live metadata fields" for field in extra_fields)

    if any(record["body_text_stored"] is not False for record in records):
        errors.append("probe_records: body_text_stored must remain false")

    return {
        "ok": not errors,
        "errors": errors,
        "scaffold_id": "eslp1-external-source-connector-live-metadata-probe-scaffold",
        "connector_id": "kasb-fss-interpretive-catalog",
        "allow_network": allow_network,
        "record_count": len(records),
        "body_text_stored": False,
        "body_cache_created": False,
        "chunks_created": False,
        "embeddings_created": False,
        "index_created": False,
        "answer_time_body_use_enabled": False,
        "decision_gate": {
            "ok": decision["ok"],
            "report_path": decision["report_path"],
            "decision": decision["decision"],
        },
        "allowed_live_metadata_fields": ALLOWED_LIVE_METADATA_FIELDS,
        "forbidden_live_metadata_fields": FORBIDDEN_LIVE_METADATA_FIELDS,
        "probe_records": records,
        "report_path": str(REPORT_PATH.relative_to(ROOT)),
        "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or external source connector live-metadata close gate",
    }


def render_report(result: dict[str, Any]) -> str:
    lines = [
        "# ESLP1 External Source Connector Live-Metadata Probe Scaffold",
        "",
        "> Scope: scaffold live metadata probes for the KASB/FSS interpretive connector.",
        "",
        "## 한 줄 결론",
        "",
        "`kasb-fss-interpretive-catalog` now has a live-metadata probe scaffold. It can check locator/status/final URL/content type metadata, while source body fetch, body cache, chunking, embeddings, indexing, and answer-time body use remain disabled.",
        "",
        "## Scaffold Result",
        "",
        f"- ok: {result['ok']}",
        f"- connector id: `{result['connector_id']}`",
        f"- allow network: {result['allow_network']}",
        f"- probe record count: {result['record_count']}",
        f"- body text stored: {result['body_text_stored']}",
        f"- body cache created: {result['body_cache_created']}",
        f"- chunks created: {result['chunks_created']}",
        f"- embeddings created: {result['embeddings_created']}",
        f"- index created: {result['index_created']}",
        f"- answer-time body use enabled: {result['answer_time_body_use_enabled']}",
        "",
        "## Probe Records",
        "",
        "| Item | Publisher | Network | Status | Final URL | Body Stored |",
        "|---|---|---:|---:|---|---|",
    ]
    for record in result["probe_records"]:
        lines.append(
            "| "
            f"{record['item_id']} | {record['publisher']} | {record['network_checked']} | "
            f"{record['status_code']} | {record['final_url'] or record['url']} | {record['body_text_stored']} |"
        )

    lines.extend([
        "",
        "## Boundary",
        "",
        "- This scaffold stores metadata fields only.",
        "- It must not store source body, copied excerpts, raw HTML, chunks, embeddings, or external body indexes.",
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
    ])
    return "\n".join(lines) + "\n"


def write_report(*, allow_network: bool = False, timeout: float = 10.0) -> dict[str, Any]:
    result = run_live_metadata_probe_scaffold(allow_network=allow_network, timeout=timeout)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_report(result), encoding="utf-8")
    return result


def _find_forbidden_fields(value: Any, path: str = "$") -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            key_path = f"{path}.{key}"
            if str(key).lower() in FORBIDDEN_LIVE_METADATA_FIELDS:
                errors.append(key_path)
            errors.extend(_find_forbidden_fields(nested, key_path))
    elif isinstance(value, list):
        for idx, nested in enumerate(value):
            errors.extend(_find_forbidden_fields(nested, f"{path}[{idx}]"))
    return errors


def _find_extra_fields(records: list[dict[str, Any]]) -> list[str]:
    allowed = set(ALLOWED_LIVE_METADATA_FIELDS)
    extras: set[str] = set()
    for record in records:
        extras.update(set(record) - allowed)
    return sorted(extras)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run KASB/FSS live metadata probe scaffold.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--allow-network", action="store_true")
    parser.add_argument("--timeout", type=float, default=10.0)
    args = parser.parse_args()

    result = (
        write_report(allow_network=args.allow_network, timeout=args.timeout)
        if args.write
        else run_live_metadata_probe_scaffold(allow_network=args.allow_network, timeout=args.timeout)
    )
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"connector_id: {result['connector_id']}")
        print(f"allow_network: {result['allow_network']}")
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
