from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs.feedback import (  # noqa: E402
    ClientPrivateUploadStoragePolicy,
    render_client_private_upload_storage_policy,
    validate_client_private_upload_storage_policy,
)


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-cpu1-client-private-upload-storage-policy.md"


def default_policy() -> ClientPrivateUploadStoragePolicy:
    return ClientPrivateUploadStoragePolicy(
        policy_id="cpu1-local-upload-parser-storage-policy",
        upload_storage_mode="local_ephemeral_quarantine",
        parser_mode="structured_facts_only",
        deletion_mode="manual_before_commit",
        allowed_public_artifacts=[
            "schema manifest",
            "redacted structured facts",
            "redaction checklist result",
            "review-pack summary",
            "deletion attestation",
        ],
        forbidden_public_artifacts=[
            "raw private file",
            "parsed private body",
            "private embedding",
            "OCR text",
            "customer identifier",
            "company identifier",
            "workpaper payload",
            "source document excerpt",
        ],
        local_only_paths=[
            "data/private_uploads/",
            "data/client_private/",
            "tmp/client_private/",
        ],
        required_operator_checks=[
            "verify local-only paths are gitignored before receiving any file",
            "delete quarantined raw files before close",
            "record deletion attestation without source body text",
            "run public-safe gate before committing any derived artifact",
        ],
        raw_file_persistence_allowed=False,
        parsed_body_persistence_allowed=False,
        embedding_allowed=False,
        commit_allowed=False,
    )


def check_upload_storage_policy() -> dict[str, object]:
    policy = default_policy()
    issues = validate_client_private_upload_storage_policy(policy)
    return {
        "ok": not issues,
        "errors": [f"{issue.path}: {issue.message}" for issue in issues],
        "policy": policy.to_dict(),
        "report_path": str(REPORT_PATH.relative_to(ROOT)),
        "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or private parser dry-run fixture design",
    }


def render_report(result: dict[str, object]) -> str:
    policy = ClientPrivateUploadStoragePolicy(**result["policy"])
    policy_markdown = render_client_private_upload_storage_policy(policy).rstrip()
    policy_markdown = policy_markdown.replace("# Client-Private Upload/Parser Storage Policy", "### Client-Private Upload/Parser Storage Policy", 1)
    lines = [
        "# CPU1 Client-Private Upload/Parser Storage Policy",
        "",
        "> Scope: storage and deletion contract required before any client-private upload, OCR, or parser UX.",
        "",
        "## 한 줄 결론",
        "",
        "Client-private upload/parser work is allowed only as a local ephemeral quarantine flow. Public artifacts may contain schema, redacted structured facts, review-pack summaries, and deletion attestation, but never raw files, parsed bodies, OCR text, or embeddings.",
        "",
        "## Policy",
        "",
        policy_markdown,
        "",
        "## What This Enables",
        "",
        "- A future local upload/parser prototype can be designed without changing public-safe repo boundaries.",
        "- Operators have concrete checks before accepting private files.",
        "- Gap audit can distinguish storage-policy readiness from actual upload/parser implementation.",
        "",
        "## Still Not Implemented",
        "",
        "- file upload UI",
        "- OCR",
        "- private document parser",
        "- local deletion automation",
        "- private embedding/index namespace",
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
    return "\n".join(lines) + "\n"


def write_report() -> dict[str, object]:
    result = check_upload_storage_policy()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_report(result), encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Check client-private upload/parser storage policy.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = write_report() if args.write else check_upload_storage_policy()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"upload_storage_mode: {result['policy']['upload_storage_mode']}")
        print(f"parser_mode: {result['policy']['parser_mode']}")
        print(f"deletion_mode: {result['policy']['deletion_mode']}")
        print(f"next_leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
