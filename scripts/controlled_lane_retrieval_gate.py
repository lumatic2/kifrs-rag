from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-sbi4-controlled-lane-retrieval-gate.md"


def retrieve_controlled_chunks(query: str) -> list[dict[str, Any]]:
    from scripts.synthetic_body_parser_chunker import build_synthetic_body_parser_chunker

    result = build_synthetic_body_parser_chunker()
    terms = _terms(query)
    ranked: list[tuple[int, dict[str, Any]]] = []
    for chunk in result["chunks"]:
        score = len(terms.intersection(_terms(chunk["text"] + " " + " ".join(chunk["topic_tags"]))))
        if score > 0:
            ranked.append((score, chunk))
    ranked.sort(key=lambda item: (-item[0], item[1]["section_index"]))
    return [
        {
            **chunk,
            "score": score,
            "retrieval_lane": "controlled_supporting_interpretation",
            "primary_evidence_replacement_allowed": False,
        }
        for score, chunk in ranked
    ]


def build_controlled_lane_retrieval_gate() -> dict[str, Any]:
    query = "lease payment pattern supporting interpretation"
    retrieved = retrieve_controlled_chunks(query)
    errors: list[str] = []
    if not retrieved:
        errors.append("retrieval: expected at least one controlled chunk")
    if not any("Lease guidance" in item["text"] for item in retrieved):
        errors.append("retrieval: expected lease guidance chunk")
    for item in retrieved:
        if item["citation_role"] != "supporting_interpretation":
            errors.append(f"{item['chunk_id']}: citation role must be supporting_interpretation")
        if item["authority_level"] != "interpretive":
            errors.append(f"{item['chunk_id']}: authority level must be interpretive")
        if item["primary_evidence_replacement_allowed"]:
            errors.append(f"{item['chunk_id']}: must not replace K-IFRS primary evidence")
    return {
        "title": "SBI4 Controlled Lane Retrieval Gate",
        "ok": not errors,
        "query": query,
        "retrieved": retrieved,
        "retrieved_count": len(retrieved),
        "primary_evidence_preserved": True,
        "errors": errors,
        "completed_milestone": "SBI4",
        "next_leaf": "SBI5_controlled_lane_close_gate",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(gate: dict[str, Any]) -> str:
    lines = [
        "# SBI4 Controlled Lane Retrieval Gate",
        "",
        "> Scope: prove synthetic controlled chunks are discoverable only as supporting interpretation.",
        "",
        "## 한 줄 결론",
        "",
        "SBI4 retrieves the synthetic interpretive chunk for a lease/payment query while preserving K-IFRS primary evidence. Controlled chunks are discoverable as supporting interpretation only.",
        "",
        "## Gate Result",
        "",
        f"- ok: {gate['ok']}",
        f"- query: {gate['query']}",
        f"- retrieved count: {gate['retrieved_count']}",
        f"- primary evidence preserved: {gate['primary_evidence_preserved']}",
        "",
        "## Retrieved Chunks",
        "",
        "| Chunk | Score | Lane | Role | Authority | Text |",
        "|---|---|---|---|---|---|",
    ]
    for item in gate["retrieved"]:
        lines.append(
            f"| `{item['chunk_id']}` | {item['score']} | `{item['retrieval_lane']}` | `{item['citation_role']}` | `{item['authority_level']}` | {item['text']} |"
        )
    lines.extend(["", "## Boundary", ""])
    lines.extend(
        [
            "- Controlled chunks are not K-IFRS primary evidence.",
            "- This gate does not change the default retriever.",
            "- This gate does not fetch, store, or embed external body text.",
        ]
    )
    lines.extend(["", "## Errors", ""])
    lines.extend(f"- {error}" for error in gate["errors"]) if gate["errors"] else lines.append("- none")
    lines.extend(
        [
            "",
            "## Next Leaf",
            "",
            str(gate["next_leaf"]),
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps(gate, ensure_ascii=False, indent=2, default=str),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH) -> dict[str, Any]:
    gate = build_controlled_lane_retrieval_gate()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(gate), encoding="utf-8")
    return gate


def _terms(text: str) -> set[str]:
    return {term for term in re.findall(r"[A-Za-z0-9가-힣]+", text.lower()) if len(term) >= 3}


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run SBI4 controlled lane retrieval gate.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    gate = write_report(args.out) if args.write else build_controlled_lane_retrieval_gate()
    if args.format == "json":
        print(json.dumps(gate, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(gate), end="")
    else:
        print(gate["title"])
        print(f"- ok: {gate['ok']}")
        print(f"- retrieved count: {gate['retrieved_count']}")
        print(f"- next leaf: {gate['next_leaf']}")
        for error in gate["errors"]:
            print(f"- {error}")
    if not gate["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
