# SBI2 Source Body Policy Record

> Scope: machine-readable policy for the selected controlled interpretive source lane.

## 한 줄 결론

SBI2 fixes the selected interpretive lane as synthetic-body-only, supporting-interpretation evidence. It cannot live-fetch, embed, commit external body text, or override K-IFRS primary evidence.

## Policy

- policy id: `sbi2-interpretive-synthetic-policy`
- source class: `interpretive_accounting_material`
- source ids: kasb-interpretation-material, fss-accounting-inquiry
- storage mode: `synthetic_body_only`
- citation role: `supporting_interpretation`
- authority level: `interpretive`
- chunking strategy: `synthetic_short_sections`
- retention policy: `public_synthetic_fixture_only`

## Allowed Fields

- source_id
- title
- issuer
- publication_date
- url_or_locator
- topic_tags
- synthetic_body
- citation_role
- authority_level

## Forbidden Fields

- copied external document text
- full article text
- PDF body cache
- embedding dump
- API secret
- client-private payload

## Safety Flags

- primary evidence override allowed: False
- live fetch allowed: False
- embedding allowed: False
- public repo body commit allowed: False

## Errors

- none

## Next Leaf

SBI3_synthetic_parser_chunker

## Machine Result

```json
{
  "title": "SBI2 Source Policy Record",
  "ok": true,
  "policy": {
    "policy_id": "sbi2-interpretive-synthetic-policy",
    "source_class": "interpretive_accounting_material",
    "source_ids": [
      "kasb-interpretation-material",
      "fss-accounting-inquiry"
    ],
    "storage_mode": "synthetic_body_only",
    "citation_role": "supporting_interpretation",
    "authority_level": "interpretive",
    "chunking_strategy": "synthetic_short_sections",
    "retention_policy": "public_synthetic_fixture_only",
    "allowed_fields": [
      "source_id",
      "title",
      "issuer",
      "publication_date",
      "url_or_locator",
      "topic_tags",
      "synthetic_body",
      "citation_role",
      "authority_level"
    ],
    "forbidden_fields": [
      "copied external document text",
      "full article text",
      "PDF body cache",
      "embedding dump",
      "API secret",
      "client-private payload"
    ],
    "primary_evidence_override_allowed": false,
    "live_fetch_allowed": false,
    "embedding_allowed": false,
    "public_repo_body_commit_allowed": false
  },
  "errors": [],
  "completed_milestone": "SBI2",
  "next_leaf": "SBI3_synthetic_parser_chunker",
  "report_path": "docs/reports/2026-07-05-sbi2-source-body-policy-record.md"
}
```
