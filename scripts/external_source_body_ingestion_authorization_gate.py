from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.external_source_body_ingestion_decision_gate import (  # noqa: E402
    check_body_ingestion_decision_gate,
)
from scripts.external_source_body_ingestion_policy_plan_check import (  # noqa: E402
    check_policy_plan,
)


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-esag1-external-source-body-authorization-gate.md"

ALLOWED_AUTHORIZATION_SCOPES = {
    "synthetic_dry_run_only",
    "source_specific_local_private_body",
}


@dataclass(frozen=True)
class BodyIngestionAuthorization:
    authorized_by: str
    authorization_scope: str
    risk_acknowledgement: bool
    source_review_required: bool
    public_repo_body_commit_allowed: bool
    live_fetch_allowed: bool
    chunking_allowed: bool
    embedding_allowed: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def load_authorization_record(path: Path) -> BodyIngestionAuthorization:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("authorization record must be a JSON object")
    required = {
        "authorized_by",
        "authorization_scope",
        "risk_acknowledgement",
        "source_review_required",
        "public_repo_body_commit_allowed",
        "live_fetch_allowed",
        "chunking_allowed",
        "embedding_allowed",
    }
    missing = sorted(required.difference(payload))
    if missing:
        raise ValueError(f"authorization record missing fields: {missing}")
    return BodyIngestionAuthorization(
        authorized_by=str(payload["authorized_by"]),
        authorization_scope=str(payload["authorization_scope"]),
        risk_acknowledgement=bool(payload["risk_acknowledgement"]),
        source_review_required=bool(payload["source_review_required"]),
        public_repo_body_commit_allowed=bool(payload["public_repo_body_commit_allowed"]),
        live_fetch_allowed=bool(payload["live_fetch_allowed"]),
        chunking_allowed=bool(payload["chunking_allowed"]),
        embedding_allowed=bool(payload["embedding_allowed"]),
    )


def check_authorization_gate(
    *,
    authorization: BodyIngestionAuthorization | None = None,
    authorization_record_path: Path | None = None,
) -> dict[str, Any]:
    policy_plan = check_policy_plan()
    authorization_errors = _validate_authorization(authorization)
    has_valid_authorization = authorization is not None and not authorization_errors
    decision_gate = check_body_ingestion_decision_gate(explicit_authorization=has_valid_authorization)

    blockers: list[str] = []
    if not policy_plan["ok"]:
        blockers.append("external source body policy plan must pass before authorization")
    if authorization is None:
        blockers.append("explicit authorization record is required before live body ingestion")
    blockers.extend(authorization_errors)
    if not decision_gate["ok"]:
        blockers.append("body-ingestion decision gate prerequisites must pass")

    allowed_to_implement = not blockers and decision_gate["decision"]["allowed_to_implement"] is True
    next_leaf = (
        "external source body ingestion implementation"
        if allowed_to_implement
        else "real-accountant-session RS2/RS3 evidence capture, or external source synthetic parser/chunker dry-run"
    )

    return {
        "ok": bool(policy_plan["ok"] and decision_gate["ok"]),
        "errors": [] if policy_plan["ok"] and decision_gate["ok"] else list(policy_plan["errors"]) + list(decision_gate["errors"]),
        "authorization_present": authorization is not None,
        "authorization_valid": has_valid_authorization,
        "authorization": authorization.to_dict() if authorization else None,
        "authorization_record_path": str(authorization_record_path) if authorization_record_path else None,
        "decision": "proceed" if allowed_to_implement else "defer",
        "allowed_to_implement": allowed_to_implement,
        "blockers": blockers,
        "policy_plan": {
            "ok": policy_plan["ok"],
            "report_path": policy_plan["report_path"],
            "body_policy_path": policy_plan["body_policy_path"],
            "implementation_plan_path": policy_plan["implementation_plan_path"],
        },
        "decision_gate": {
            "ok": decision_gate["ok"],
            "decision": decision_gate["decision"]["decision"],
            "allowed_to_implement": decision_gate["decision"]["allowed_to_implement"],
            "blockers": decision_gate["decision"]["blockers"],
            "report_path": decision_gate["report_path"],
        },
        "report_path": str(REPORT_PATH.relative_to(ROOT)),
        "next_leaf": next_leaf,
    }


