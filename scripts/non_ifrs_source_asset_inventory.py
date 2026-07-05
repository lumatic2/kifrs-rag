from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-nis1-source-asset-inventory.md"

LANES: dict[str, dict[str, Any]] = {
    "document_metadata": {
        "purpose": "KASB/FSS/FSC interpretive catalog entries and supporting document metadata without committed body text.",
        "reuse": [
            "docs/reports/2026-07-05-non-ifrs-source-map.md",
            "docs/reports/2026-07-05-as1-source-taxonomy.md",
            "docs/reports/2026-07-05-as2-authority-citation-policy.md",
            "docs/reports/2026-07-05-msi1-connector-contract.md",
            "docs/reports/2026-07-05-msi2-metadata-catalog-prototype.md",
            "docs/ingestion/source_manifest.example.json",
            "kifrs/ingestion/manifest.py",
            "scripts/validate_ingestion_manifest.py",
            "tests/test_ingestion_manifest.py",
        ],
        "build_next": [
            "NIS2 source record wrapper around document_metadata",
            "NIS3 non_ifrs_source_records fixture entries for KASB/FSS-style metadata",
        ],
        "exclude": [
            "KASB/FSS/FSC document body fetch",
            "copied interpretation text or excerpts",
        ],
    },
    "law_locator": {
        "purpose": "Law/regulation references as locators and legal-boundary evidence, not copied article text.",
        "reuse": [
            "docs/reports/2026-07-05-non-ifrs-source-map.md",
            "docs/reports/2026-07-05-msi1-connector-contract.md",
            "docs/ingestion/source_manifest.example.json",
            "kifrs/ingestion/manifest.py",
        ],
        "build_next": [
            "NIS2 explicit law locator record type or subtype policy",
            "NIS3 public-safe law locator fixture",
        ],
        "exclude": [
            "law article body copy",
            "full legal database ingestion",
        ],
    },
    "structured_fact": {
        "purpose": "OpenDART/XBRL-like company facts as structured values, separate from document RAG.",
        "reuse": [
            "docs/reports/2026-07-05-msi1-connector-contract.md",
            "docs/reports/2026-07-05-msi5-ingestion-gate-close-report.md",
            "docs/ingestion/source_manifest.example.json",
            "kifrs/ingestion/manifest.py",
            "tests/test_ingestion_manifest.py",
        ],
        "build_next": [
            "NIS2 structured_fact contract with authority/storage/retrieval lane fields",
            "NIS3 synthetic OpenDART-like facts in non_ifrs_source_records.example.json",
        ],
        "exclude": [
            "live OpenDART API call",
            "raw XML/XBRL dump",
            "external secret handling",
        ],
    },
    "client_private": {
        "purpose": "Local-only case facts from contracts, TB, accounting policies, and workpapers.",
        "reuse": [
            "docs/reports/2026-07-05-local-parser-real-adapter-implementation-plan.md",
            "docs/reports/2026-07-05-lpa1-local-parser-adapter-contract.md",
            "docs/reports/2026-07-05-lpas1-local-parser-adapter-scaffold.md",
            "docs/reports/2026-07-05-lpad1-local-parser-adapter-dry-run-gate.md",
            "kifrs/feedback/local_parser.py",
        ],
        "build_next": [
            "NIS2 client_private placeholder contract",
            "NIS3 local-only placeholder fixture without private content",
        ],
        "exclude": [
            "real client file upload",
            "OCR output body",
            "private document excerpts",
        ],
    },
    "policy_and_gate": {
        "purpose": "Cross-lane source taxonomy, storage policy, evidence manifest, and public-safe gates.",
        "reuse": [
            "docs/authority/sources.json",
            "docs/authority/source_pack.json",
            "docs/reports/2026-07-05-authority-source-map-close-report.md",
            "docs/reports/2026-07-05-msi4-provenance-citation-manifest.md",
            "docs/reports/2026-07-05-msi5-ingestion-gate-close-report.md",
            "docs/ingestion/evidence_manifest.example.json",
            "kifrs/ingestion/evidence.py",
            "scripts/validate_authority_sources.py",
            "scripts/validate_authority_source_pack.py",
            "scripts/validate_ingestion_evidence.py",
            "tests/test_ingestion_evidence.py",
        ],
        "build_next": [
            "NIS4 chunking and embedding policy",
            "NIS5 non_ifrs_dataization_gate",
        ],
        "exclude": [
            "default retriever change",
            "multi-authority answer composition runtime",
        ],
    },
}

