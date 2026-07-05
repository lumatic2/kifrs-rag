# ESB2 Synthetic Source-Body Fixture Contract

> Scope: synthetic fixture and parser/chunker schema for the selected ESB connector lane.

## 한 줄 결론

The selected interpretive connector now has a synthetic fixture contract and parser/chunker output schema; public artifacts still contain labels, locators, policy status, and retrieval metadata only.

## Fixture Input Schema

| Field | Contract |
|---|---|
| `fixture_id` | string, stable synthetic fixture id |
| `source_class` | interpretive_accounting_material |
| `authority_role` | supporting_interpretive_evidence |
| `publisher_class` | regulator_or_standard_setter |
| `canonical_locator` | string, public locator or invented local locator |
| `policy_status` | synthetic_dry_run_only |
| `synthetic_body_label` | label only; no copied third-party body payload |
| `topic_tags` | ['revenue', 'lease', 'financial_instrument', 'disclosure'] |

## Parser Output Schema

| Field | Contract |
|---|---|
| `record_id` | string |
| `source_class` | string |
| `authority_role` | string |
| `canonical_locator` | string |
| `topic_tags` | list[string] |
| `assertion_labels` | list[string] |
| `chunk_strategy` | semantic_section_stub |
| `chunk_count` | integer |
| `policy_status` | synthetic_only |

## Chunk Output Schema

| Field | Contract |
|---|---|
| `chunk_id` | string |
| `fixture_id` | string |
| `locator` | string |
| `topic_tags` | list[string] |
| `synthetic_summary_label` | string |
| `retrieval_terms` | list[string] |
| `contains_copied_body_payload` | False |

## Sample Fixture

| Field | Value |
|---|---|
| `fixture_id` | esb2-fixture-interpretive-001 |
| `source_class` | interpretive_accounting_material |
| `authority_role` | supporting_interpretive_evidence |
| `publisher_class` | regulator_or_standard_setter |
| `canonical_locator` | synthetic://interpretive-accounting-material/esb2-001 |
| `policy_status` | synthetic_dry_run_only |
| `synthetic_body_label` | author_written_placeholder_label_only |
| `topic_tags` | ['revenue', 'disclosure'] |

## Public-Safety Boundary

- forbidden public state count: 6
- fixture report stores labels and schemas only
- live fetching, real body caching, chunking, and embedding remain outside ESB2

## Checks

| Check | OK |
|---|---|
| selected_lane_matches_ESB1 | True |
| fixture_has_no_copied_payload | True |
| parser_output_schema_present | True |
| chunk_output_schema_present | True |
| chunk_contract_blocks_copied_payload | True |
| forbidden_public_states_present | True |
| next_milestone_named | True |

## Errors

- none

## Next Leaf

- `ESB3_chunking_and_retrieval_dry_run`

## Machine Result

```json
{
  "title": "ESB2 Synthetic Source-Body Fixture Contract",
  "ok": true,
  "horizon": "external-source-body-connector-expansion",
  "completed_milestone": "ESB2",
  "selected_source_class": "interpretive_accounting_material",
  "fixture_input_schema": {
    "fixture_id": "string, stable synthetic fixture id",
    "source_class": "interpretive_accounting_material",
    "authority_role": "supporting_interpretive_evidence",
    "publisher_class": "regulator_or_standard_setter",
    "canonical_locator": "string, public locator or invented local locator",
    "policy_status": "synthetic_dry_run_only",
    "synthetic_body_label": "label only; no copied third-party body payload",
    "topic_tags": [
      "revenue",
      "lease",
      "financial_instrument",
      "disclosure"
    ]
  },
  "parser_output_schema": {
    "record_id": "string",
    "source_class": "string",
    "authority_role": "string",
    "canonical_locator": "string",
    "topic_tags": "list[string]",
    "assertion_labels": "list[string]",
    "chunk_strategy": "semantic_section_stub",
    "chunk_count": "integer",
    "policy_status": "synthetic_only"
  },
  "chunk_output_schema": {
    "chunk_id": "string",
    "fixture_id": "string",
    "locator": "string",
    "topic_tags": "list[string]",
    "synthetic_summary_label": "string",
    "retrieval_terms": "list[string]",
    "contains_copied_body_payload": false
  },
  "sample_fixture": {
    "fixture_id": "esb2-fixture-interpretive-001",
    "source_class": "interpretive_accounting_material",
    "authority_role": "supporting_interpretive_evidence",
    "publisher_class": "regulator_or_standard_setter",
    "canonical_locator": "synthetic://interpretive-accounting-material/esb2-001",
    "policy_status": "synthetic_dry_run_only",
    "synthetic_body_label": "author_written_placeholder_label_only",
    "topic_tags": [
      "revenue",
      "disclosure"
    ]
  },
  "forbidden_public_state_count": 6,
  "checks": {
    "selected_lane_matches_ESB1": true,
    "fixture_has_no_copied_payload": true,
    "parser_output_schema_present": true,
    "chunk_output_schema_present": true,
    "chunk_contract_blocks_copied_payload": true,
    "forbidden_public_states_present": true,
    "next_milestone_named": true
  },
  "errors": [],
  "next_leaf": "ESB3_chunking_and_retrieval_dry_run",
  "report_path": "docs/reports/2026-07-05-esb2-source-body-fixture-contract.md"
}
```
