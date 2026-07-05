# CPL1 Client-Private Local Parser Close Gate

> Scope: close the public-safe readiness path for future local client-private parser work.

## 한 줄 결론

The client-private local parser readiness path is now closed at the contract level: local-only intake, redaction, routing, storage policy, synthetic parser output, and deletion attestation all pass. This still does not implement real upload, OCR, parsing, deletion automation, or private embeddings.

## Check Results

| Check | Status |
|---|---|
| local_only_close_gate | ok |
| upload_storage_policy | ok |
| parser_dry_run_fixture | ok |
| deletion_attestation | ok |
| quality_preflight | ok |

## Closed Scope

- local-only client-private control record
- public-safe redaction and review-pack routing
- upload/parser storage policy
- synthetic parser dry-run output contract
- local deletion attestation contract

## Still Not Implemented

- real file upload UI
- OCR
- real private document parser
- real file deletion automation
- private embedding/index namespace

## What This Means

- The next parser work can start as a controlled local prototype instead of reopening safety policy decisions.
- Public reports can prove readiness without storing source bodies or identifiers.
- The gap audit can now move from policy/fixture/attestation readiness to prototype implementation or actual reviewer evidence.

## Next Leaf

real-accountant-session RS2/RS3 evidence capture, or first local parser prototype spike

## Machine Result

