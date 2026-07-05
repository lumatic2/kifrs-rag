from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-sbi2-source-body-policy-record.md"


@dataclass(frozen=True)
class SourcePolicyRecord:
    policy_id: str
    source_class: str
    source_ids: list[str]
    storage_mode: str
    citation_role: str
    authority_level: str
    chunking_strategy: str
    retention_policy: str
    allowed_fields: list[str] = field(default_factory=list)
    forbidden_fields: list[str] = field(default_factory=list)
    primary_evidence_override_allowed: bool = False
    live_fetch_allowed: bool = False
    embedding_allowed: bool = False
    public_repo_body_commit_allowed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def default_source_policy_record() -> SourcePolicyRecord:
    from scripts.source_class_selection import build_source_class_selection

    selection = build_source_class_selection()
    return SourcePolicyRecord(
        policy_id="sbi2-interpretive-synthetic-policy",
        source_class=selection["selected_source_class"],
        source_ids=list(selection["selected_source_ids"]),
        storage_mode="synthetic_body_only",
        citation_role="supporting_interpretation",
        authority_level="interpretive",
        chunking_strategy="synthetic_short_sections",
        retention_policy="public_synthetic_fixture_only",
        allowed_fields=list(selection["allowed_fields"]),
        forbidden_fields=list(selection["forbidden_fields"]),
        primary_evidence_override_allowed=False,
        live_fetch_allowed=False,
        embedding_allowed=False,
        public_repo_body_commit_allowed=False,
    )


def validate_source_policy_record(policy: SourcePolicyRecord) -> list[str]:
    errors: list[str] = []
    if not policy.policy_id:
        errors.append("policy_id: policy_id is required")
    if policy.source_class != "interpretive_accounting_material":
        errors.append("source_class: first controlled lane must be interpretive_accounting_material")
    expected_sources = {"kasb-interpretation-material", "fss-accounting-inquiry"}
    if set(policy.source_ids) != expected_sources:
        errors.append(f"source_ids: expected {sorted(expected_sources)}")
    if policy.storage_mode != "synthetic_body_only":
        errors.append("storage_mode: storage mode must remain synthetic_body_only until authorization exists")
    if policy.citation_role != "supporting_interpretation":
        errors.append("citation_role: citation role must be supporting_interpretation")
    if policy.authority_level != "interpretive":
        errors.append("authority_level: authority level must be interpretive")
    if policy.chunking_strategy != "synthetic_short_sections":
        errors.append("chunking_strategy: chunking strategy must be synthetic_short_sections")
    if policy.retention_policy != "public_synthetic_fixture_only":
        errors.append("retention_policy: retention policy must be public_synthetic_fixture_only")
    for required in ("source_id", "title", "synthetic_body", "citation_role", "authority_level"):
        if required not in policy.allowed_fields:
            errors.append(f"allowed_fields: missing {required}")
    for required in ("copied external document text", "PDF body cache", "embedding dump", "API secret"):
        if required not in policy.forbidden_fields:
            errors.append(f"forbidden_fields: missing {required}")
    if policy.primary_evidence_override_allowed:
        errors.append("primary_evidence_override_allowed: controlled lane must not override K-IFRS primary evidence")
    if policy.live_fetch_allowed:
        errors.append("live_fetch_allowed: live fetch is not allowed in SBI2")
    if policy.embedding_allowed:
        errors.append("embedding_allowed: embeddings are not allowed in SBI2")
    if policy.public_repo_body_commit_allowed:
        errors.append("public_repo_body_commit_allowed: public repo body commits are not allowed")
    errors.extend(_public_safe_errors(policy.to_dict()))
    return errors


def build_source_policy_record() -> dict[str, Any]:
    policy = default_source_policy_record()
    errors = validate_source_policy_record(policy)
    return {
        "title": "SBI2 Source Policy Record",
        "ok": not errors,
        "policy": policy.to_dict(),
        "errors": errors,
        "completed_milestone": "SBI2",
        "next_leaf": "SBI3_synthetic_parser_chunker",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    policy = result["policy"]
    lines = [
        "# SBI2 Source Body Policy Record",
        "",
        "> Scope: machine-readable policy for the selected controlled interpretive source lane.",
        "",
        "## 한 줄 결론",
        "",
        "SBI2 fixes the selected interpretive lane as synthetic-body-only, supporting-interpretation evidence. It cannot live-fetch, embed, commit external body text, or override K-IFRS primary evidence.",
        "",
        "## Policy",
        "",
        f"- policy id: `{policy['policy_id']}`",
        f"- source class: `{policy['source_class']}`",
        f"- source ids: {', '.join(policy['source_ids'])}",
        f"- storage mode: `{policy['storage_mode']}`",
        f"- citation role: `{policy['citation_role']}`",
        f"- authority level: `{policy['authority_level']}`",
        f"- chunking strategy: `{policy['chunking_strategy']}`",
        f"- retention policy: `{policy['retention_policy']}`",
        "",
        "## Allowed Fields",
        "",
    ]
    lines.extend(f"- {field}" for field in policy["allowed_fields"])
    lines.extend(["", "## Forbidden Fields", ""])
    lines.extend(f"- {field}" for field in policy["forbidden_fields"])
    lines.extend(
        [
            "",
            "## Safety Flags",
            "",
            f"- primary evidence override allowed: {policy['primary_evidence_override_allowed']}",
            f"- live fetch allowed: {policy['live_fetch_allowed']}",
            f"- embedding allowed: {policy['embedding_allowed']}",
            f"- public repo body commit allowed: {policy['public_repo_body_commit_allowed']}",
            "",
            "## Errors",
            "",
        ]
    )
    lines.extend(f"- {error}" for error in result["errors"]) if result["errors"] else lines.append("- none")
    lines.extend(
        [
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
    result = build_source_policy_record()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _public_safe_errors(data: Any) -> list[str]:
    forbidden_keys = {"api_key", "token", "secret_value", "raw_text", "embedding_vector"}
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
    parser = argparse.ArgumentParser(description="Run SBI2 source policy record check.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_source_policy_record()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        policy = result["policy"]
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- storage mode: {policy['storage_mode']}")
        print(f"- citation role: {policy['citation_role']}")
        print(f"- next leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")
    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
