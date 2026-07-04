# CPU1 Client-Private Upload/Parser Storage Policy

> Scope: storage and deletion contract required before any client-private upload, OCR, or parser UX.

## 한 줄 결론

Client-private upload/parser work is allowed only as a local ephemeral quarantine flow. Public artifacts may contain schema, redacted structured facts, review-pack summaries, and deletion attestation, but never raw files, parsed bodies, OCR text, or embeddings.

## Policy

### Client-Private Upload/Parser Storage Policy - cpu1-local-upload-parser-storage-policy

- Upload storage mode: local_ephemeral_quarantine
- Parser mode: structured_facts_only
- Deletion mode: manual_before_commit
- Raw file persistence allowed: False
- Parsed body persistence allowed: False
- Embedding allowed: False
- Commit allowed: False

## Allowed Public Artifacts

- schema manifest
- redacted structured facts
- redaction checklist result
- review-pack summary
- deletion attestation

## Forbidden Public Artifacts

- raw private file
- parsed private body
- private embedding
- OCR text
- customer identifier
- company identifier
- workpaper payload
- source document excerpt

## Local-Only Paths

- `data/private_uploads/`
- `data/client_private/`
- `tmp/client_private/`

## Required Operator Checks

- verify local-only paths are gitignored before receiving any file
- delete quarantined raw files before close
- record deletion attestation without source body text
- run public-safe gate before committing any derived artifact

## Boundary

- This policy does not implement upload, OCR, or private document parsing.
- This policy only defines the storage and deletion contract that must exist before those features are built.
- Public artifacts may contain schemas, redacted structured facts, and deletion attestations only.

## What This Enables

- A future local upload/parser prototype can be designed without changing public-safe repo boundaries.
- Operators have concrete checks before accepting private files.
- Gap audit can distinguish storage-policy readiness from actual upload/parser implementation.

## Still Not Implemented

- file upload UI
- OCR
- private document parser
- local deletion automation
- private embedding/index namespace

## Next Leaf

real-accountant-session RS2/RS3 evidence capture, or private parser dry-run fixture design

## Machine Result

```json
{
  "ok": true,
  "errors": [],
  "policy": {
    "policy_id": "cpu1-local-upload-parser-storage-policy",
    "upload_storage_mode": "local_ephemeral_quarantine",
    "parser_mode": "structured_facts_only",
    "deletion_mode": "manual_before_commit",
    "allowed_public_artifacts": [
      "schema manifest",
      "redacted structured facts",
      "redaction checklist result",
      "review-pack summary",
      "deletion attestation"
    ],
    "forbidden_public_artifacts": [
      "raw private file",
      "parsed private body",
      "private embedding",
      "OCR text",
      "customer identifier",
      "company identifier",
      "workpaper payload",
      "source document excerpt"
    ],
    "local_only_paths": [
      "data/private_uploads/",
      "data/client_private/",
      "tmp/client_private/"
    ],
    "required_operator_checks": [
      "verify local-only paths are gitignored before receiving any file",
      "delete quarantined raw files before close",
      "record deletion attestation without source body text",
      "run public-safe gate before committing any derived artifact"
    ],
    "raw_file_persistence_allowed": false,
    "parsed_body_persistence_allowed": false,
    "embedding_allowed": false,
    "commit_allowed": false
  },
  "report_path": "docs\\reports\\2026-07-05-cpu1-client-private-upload-storage-policy.md",
  "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or private parser dry-run fixture design"
}
```
