from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.external_source_body_ingestion_authorization_gate import check_authorization_gate  # noqa: E402
from scripts.external_source_body_ingestion_policy_plan_check import FORBIDDEN_PUBLIC_FIELDS  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-essd1-external-source-synthetic-parser-chunker-dry-run.md"

SYNTHETIC_FIXTURE = """
# Synthetic KASB/FSS Interpretive Memo

## Issue
The entity asks whether a bundled software setup fee should be recognized at contract inception or over the service period.

## Analysis
The setup activity does not transfer a distinct good or service to the customer. It supports access to the hosted service.

## Evidence Role
This source can only support interpretation. K-IFRS primary paragraphs remain the primary evidence for final treatment.
""".strip()


@dataclass(frozen=True)
class SyntheticChunkMetadata:
    chunk_id: str
    source_id: str
    source_class: str
    locator: str
    heading: str
    chunk_strategy: str
    citation_role: str
    topic_tags: list[str]
    synthetic_input_chars: int
    body_text_stored: bool
    embedding_created: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def run_synthetic_parser_chunker_dry_run() -> dict[str, Any]:
    authorization = check_authorization_gate()
    chunks = _parse_synthetic_fixture(SYNTHETIC_FIXTURE)
    chunk_dicts = [chunk.to_dict() for chunk in chunks]
    errors = _validate_chunk_metadata(chunk_dicts)
    if authorization["ok"] is not True:
        errors.extend(f"authorization_gate: {error}" for error in authorization["errors"])

    return {
        "ok": not errors,
        "errors": errors,
        "dry_run_id": "essd1-external-source-synthetic-parser-chunker-dry-run",
        "fixture_id": "essd1-synthetic-kasb-fss-interpretive-memo",
        "fixture_kind": "author_written_synthetic_external_source",
        "synthetic_input_sha256": hashlib.sha256(SYNTHETIC_FIXTURE.encode("utf-8")).hexdigest(),
        "source_id": "synthetic-kasb-fss-interpretive-memo",
        "source_class": "interpretive_accounting_material",
        "chunk_strategy": "private_qna_item_synthetic_dry_run",
        "chunk_count": len(chunk_dicts),
        "chunks": chunk_dicts,
        "body_text_stored": False,
        "embedding_created": False,
        "live_fetch_performed": False,
        "authorization_gate": {
            "ok": authorization["ok"],
            "decision": authorization["decision"],
            "allowed_to_implement": authorization["allowed_to_implement"],
            "authorization_present": authorization["authorization_present"],
            "report_path": authorization["report_path"],
        },
        "report_path": str(REPORT_PATH.relative_to(ROOT)),
        "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or external source synthetic parser/chunker close gate",
    }


