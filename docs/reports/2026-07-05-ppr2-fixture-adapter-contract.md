# PPR2 Realistic Local Fixture Adapter Contract

> Scope: public-safe contract for realistic local fixture parser adapter work.

## 한 줄 결론

The next parser adapter may handle synthetic local fixtures through structured facts, redaction states, and explicit failure states only.

## File Classes

| Class | Source Kind | Extensions | Structured Outputs |
|---|---|---|---|
| lease_contract_fixture | synthetic local fixture | .md, .txt, .json | contract_terms, payment_schedule, lease_term, option_flags |
| trial_balance_fixture | synthetic local fixture | .csv, .json | account_code, account_name, debit, credit, period |
| accounting_policy_fixture | synthetic local fixture | .md, .txt, .json | policy_area, recognition_rule, measurement_rule, disclosure_note |

## Output Schema

| Field | Type |
|---|---|
| fixture_id | string |
| file_class | enum |
| parser_status | parsed | partial | rejected |
| structured_facts | list[public_safe_fact] |
| redactions | list[redaction_status] |
| needs_human_review | boolean |
| retention_state | retained | delete_pending | deleted |

## Redaction Fields

- counterparty_name
- employee_name
- registration_number
- bank_account
- contract_address
- raw_clause_text

## Failure States

| State | Public Action |
|---|---|
| unsupported_file_type | report class and extension only |
| parse_confidence_low | emit structured error and require human review |
| redaction_required | drop raw field and emit redaction status |
| authorization_missing | do not parse; emit authorization-required status |

## Evidence

| ID | Path | Exists |
|---|---|---|
| ppr1_authorization_plan | `docs/reports/2026-07-05-ppr1-authorization-safe-adapter-proof.md` | True |
| local_parser_plan | `docs/reports/2026-07-05-local-parser-real-adapter-implementation-plan.md` | True |
| parser_prototype_close | `docs/reports/2026-07-05-real-local-parser-prototype-close-report.md` | True |

## Checks

| Check | OK |
|---|---|
| all_evidence_exists | True |
| file_classes_defined | True |
| redaction_fields_defined | True |
| failure_states_defined | True |
| raw_payload_not_output | True |
| human_review_flag_present | True |

## Errors

- none

## Next Leaf

- `PPR3_deletion_and_retention_rehearsal`

## Machine Result

```json
{
  "title": "PPR2 Realistic Local Fixture Adapter Contract",
  "ok": true,
  "horizon": "private-parser-realism-hardening",
  "completed_milestone": "PPR2",
  "file_classes": [
    {
      "class_id": "lease_contract_fixture",
      "source_kind": "synthetic local fixture",
      "accepted_extensions": [
        ".md",
        ".txt",
        ".json"
      ],
      "structured_outputs": [
        "contract_terms",
        "payment_schedule",
        "lease_term",
        "option_flags"
      ]
    },
    {
      "class_id": "trial_balance_fixture",
      "source_kind": "synthetic local fixture",
      "accepted_extensions": [
        ".csv",
        ".json"
      ],
      "structured_outputs": [
        "account_code",
        "account_name",
        "debit",
        "credit",
        "period"
      ]
    },
    {
      "class_id": "accounting_policy_fixture",
      "source_kind": "synthetic local fixture",
      "accepted_extensions": [
        ".md",
        ".txt",
        ".json"
      ],
      "structured_outputs": [
        "policy_area",
        "recognition_rule",
        "measurement_rule",
        "disclosure_note"
      ]
    }
  ],
  "output_schema": {
    "fixture_id": "string",
    "file_class": "enum",
    "parser_status": "parsed | partial | rejected",
    "structured_facts": "list[public_safe_fact]",
    "redactions": "list[redaction_status]",
    "needs_human_review": "boolean",
    "retention_state": "retained | delete_pending | deleted"
  },
  "redaction_fields": [
    "counterparty_name",
    "employee_name",
    "registration_number",
    "bank_account",
    "contract_address",
    "raw_clause_text"
  ],
  "failure_states": [
    {
      "state": "unsupported_file_type",
      "public_action": "report class and extension only"
    },
    {
      "state": "parse_confidence_low",
      "public_action": "emit structured error and require human review"
    },
    {
      "state": "redaction_required",
      "public_action": "drop raw field and emit redaction status"
    },
    {
      "state": "authorization_missing",
      "public_action": "do not parse; emit authorization-required status"
    }
  ],
  "evidence": [
    {
      "id": "ppr1_authorization_plan",
      "path": "docs/reports/2026-07-05-ppr1-authorization-safe-adapter-proof.md",
      "exists": true
    },
    {
      "id": "local_parser_plan",
      "path": "docs/reports/2026-07-05-local-parser-real-adapter-implementation-plan.md",
      "exists": true
    },
    {
      "id": "parser_prototype_close",
      "path": "docs/reports/2026-07-05-real-local-parser-prototype-close-report.md",
      "exists": true
    }
  ],
  "checks": {
    "all_evidence_exists": true,
    "file_classes_defined": true,
    "redaction_fields_defined": true,
    "failure_states_defined": true,
    "raw_payload_not_output": true,
    "human_review_flag_present": true
  },
  "errors": [],
  "next_leaf": "PPR3_deletion_and_retention_rehearsal",
  "report_path": "docs/reports/2026-07-05-ppr2-fixture-adapter-contract.md"
}
```