```json
{
  "ok": true,
  "errors": [],
  "checks": {
    "local_only_close_gate": {
      "ok": true,
      "errors": [],
      "checks": {
        "contract": {
          "ok": true,
          "errors": [],
          "good_issue_count": 0,
          "bad_issue_paths": [
            "structured_facts.raw_contract"
          ],
          "report_exists": true
        },
        "redaction": {
          "ok": true,
          "errors": [],
          "summary_keys": [
            "allowed_output_level",
            "case_id",
            "document_type",
            "redaction_status",
            "reviewer_original_document_check",
            "structured_fact_keys",
            "structured_facts"
          ],
          "rejected_unreviewed": true,
          "report_exists": true
        },
        "routing": {
          "ok": true,
          "errors": [],
          "route_1116": {
            "case_id": "local-case-routing-check",
            "domain": "KIFRS1116",
            "route": "kifrs1116_review_pack",
            "status": "candidate",
            "reason": "minimum structured facts are present for a review-pack draft candidate",
            "missing_facts": []
          },
          "route_1109": {
            "case_id": "local-case-routing-check",
            "domain": "KIFRS1109",
            "route": "kifrs1109_review_pack",
            "status": "needs_more_facts",
            "reason": "required structured facts are missing",
            "missing_facts": [
              "instrument_type",
              "business_model",
              "cash_flow_terms"
            ]
          },
          "route_blocked": {
            "case_id": "local-case-routing-check",
            "domain": "KIFRS1116",
            "route": "redaction_gate",
            "status": "blocked",
            "reason": "review-pack routing requires allowed_output_level review_pack_summary",
            "missing_facts": []
          },
          "report_exists": true
        },
        "readiness": {
          "ok": true,
          "errors": [],
          "missing_artifacts": [],
          "missing_report_terms": [],
          "missing_next_steps": []
        }
      },
      "quality_preflight": {
        "ran": false
      },
      "report_path": "docs\\reports\\2026-07-05-cp4-client-private-close-report.md",
      "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or live external source/retriever validation"
    },
    "upload_storage_policy": {
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
    },
    "parser_dry_run_fixture": {
      "ok": true,
      "errors": [],
      "policy_id": "cpu1-local-upload-parser-storage-policy",
      "fixture": {
        "fixture_id": "pdf1-synthetic-lease-contract-dry-run",
        "parser_mode": "structured_facts_only",
        "document_type": "contract",
        "source_stub": "local-private://dry-run/synthetic-lease-contract",
        "expected_domain": "KIFRS1116",
        "structured_facts": {
          "party": "lessee",
          "lease_term": "5 years",
          "payment_schedule": "monthly fixed payments"
        },
        "allowed_output_level": "review_pack_summary",
        "redaction_status": "reviewed_public_safe",
        "reviewer_original_document_check": true,
        "deletion_attestation": "synthetic dry-run raw file deleted before report write"
      },
      "redacted_summary": {
        "case_id": "pdf1-synthetic-lease-contract-dry-run",
        "document_type": "contract",
        "redaction_status": "reviewed_public_safe",
        "allowed_output_level": "review_pack_summary",
        "reviewer_original_document_check": true,
        "structured_fact_keys": [
          "lease_term",
          "party",
          "payment_schedule"
        ],
        "structured_facts": {
          "lease_term": "5 years",
          "party": "lessee",
          "payment_schedule": "monthly fixed payments"
        }
      },
      "route": {
        "case_id": "pdf1-synthetic-lease-contract-dry-run",
        "domain": "KIFRS1116",
        "route": "kifrs1116_review_pack",
        "status": "candidate",
        "reason": "minimum structured facts are present for a review-pack draft candidate",
        "missing_facts": []
      },
      "report_path": "docs\\reports\\2026-07-05-pdf1-private-parser-dry-run-fixture.md",
      "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or local deletion attestation gate"
    },
    "deletion_attestation": {
      "ok": true,
      "errors": [],
      "policy_id": "cpu1-local-upload-parser-storage-policy",
      "fixture_id": "pdf1-synthetic-lease-contract-dry-run",
      "attestation": {
        "attestation_id": "lda1-synthetic-lease-contract-deletion-attestation",
        "fixture_id": "pdf1-synthetic-lease-contract-dry-run",
        "source_stub": "local-private://dry-run/synthetic-lease-contract",
        "deletion_status": "deleted",
        "deletion_mode": "manual_before_commit",
        "operator_check": "operator verified gitignored local-only paths and checked the synthetic dry-run raw file was deleted before report write",
        "allowed_public_artifact": "deletion attestation",
        "deleted_before_report_write": true,
        "raw_file_present": false,
        "parsed_body_present": false,
        "ocr_text_present": false,
        "embedding_present": false
      },
      "report_path": "docs\\reports\\2026-07-05-lda1-local-deletion-attestation-gate.md",
      "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or client-private local parser close gate"
    }
  },
  "quality_preflight": {
    "ran": true,
    "returncode": 0,
    "stdout": "{\n  \"ok\": true,\n  \"public_safe\": true,\n  \"protected_assets_required\": false,\n  \"results\": [\n    {\n      \"name\": \"focused_pytest\",\n      \"cmd\": [\n        \"C:\\\\Users\\\\yusun\\\\AppData\\\\Local\\\\Programs\\\\Python\\\\Python312\\\\python.exe\",\n        \"-m\",\n        \"pytest\",\n        \"tests/test_eval_gates.py\",\n        \"tests/test_authority.py\",\n        \"tests/test_authority_source_pack.py\",\n        \"tests/test_user_note_v2_runtime.py\",\n        \"tests/test_user_notes.py\",\n        \"tests/test_user_note_v2_migration.py\",\n        \"-q\"\n      ],\n      \"returncode\": 0,\n      \"stdout\": \"..................                                                       [100%]\\n============================== warnings summary ===============================\\n..\\\\..\\\\AppData\\\\Local\\\\Programs\\\\Python\\\\Python312\\\\Lib\\\\site-packages\\\\_pytest\\\\cacheprovider.py:475\\n  C:\\\\Users\\\\yusun\\\\AppData\\\\Local\\\\Programs\\\\Python\\\\Python312\\\\Lib\\\\site-packages\\\\_pytest\\\\cacheprovider.py:475: PytestCacheWarning: could not create cache path C:\\\\Users\\\\yusun\\\\projects\\\\kifrs-rag\\\\.pytest_cache\\\\v\\\\cache\\\\nodeids: [WinError 5] 액세스가 거부되었습니다: 'C:\\\\\\\\Users\\\\\\\\yusun\\\\\\\\projects\\\\\\\\kifrs-rag\\\\\\\\.pytest_cache\\\\\\\\v\\\\\\\\cache'\\n    config.cache.set(\\\"cache/nodeids\\\", sorted(self.cached_nodeids))\\n\\n-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html\\n18 passed, 1 warning in 0.33s\",\n      \"stderr\": \"\"\n    },\n    {\n      \"name\": \"local_rag_threshold_gate\",\n      \"cmd\": [\n        \"C:\\\\Users\\\\yusun\\\\AppData\\\\Local\\\\Programs\\\\Python\\\\Python312\\\\python.exe\",\n        \"scripts/eval_quality_gate.py\",\n        \"--runner\",\n        \"local-rag\",\n        \"--only\",\n        \"Q019\",\n        \"Q020\",\n        \"Q021\",\n        \"Q022\",\n        \"Q023\",\n        \"--min-composite\",\n        \"0.6\",\n        \"--min-cite\",\n        \"0.45\",\n        \"--format\",\n        \"text\"\n      ],\n      \"returncode\": 0,\n      \"stdout\": \"ok: True\\nmean_composite: 0.921\\nmean_cite: 0.763\\nmean_global_rules: 1.0\\nfailing_items: 0\",\n      \"stderr\": \"\"\n    },\n    {\n      \"name\": \"authority_registry\",\n      \"cmd\": [\n        \"C:\\\\Users\\\\yusun\\\\AppData\\\\Local\\\\Programs\\\\Python\\\\Python312\\\\python.exe\",\n        \"scripts/validate_authority_sources.py\"\n      ],\n      \"returncode\": 0,\n      \"stdout\": \"{\\n  \\\"ok\\\": true,\\n  \\\"errors\\\": [],\\n  \\\"total\\\": 7\\n}\",\n      \"stderr\": \"\"\n    },\n    {\n      \"name\": \"authority_source_pack\",\n      \"cmd\": [\n        \"C:\\\\Users\\\\yusun\\\\AppData\\\\Local\\\\Programs\\\\Python\\\\Python312\\\\python.exe\",\n        \"scripts/validate_authority_source_pack.py\"\n      ],\n      \"returncode\": 0,\n      \"stdout\": \"{\\n  \\\"ok\\\": true,\\n  \\\"errors\\\": [],\\n  \\\"total\\\": 7\\n}\",\n      \"stderr\": \"\"\n    },\n    {\n      \"name\": \"user_note_v2_audit\",\n      \"cmd\": [\n        \"C:\\\\Users\\\\yusun\\\\AppData\\\\Local\\\\Programs\\\\Python\\\\Python312\\\\python.exe\",\n        \"scripts/audit_user_notes.py\",\n        \"--source\",\n        \"v2\",\n        \"--format\",\n        \"json\"\n      ],\n      \"returncode\": 0,\n      \"stdout\": \"{\\n  \\\"total\\\": 20,\\n  \\\"ok\\\": true,\\n  \\\"missing_required\\\": [],\\n  \\\"invalid_type\\\": [],\\n  \\\"dead_anchor\\\": [],\\n  \\\"duplicate_trigger\\\": [],\\n  \\\"conflicting_trigger\\\": [],\\n  \\\"source\\\": \\\"v2\\\"\\n}\",\n      \"stderr\": \"\"\n    }\n  ]\n}\n",
    "stderr": "",
    "ok": true,
    "public_safe": true
  },
  "report_path": "docs\\reports\\2026-07-05-cpl1-client-private-local-parser-close-gate.md",
  "closed_scope": [
    "local-only client-private control record",
    "public-safe redaction and review-pack routing",
    "upload/parser storage policy",
    "synthetic parser dry-run output contract",
    "local deletion attestation contract"
  ],
  "not_implemented": [
    "real file upload UI",
    "OCR",
    "real private document parser",
    "real file deletion automation",
    "private embedding/index namespace"
  ],
  "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or first local parser prototype spike"
}
```
