from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-sbi3-synthetic-body-parser-chunker.md"


@dataclass(frozen=True)
class SyntheticBodyFixture:
    fixture_id: str
    source_id: str
    title: str
    issuer: str
    topic_tags: list[str]
    synthetic_body: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SyntheticChunk:
    chunk_id: str
    source_id: str
    section_index: int
    text: str
    citation_role: str
    authority_level: str
    topic_tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def default_synthetic_fixture() -> SyntheticBodyFixture:
    return SyntheticBodyFixture(
        fixture_id="sbi3-kasb-fss-interpretive-synthetic",
        source_id="kasb-interpretation-material",
        title="Synthetic revenue and lease interpretation note",
        issuer="synthetic KASB/FSS-style source",
        topic_tags=["revenue", "lease", "supporting interpretation"],
        synthetic_body=(
            "Revenue guidance summary: identify the contract, promised goods, and timing pattern. "
            "Lease guidance summary: confirm control of use, term evidence, and payment pattern. "
            "This synthetic note supports interpretation only and does not replace K-IFRS paragraph evidence."
        ),
    )


def parse_and_chunk_synthetic_body(fixture: SyntheticBodyFixture) -> list[SyntheticChunk]:
    from scripts.source_policy_record import default_source_policy_record

    policy = default_source_policy_record()
    errors = validate_synthetic_fixture(fixture)
    if errors:
        raise ValueError("; ".join(errors))
    sentences = [part.strip() for part in re.split(r"(?<=\.)\s+", fixture.synthetic_body) if part.strip()]
    chunks = [
        SyntheticChunk(
            chunk_id=f"{fixture.fixture_id}-chunk-{index}",
            source_id=fixture.source_id,
            section_index=index,
            text=sentence,
            citation_role=policy.citation_role,
            authority_level=policy.authority_level,
            topic_tags=list(fixture.topic_tags),
        )
        for index, sentence in enumerate(sentences, start=1)
    ]
    return chunks


def validate_synthetic_fixture(fixture: SyntheticBodyFixture) -> list[str]:
    errors: list[str] = []
    if not fixture.fixture_id:
        errors.append("fixture_id: fixture_id is required")
    if fixture.source_id not in {"kasb-interpretation-material", "fss-accounting-inquiry"}:
        errors.append("source_id: source_id must belong to selected interpretive lane")
    if not fixture.synthetic_body:
        errors.append("synthetic_body: synthetic_body is required")
    if "synthetic" not in fixture.synthetic_body.lower():
        errors.append("synthetic_body: body must explicitly state it is synthetic")
    if len(fixture.synthetic_body) > 800:
        errors.append("synthetic_body: fixture must stay short")
    errors.extend(_public_safe_errors(fixture.to_dict()))
    return errors


def validate_synthetic_chunks(chunks: list[SyntheticChunk]) -> list[str]:
    from scripts.source_policy_record import default_source_policy_record

    policy = default_source_policy_record()
    errors: list[str] = []
    if not chunks:
        errors.append("chunks: at least one chunk is required")
    for chunk in chunks:
        if chunk.citation_role != policy.citation_role:
            errors.append(f"{chunk.chunk_id}: citation role must be {policy.citation_role}")
        if chunk.authority_level != policy.authority_level:
            errors.append(f"{chunk.chunk_id}: authority level must be {policy.authority_level}")
        if len(chunk.text) > 300:
            errors.append(f"{chunk.chunk_id}: chunk text is too long")
        if "synthetic" not in chunk.text.lower() and chunk.section_index == len(chunks):
            errors.append(f"{chunk.chunk_id}: final chunk must preserve synthetic boundary")
        errors.extend(_public_safe_errors(chunk.to_dict()))
    return errors


def build_synthetic_body_parser_chunker() -> dict[str, Any]:
    fixture = default_synthetic_fixture()
    fixture_errors = validate_synthetic_fixture(fixture)
    chunks = [] if fixture_errors else parse_and_chunk_synthetic_body(fixture)
    chunk_errors = validate_synthetic_chunks(chunks) if chunks else []
    errors = fixture_errors + chunk_errors
    return {
        "title": "SBI3 Synthetic Body Parser And Chunker",
        "ok": not errors,
        "fixture": fixture.to_dict(),
        "chunks": [chunk.to_dict() for chunk in chunks],
        "chunk_count": len(chunks),
        "errors": errors,
        "completed_milestone": "SBI3",
        "next_leaf": "SBI4_controlled_lane_retrieval_gate",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    fixture = result["fixture"]
    lines = [
        "# SBI3 Synthetic Body Parser And Chunker",
        "",
        "> Scope: synthetic-only parser/chunker dry-run for the selected interpretive lane.",
        "",
        "## 한 줄 결론",
        "",
        "SBI3 turns a short synthetic interpretive fixture into public-safe chunks with supporting-interpretation citation role. No protected external text, live fetch, OCR, embedding, or body cache is created.",
        "",
        "## Fixture",
        "",
        f"- fixture id: `{fixture['fixture_id']}`",
        f"- source id: `{fixture['source_id']}`",
        f"- title: {fixture['title']}",
        f"- issuer: {fixture['issuer']}",
        f"- topic tags: {', '.join(fixture['topic_tags'])}",
        "",
        "## Chunks",
        "",
        "| Chunk | Source | Role | Authority | Text |",
        "|---|---|---|---|---|",
    ]
    for chunk in result["chunks"]:
        lines.append(
            f"| `{chunk['chunk_id']}` | `{chunk['source_id']}` | `{chunk['citation_role']}` | `{chunk['authority_level']}` | {chunk['text']} |"
        )
    lines.extend(["", "## Errors", ""])
    lines.extend(f"- {error}" for error in result["errors"]) if result["errors"] else lines.append("- none")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This is synthetic-only parser/chunker evidence.",
            "- It does not fetch, copy, cache, OCR, embed, or index external body text.",
            "- K-IFRS paragraph evidence remains primary.",
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
    )
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH) -> dict[str, Any]:
    result = build_synthetic_body_parser_chunker()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _public_safe_errors(data: Any) -> list[str]:
    forbidden_keys = {"api_key", "token", "secret_value", "raw_text", "embedding_vector", "copied_text"}
    errors: list[str] = []

    def visit(value: Any, path: str) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                key_path = f"{path}.{key}" if path else str(key)
                if str(key) in forbidden_keys:
                    errors.append(f"{key_path}: forbidden public field")
                visit(child, key_path)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                visit(child, f"{path}[{index}]")

    visit(data, "")
    return errors


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run SBI3 synthetic parser/chunker dry-run.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_synthetic_body_parser_chunker()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- chunk count: {result['chunk_count']}")
        print(f"- next leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")
    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