FORBIDDEN_SCOPE = [
    "source body text",
    "law article body",
    "DART raw filing/XML/XBRL dump",
    "embeddings or vector store files",
    "external secrets",
    "client-private document body or excerpt",
]


def build_inventory() -> dict[str, Any]:
    lanes: dict[str, Any] = {}
    errors: list[str] = []
    for lane, payload in LANES.items():
        reuse = [_asset(path) for path in payload["reuse"]]
        missing = [item["path"] for item in reuse if not item["exists"]]
        if missing:
            errors.extend(f"{lane}: missing reusable asset {path}" for path in missing)
        lanes[lane] = {
            "purpose": payload["purpose"],
            "reusable_assets": reuse,
            "build_next": payload["build_next"],
            "excluded_from_active_implementation": payload["exclude"],
        }

    return {
        "ok": not errors,
        "title": "NIS1 Source Asset Inventory",
        "milestone": "NIS1",
        "lanes": lanes,
        "reusable_asset_count": sum(len(lane["reusable_assets"]) for lane in lanes.values()),
        "missing_asset_count": len(errors),
        "forbidden_scope": FORBIDDEN_SCOPE,
        "next_leaf": "NIS2_source_record_contract",
        "errors": errors,
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(inventory: dict[str, Any]) -> str:
    conclusion = (
        "Reuse the existing authority/MSI/client-private assets, then add a stricter source record contract in NIS2."
        if inventory["ok"]
        else "Fix missing reusable assets before opening NIS2."
    )
    lines = [
        "# NIS1 Source Asset Inventory",
        "",
        "> Scope: classify existing source-map, ingestion, connector, parser, and policy assets for non-IFRS source dataization.",
        "",
        "## One-Line Conclusion",
        "",
        conclusion,
        "",
        "## Lane Inventory",
        "",
    ]
    for lane, payload in inventory["lanes"].items():
        lines.extend(
            [
                f"### {lane}",
                "",
                payload["purpose"],
                "",
                "| Reusable Asset | Exists |",
                "|---|---|",
            ]
        )
        for asset in payload["reusable_assets"]:
            lines.append(f"| `{asset['path']}` | {asset['exists']} |")
        lines.extend(["", "Build next:"])
        lines.extend(f"- {item}" for item in payload["build_next"])
        lines.extend(["", "Excluded from active implementation:"])
        lines.extend(f"- {item}" for item in payload["excluded_from_active_implementation"])
        lines.append("")

    lines.extend(
        [
            "## Forbidden Scope",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in inventory["forbidden_scope"])
    lines.extend(
        [
            "",
            "## Next Leaf",
            "",
            inventory["next_leaf"],
        ]
    )
    if inventory["errors"]:
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in inventory["errors"])
    lines.extend(
        [
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps(inventory, ensure_ascii=False, indent=2, default=str),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH) -> dict[str, Any]:
    inventory = build_inventory()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(inventory), encoding="utf-8")
    return inventory


def _asset(path: str) -> dict[str, Any]:
    absolute = ROOT / path
    return {"path": path, "exists": absolute.exists(), "kind": "file" if absolute.is_file() else "missing"}


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Render NIS1 non-IFRS source asset inventory.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    inventory = write_report(args.out) if args.write else build_inventory()
    if args.format == "json":
        print(json.dumps(inventory, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(inventory), end="")
    else:
        print(inventory["title"])
        print(f"- ok: {inventory['ok']}")
        print(f"- lanes: {len(inventory['lanes'])}")
        print(f"- reusable_asset_count: {inventory['reusable_asset_count']}")
        print(f"- missing_asset_count: {inventory['missing_asset_count']}")
        print(f"- next_leaf: {inventory['next_leaf']}")
        print(f"- report_path: {inventory['report_path']}")
    if not inventory["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
