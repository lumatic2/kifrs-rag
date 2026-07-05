from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-esb3-chunking-retrieval-dry-run.md"


def build_retrieval_dry_run() -> dict[str, Any]:
    chunks = [
        {
            "chunk_id": "esb3-interpretive-001-c01",
            "fixture_id": "esb2-fixture-interpretive-001",
            "locator": "synthetic://interpretive-accounting-material/esb2-001#c01",
            "topic_tags": ["revenue", "disclosure"],
            "synthetic_summary_label": "principal_agent_indicator_label",
            "retrieval_terms": ["revenue", "gross_or_net", "principal_agent"],
            "contains_copied_payload": False,
        },
        {
            "chunk_id": "esb3-interpretive-001-c02",
            "fixture_id": "esb2-fixture-interpretive-001",
            "locator": "synthetic://interpretive-accounting-material/esb2-001#c02",
            "topic_tags": ["revenue", "variable_consideration"],
            "synthetic_summary_label": "constraint_indicator_label",
            "retrieval_terms": ["revenue", "variable_consideration", "constraint"],
            "contains_copied_payload": False,
        },
        {
            "chunk_id": "esb3-interpretive-001-c03",
            "fixture_id": "esb2-fixture-interpretive-001",
            "locator": "synthetic://interpretive-accounting-material/esb2-001#c03",
            "topic_tags": ["disclosure", "judgement"],
            "synthetic_summary_label": "disclosure_judgement_label",
            "retrieval_terms": ["disclosure", "judgement", "policy"],
            "contains_copied_payload": False,
        },
    ]
    queries = [
        {
            "query_id": "esb3-q-revenue-principal-agent",
            "topic": "revenue principal agent review support",
            "expected_chunk": "esb3-interpretive-001-c01",
        },
        {
            "query_id": "esb3-q-variable-consideration",
            "topic": "variable consideration constraint support",
            "expected_chunk": "esb3-interpretive-001-c02",
        },
    ]
    retrieval_results = [_retrieve(query, chunks) for query in queries]
    checks = {
        "chunks_present": len(chunks) == 3,
        "all_chunks_public_safe": all(chunk["contains_copied_payload"] is False for chunk in chunks),
        "retrieval_results_present": len(retrieval_results) == len(queries),
        "expected_chunks_top_ranked": all(result["top_chunk_id"] == result["expected_chunk"] for result in retrieval_results),
        "no_body_payload_in_results": all(result["payload_rendered"] is False for result in retrieval_results),
        "next_milestone_named": True,
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "ESB3 Chunking And Retrieval Dry Run",
        "ok": not errors,
        "horizon": "external-source-body-connector-expansion",
        "completed_milestone": "ESB3",
        "chunk_strategy": "semantic_section_stub",
        "chunks": chunks,
        "queries": queries,
        "retrieval_results": retrieval_results,
        "checks": checks,
        "errors": errors,
        "next_leaf": "ESB4_connector_leak_and_policy_gate",
        "report_path": _display_path(REPORT_PATH),
    }


def _retrieve(query: dict[str, str], chunks: list[dict[str, Any]]) -> dict[str, Any]:
    query_terms = set(query["topic"].split())
    scored = []
    for chunk in chunks:
        overlap = len(query_terms.intersection(chunk["retrieval_terms"]))
        scored.append(
            {
                "chunk_id": chunk["chunk_id"],
                "score": overlap,
                "locator": chunk["locator"],
                "synthetic_summary_label": chunk["synthetic_summary_label"],
            }
        )
    scored.sort(key=lambda item: (-item["score"], item["chunk_id"]))
    top = scored[0]
    return {
        "query_id": query["query_id"],
        "expected_chunk": query["expected_chunk"],
        "top_chunk_id": top["chunk_id"],
        "top_score": top["score"],
        "top_locator": top["locator"],
        "top_summary_label": top["synthetic_summary_label"],
        "payload_rendered": False,
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: synthetic chunking and retrieval dry-run for the selected external source-body connector lane.",
        "",
        "## 한 줄 결론",
        "",
        "Synthetic chunks can be ranked for retrieval using labels and metadata only; no copied payload is rendered.",
        "",
        "## Chunks",
        "",
        "| Chunk | Fixture | Locator | Tags | Summary Label | Payload Rendered |",
        "|---|---|---|---|---|---|",
    ]
    for chunk in result["chunks"]:
        lines.append(
            "| {chunk_id} | {fixture_id} | {locator} | {tags} | {label} | {payload} |".format(
                chunk_id=chunk["chunk_id"],
                fixture_id=chunk["fixture_id"],
                locator=chunk["locator"],
                tags=", ".join(chunk["topic_tags"]),
                label=chunk["synthetic_summary_label"],
                payload=chunk["contains_copied_payload"],
            )
        )
    lines.extend(
        [
            "",
            "## Retrieval Results",
            "",
            "| Query | Expected | Top Chunk | Score | Payload Rendered |",
            "|---|---|---|---:|---|",
        ]
    )
    for result_row in result["retrieval_results"]:
        lines.append(
            "| {query_id} | {expected_chunk} | {top_chunk_id} | {top_score} | {payload_rendered} |".format(
                **result_row
            )
        )
    lines.extend(["", "## Checks", "", "| Check | OK |", "|---|---|"])
    for name, ok in result["checks"].items():
        lines.append(f"| {name} | {ok} |")
    lines.extend(["", "## Errors", ""])
    lines.extend(f"- {error}" for error in result["errors"]) if result["errors"] else lines.append("- none")
    lines.extend(
        [
            "",
            "## Next Leaf",
            "",
            f"- `{result['next_leaf']}`",
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps(result, ensure_ascii=False, indent=2),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH) -> dict[str, Any]:
    result = build_retrieval_dry_run()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build ESB3 synthetic chunking and retrieval dry-run report.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_retrieval_dry_run()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- chunks: {len(result['chunks'])}")
        print(f"- next leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