def render_report(result: dict[str, Any]) -> str:
    if result["authorization_present"] and result["authorization_valid"] and result["allowed_to_implement"]:
        conclusion = (
            "External source body ingestion can proceed because a valid explicit authorization record is present. "
            "Implementation must still keep body cache/chunks/embeddings local-private and out of public commits."
        )
    elif result["authorization_present"]:
        conclusion = (
            "External source body ingestion remains deferred because the supplied authorization record is not valid. "
            "No live body fetching, chunking, embedding, or indexing is authorized."
        )
    else:
        conclusion = (
            "External source body ingestion remains deferred because no explicit authorization record is present. "
            "The gate is now machine-readable: policy/plan and ESBD1 prerequisites are checked, but live body fetching, "
            "chunking, embedding, and indexing remain blocked."
        )
    lines = [
        "# ESAG1 External Source Body Authorization Gate",
        "",
        "> Scope: explicit authorization gate before any external source body ingestion implementation.",
        "",
        "## 한 줄 결론",
        "",
        conclusion,
        "",
        "## Decision",
        "",
        f"- Decision: {result['decision']}",
        f"- Allowed to implement: {result['allowed_to_implement']}",
        f"- Authorization present: {result['authorization_present']}",
        f"- Authorization valid: {result['authorization_valid']}",
        "",
        "## Blockers",
        "",
    ]
    lines.extend(f"- {blocker}" for blocker in result["blockers"])
    lines.extend([
        "",
        "## Checked Inputs",
        "",
        f"- Policy plan ok: {result['policy_plan']['ok']}",
        f"- Body policy: `{result['policy_plan']['body_policy_path']}`",
        f"- Implementation plan: `{result['policy_plan']['implementation_plan_path']}`",
        f"- Decision gate ok: {result['decision_gate']['ok']}",
        f"- Decision gate blockers: {result['decision_gate']['blockers']}",
        "",
        "## Authorization Contract",
        "",
        "- `authorized_by` must be non-empty.",
        f"- `authorization_scope` must be one of: {sorted(ALLOWED_AUTHORIZATION_SCOPES)}.",
        "- `risk_acknowledgement` must be true.",
        "- `source_review_required` must be true.",
        "- `public_repo_body_commit_allowed` must be false.",
        "- Optional JSON record can be supplied with `--authorization-record <path>`; keep it source-specific and do not include source bodies, credentials, or copied text.",
        "",
        "## Still Not Implemented",
        "",
        "- live external body fetch/crawl",
        "- source body cache",
        "- source-specific chunking",
        "- external body embeddings",
        "- external body index namespace",
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


def write_report(
    *,
    authorization: BodyIngestionAuthorization | None = None,
    authorization_record_path: Path | None = None,
) -> dict[str, Any]:
    result = check_authorization_gate(
        authorization=authorization,
        authorization_record_path=authorization_record_path,
    )
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_report(result), encoding="utf-8")
    return result


def _validate_authorization(authorization: BodyIngestionAuthorization | None) -> list[str]:
    if authorization is None:
        return []

    errors: list[str] = []
    if not authorization.authorized_by.strip():
        errors.append("authorized_by is required")
    if authorization.authorization_scope not in ALLOWED_AUTHORIZATION_SCOPES:
        errors.append(f"authorization_scope must be one of {sorted(ALLOWED_AUTHORIZATION_SCOPES)}")
    if authorization.risk_acknowledgement is not True:
        errors.append("risk_acknowledgement must be true")
    if authorization.source_review_required is not True:
        errors.append("source_review_required must be true")
    if authorization.public_repo_body_commit_allowed is not False:
        errors.append("public_repo_body_commit_allowed must be false")
    live_actions = (
        authorization.live_fetch_allowed,
        authorization.chunking_allowed,
        authorization.embedding_allowed,
    )
    if authorization.authorization_scope == "synthetic_dry_run_only" and any(live_actions):
        errors.append("synthetic_dry_run_only scope must not allow live fetch, chunking, or embedding")
    if authorization.authorization_scope == "source_specific_local_private_body" and not authorization.live_fetch_allowed:
        errors.append("source_specific_local_private_body scope requires live_fetch_allowed")
    return errors


def _authorization_from_args(args: argparse.Namespace) -> BodyIngestionAuthorization | None:
    if args.authorization_record:
        return load_authorization_record(args.authorization_record)
    if not args.authorize_body_ingestion:
        return None
    return BodyIngestionAuthorization(
        authorized_by=args.authorized_by,
        authorization_scope=args.authorization_scope,
        risk_acknowledgement=args.acknowledge_risk,
        source_review_required=args.source_review_required,
        public_repo_body_commit_allowed=args.public_repo_body_commit_allowed,
        live_fetch_allowed=args.live_fetch_allowed,
        chunking_allowed=args.chunking_allowed,
        embedding_allowed=args.embedding_allowed,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run external source body-ingestion authorization gate.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--authorization-record", type=Path)
    parser.add_argument("--authorize-body-ingestion", action="store_true")
    parser.add_argument("--authorized-by", default="")
    parser.add_argument("--authorization-scope", default="synthetic_dry_run_only")
    parser.add_argument("--acknowledge-risk", action="store_true")
    parser.add_argument("--source-review-required", action="store_true")
    parser.add_argument("--public-repo-body-commit-allowed", action="store_true")
    parser.add_argument("--live-fetch-allowed", action="store_true")
    parser.add_argument("--chunking-allowed", action="store_true")
    parser.add_argument("--embedding-allowed", action="store_true")
    args = parser.parse_args()

    try:
        authorization = _authorization_from_args(args)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"authorization_record_error: {exc}")
        raise SystemExit(1) from exc

    result = (
        write_report(
            authorization=authorization,
            authorization_record_path=args.authorization_record,
        )
        if args.write
        else check_authorization_gate(
            authorization=authorization,
            authorization_record_path=args.authorization_record,
        )
    )
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"decision: {result['decision']}")
        print(f"allowed_to_implement: {result['allowed_to_implement']}")
        print(f"authorization_present: {result['authorization_present']}")
        print(f"authorization_valid: {result['authorization_valid']}")
        print(f"blockers: {result['blockers']}")
        print(f"next_leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
