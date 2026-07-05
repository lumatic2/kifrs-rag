# ESPP1 External Source Body Policy Plan

> Scope: policy and implementation-plan prerequisite for ESBD1.

## 한 줄 결론

External body ingestion still remains blocked, but the missing policy and implementation-plan artifacts now exist. The only remaining implementation blocker should be explicit user authorization plus any source-specific review required by the next gate.

## Outputs

- Body policy: `docs\reports\2026-07-05-external-source-body-storage-policy.md`
- Implementation plan: `docs\reports\2026-07-05-external-source-body-ingestion-plan.md`

## Validation

- ok: True
- errors: []

## Boundary

- This does not fetch, cache, chunk, embed, or index any external source body.
- This does not authorize live body ingestion.
- This preserves public-safe metadata-only repo boundaries.

## Next Leaf

real-accountant-session RS2/RS3 evidence capture, or external source body-ingestion authorization gate

## Machine Result

```json
{
  "ok": true,
  "errors": [],
  "policy_plan": {
    "policy_id": "espp1-external-source-body-policy-plan",
    "source_classes": [
      "interpretive_accounting_material",
      "law_regulation",
      "primary_audit_standard",
      "supporting_material"
    ],
    "body_storage_mode": "local_private_body_only_after_source_review",
    "public_artifact_rule": "public repo may store metadata, locators, schema, tests, aggregate metrics, and author-written notes only",
    "local_artifact_rule": "body cache, chunks, and embeddings may exist only in gitignored local/private paths after source-specific review",
    "required_source_checks": [
      "record publisher and canonical locator",
      "check robots/terms/license constraints for the exact source",
      "classify authority role before retrieval use",
      "choose source-specific chunk strategy before storing any chunk",
      "document deletion/reindex command before first local cache write"
    ],
    "required_operator_checks": [
      "run metadata-only live validation before source-specific review",
      "verify target cache/index paths are gitignored",
      "run forbidden-field scan before committing any report or manifest",
      "keep K-IFRS primary evidence priority above external body text",
      "record explicit user authorization before live body ingestion"
    ],
    "implementation_steps": [
      "source-specific policy record",
      "local cache path contract",
      "parser/chunker dry-run with synthetic text",
      "forbidden-field regression tests",
      "explicit authorization gate"
    ],
    "proceed_gate_requirements": [
      "source manifest ok",
      "evidence manifest ok",
      "live landing validation report present",
      "external source body storage policy present",
      "external source body ingestion implementation plan present",
      "explicit user authorization present"
    ],
    "forbidden_public_fields": [
      "api_key",
      "body",
      "content",
      "credential",
      "embedding",
      "excerpt",
      "full_text",
      "pdf_bytes",
      "quote",
      "raw_xml",
      "source_body",
      "text",
      "token",
      "xbrl_dump"
    ],
    "body_fetching_allowed_by_this_plan": false,
    "chunking_allowed_by_this_plan": false,
    "embedding_allowed_by_this_plan": false,
    "commit_allowed_by_this_plan": false
  },
  "body_policy_path": "docs\\reports\\2026-07-05-external-source-body-storage-policy.md",
  "implementation_plan_path": "docs\\reports\\2026-07-05-external-source-body-ingestion-plan.md",
  "report_path": "docs\\reports\\2026-07-05-espp1-external-source-body-policy-plan.md",
  "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or external source body-ingestion authorization gate"
}
```