def render_report(result: dict[str, Any]) -> str:
    lines = [
        "# ESSD1 External Source Synthetic Parser/Chunker Dry-Run",
        "",
        "> Scope: synthetic-only parser/chunker dry-run before any live external source body ingestion.",
        "",
        "## 한 줄 결론",
        "",
        "The project can now exercise an external-source parser/chunker shape without live fetch, stored body text, or embeddings. The dry-run uses author-written synthetic input and emits metadata-only chunk records.",
        "",
        "## Dry-Run Result",
        "",
        f"- ok: {result['ok']}",
        f"- fixture kind: {result['fixture_kind']}",
        f"- chunk count: {result['chunk_count']}",
        f"- live fetch performed: {result['live_fetch_performed']}",
        f"- body text stored: {result['body_text_stored']}",
        f"- embedding created: {result['embedding_created']}",
        "",
        "## Chunks",
        "",
        "| Chunk | Heading | Locator | Topic Tags |",
        "|---|---|---|---|",
    ]
    for chunk in result["chunks"]:
        tags = ", ".join(chunk["topic_tags"])
        lines.append(f"| `{chunk['chunk_id']}` | {chunk['heading']} | `{chunk['locator']}` | {tags} |")

    lines.extend([
        "",
        "## Boundary",
        "",
        "- This dry-run does not fetch or crawl any live external source.",
        "- This dry-run does not write source text, source body, embeddings, raw HTML, PDF bytes, or external cache artifacts.",
        "- Public output keeps chunk metadata only: id, heading, locator, role, tags, and synthetic input length.",
        "- K-IFRS primary evidence priority is unchanged.",
        "",
        "## Authorization Gate Snapshot",
        "",
        f"- gate ok: {result['authorization_gate']['ok']}",
        f"- decision: {result['authorization_gate']['decision']}",
        f"- allowed to implement live ingestion: {result['authorization_gate']['allowed_to_implement']}",
        f"- authorization present: {result['authorization_gate']['authorization_present']}",
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


def write_report() -> dict[str, Any]:
    result = run_synthetic_parser_chunker_dry_run()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_report(result), encoding="utf-8")
    return result


def _parse_synthetic_fixture(source: str) -> list[SyntheticChunkMetadata]:
    sections = re.findall(r"^##\s+(.+?)\n(.+?)(?=\n##\s+|\Z)", source, flags=re.MULTILINE | re.DOTALL)
    chunks: list[SyntheticChunkMetadata] = []
    for index, (heading, content) in enumerate(sections, start=1):
        clean_heading = heading.strip()
        clean_content = " ".join(content.split())
        chunks.append(
            SyntheticChunkMetadata(
                chunk_id=f"essd1-chunk-{index:02d}",
                source_id="synthetic-kasb-fss-interpretive-memo",
                source_class="interpretive_accounting_material",
                locator=f"synthetic://essd1/kasb-fss-interpretive-memo#{_slugify(clean_heading)}",
                heading=clean_heading,
                chunk_strategy="private_qna_item_synthetic_dry_run",
                citation_role="supporting_interpretation",
                topic_tags=_topic_tags(clean_heading, clean_content),
                synthetic_input_chars=len(clean_content),
                body_text_stored=False,
                embedding_created=False,
            )
        )
    return chunks


def _validate_chunk_metadata(chunks: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    if len(chunks) < 3:
        errors.append("chunks: expected at least three synthetic chunks")
    for idx, chunk in enumerate(chunks):
        prefix = f"chunks[{idx}]"
        forbidden_keys = sorted(FORBIDDEN_PUBLIC_FIELDS.intersection({key.lower() for key in chunk}))
        if forbidden_keys:
            errors.append(f"{prefix}: forbidden public fields present: {forbidden_keys}")
        if chunk.get("body_text_stored") is not False:
            errors.append(f"{prefix}: body_text_stored must be false")
        if chunk.get("embedding_created") is not False:
            errors.append(f"{prefix}: embedding_created must be false")
        if chunk.get("citation_role") != "supporting_interpretation":
            errors.append(f"{prefix}: citation_role must remain supporting_interpretation")
        if not str(chunk.get("locator", "")).startswith("synthetic://"):
            errors.append(f"{prefix}: locator must be synthetic://")
    return errors


def _topic_tags(heading: str, content: str) -> list[str]:
    text = f"{heading} {content}".lower()
    tags: list[str] = []
    if "setup" in text:
        tags.append("setup_fee")
    if "distinct" in text or "service" in text:
        tags.append("distinct_service")
    if "primary evidence" in text or "k-ifrs" in text:
        tags.append("evidence_priority")
    return tags or ["synthetic_interpretive_source"]


def _slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run external source synthetic parser/chunker dry-run.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = write_report() if args.write else run_synthetic_parser_chunker_dry_run()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"chunk_count: {result['chunk_count']}")
        print(f"live_fetch_performed: {result['live_fetch_performed']}")
        print(f"body_text_stored: {result['body_text_stored']}")
        print(f"embedding_created: {result['embedding_created']}")
        print(f"next_leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
