from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCES_PATH = ROOT / "docs" / "authority" / "sources.json"
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-sbi1-source-class-selection.md"


@dataclass(frozen=True)
class SourceClassCandidate:
    source_class: str
    source_ids: list[str]
    lane_type: str
    product_value: int
    body_lane_fit: int
    authorization_status: str
    implementation_mode: str
    rationale: str

    @property
    def score(self) -> int:
        authorization_penalty = 0 if self.implementation_mode == "synthetic_body_only" else 2
        return self.product_value + self.body_lane_fit - authorization_penalty

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["score"] = self.score
        return payload


def build_source_class_selection() -> dict[str, Any]:
    source_registry = json.loads(SOURCES_PATH.read_text(encoding="utf-8"))
    source_ids = {source["id"] for source in source_registry["sources"]}
    candidates = [
        SourceClassCandidate(
            source_class="interpretive_accounting_material",
            source_ids=["kasb-interpretation-material", "fss-accounting-inquiry"],
            lane_type="document_body_controlled_lane",
            product_value=5,
            body_lane_fit=5,
            authorization_status="not_authorized_for_body",
            implementation_mode="synthetic_body_only",
            rationale="Highest fit for controlled source-body ingestion: KASB/FSS-style guidance is useful as supporting interpretation but cannot be copied without authorization.",
        ),
        SourceClassCandidate(
            source_class="law_regulation",
            source_ids=["commercial-act-capital"],
            lane_type="law_locator",
            product_value=4,
            body_lane_fit=3,
            authorization_status="not_authorized_for_body",
            implementation_mode="locator_or_synthetic_body_only",
            rationale="Useful legal boundary evidence, but locator-first handling is safer than body chunking.",
        ),
        SourceClassCandidate(
            source_class="filing_data",
            source_ids=["opendart-structured-financials"],
            lane_type="structured_fact",
            product_value=4,
            body_lane_fit=1,
            authorization_status="metadata_or_api_contract_only",
            implementation_mode="structured_fact_only",
            rationale="Valuable for company facts, but not a source-body ingestion lane.",
        ),
        SourceClassCandidate(
            source_class="client_private",
            source_ids=["client-private-local"],
            lane_type="local_private_case_facts",
            product_value=5,
            body_lane_fit=2,
            authorization_status="user_owned_local_only",
            implementation_mode="structured_facts_only",
            rationale="Important product path, but just closed under the local parser prototype horizon.",
        ),
    ]
    missing_source_ids = sorted(
        source_id
        for candidate in candidates
        for source_id in candidate.source_ids
        if source_id not in source_ids
    )
    selected = max(candidates, key=lambda candidate: candidate.score)
    allowed_fields = [
        "source_id",
        "title",
        "issuer",
        "publication_date",
        "url_or_locator",
        "topic_tags",
        "synthetic_body",
        "citation_role",
        "authority_level",
    ]
    forbidden_fields = [
        "copied external document text",
        "full article text",
        "PDF body cache",
        "embedding dump",
        "API secret",
        "client-private payload",
    ]
    return {
        "title": "SBI1 Source Class Selection",
        "ok": not missing_source_ids,
        "selected_source_class": selected.source_class,
        "selected_source_ids": selected.source_ids,
        "selected_lane_type": selected.lane_type,
        "authorization_status": selected.authorization_status,
        "implementation_mode": selected.implementation_mode,
        "allowed_fields": allowed_fields,
        "forbidden_fields": forbidden_fields,
        "fallback_plan": "Use synthetic_body_only until explicit source-specific authorization exists; keep K-IFRS primary evidence unchanged.",
        "candidates": [candidate.to_dict() for candidate in candidates],
        "missing_source_ids": missing_source_ids,
        "completed_milestone": "SBI1",
        "next_leaf": "SBI2_source_policy_record",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(selection: dict[str, Any]) -> str:
    lines = [
        f"# {selection['title']}",
        "",
        "> Scope: choose the first controlled non-IFRS source-body lane and document its authorization boundary.",
        "",
        "## 한 줄 결론",
        "",
        "Select `interpretive_accounting_material` as the first controlled source-body lane. Because body-level authorization is absent, implementation remains synthetic-body-only until a source-specific authorization record exists.",
        "",
        "## Selected Lane",
        "",
        f"- source class: `{selection['selected_source_class']}`",
        f"- source ids: {', '.join(selection['selected_source_ids'])}",
        f"- lane type: `{selection['selected_lane_type']}`",
        f"- authorization status: `{selection['authorization_status']}`",
        f"- implementation mode: `{selection['implementation_mode']}`",
        f"- fallback plan: {selection['fallback_plan']}",
        "",
        "## Candidate Comparison",
        "",
        "| Source Class | Source IDs | Lane Type | Score | Authorization | Mode | Rationale |",
        "|---|---|---|---|---|---|---|",
    ]
    for candidate in selection["candidates"]:
        lines.append(
            "| {source_class} | {source_ids} | `{lane_type}` | {score} | `{authorization_status}` | `{implementation_mode}` | {rationale} |".format(
                **{
                    **candidate,
                    "source_ids": ", ".join(candidate["source_ids"]),
                }
            )
        )
    lines.extend(["", "## Allowed Fields", ""])
    lines.extend(f"- {field}" for field in selection["allowed_fields"])
    lines.extend(["", "## Forbidden Fields", ""])
    lines.extend(f"- {field}" for field in selection["forbidden_fields"])
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- SBI1 does not fetch, scrape, cache, chunk, or embed external body text.",
            "- SBI1 selects the controlled lane and authorization boundary only.",
            "- K-IFRS paragraph evidence remains primary.",
            "",
            "## Next Leaf",
            "",
            str(selection["next_leaf"]),
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps(selection, ensure_ascii=False, indent=2, default=str),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH) -> dict[str, Any]:
    selection = build_source_class_selection()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(selection), encoding="utf-8")
    return selection


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run SBI1 source class selection.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    selection = write_report(args.out) if args.write else build_source_class_selection()
    if args.format == "json":
        print(json.dumps(selection, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(selection), end="")
    else:
        print(selection["title"])
        print(f"- ok: {selection['ok']}")
        print(f"- selected source class: {selection['selected_source_class']}")
        print(f"- authorization: {selection['authorization_status']}")
        print(f"- implementation mode: {selection['implementation_mode']}")
        print(f"- next leaf: {selection['next_leaf']}")
    if not selection["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
