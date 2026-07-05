# ESB3 Chunking And Retrieval Dry Run

> Scope: synthetic chunking and retrieval dry-run for the selected external source-body connector lane.

## 한 줄 결론

Synthetic chunks can be ranked for retrieval using labels and metadata only; no copied payload is rendered.

## Chunks

| Chunk | Fixture | Locator | Tags | Summary Label | Payload Rendered |
|---|---|---|---|---|---|
| esb3-interpretive-001-c01 | esb2-fixture-interpretive-001 | synthetic://interpretive-accounting-material/esb2-001#c01 | revenue, disclosure | principal_agent_indicator_label | False |
| esb3-interpretive-001-c02 | esb2-fixture-interpretive-001 | synthetic://interpretive-accounting-material/esb2-001#c02 | revenue, variable_consideration | constraint_indicator_label | False |
| esb3-interpretive-001-c03 | esb2-fixture-interpretive-001 | synthetic://interpretive-accounting-material/esb2-001#c03 | disclosure, judgement | disclosure_judgement_label | False |

## Retrieval Results

| Query | Expected | Top Chunk | Score | Payload Rendered |
|---|---|---|---:|---|
| esb3-q-revenue-principal-agent | esb3-interpretive-001-c01 | esb3-interpretive-001-c01 | 1 | False |
| esb3-q-variable-consideration | esb3-interpretive-001-c02 | esb3-interpretive-001-c02 | 1 | False |

## Checks

| Check | OK |
|---|---|
| chunks_present | True |
| all_chunks_public_safe | True |
| retrieval_results_present | True |
| expected_chunks_top_ranked | True |
| no_body_payload_in_results | True |
| next_milestone_named | True |

## Errors

- none

## Next Leaf

- `ESB4_connector_leak_and_policy_gate`

## Machine Result

```json
{
  "title": "ESB3 Chunking And Retrieval Dry Run",
  "ok": true,
  "horizon": "external-source-body-connector-expansion",
  "completed_milestone": "ESB3",
  "chunk_strategy": "semantic_section_stub",
  "chunks": [
    {
      "chunk_id": "esb3-interpretive-001-c01",
      "fixture_id": "esb2-fixture-interpretive-001",
      "locator": "synthetic://interpretive-accounting-material/esb2-001#c01",
      "topic_tags": [
        "revenue",
        "disclosure"
      ],
      "synthetic_summary_label": "principal_agent_indicator_label",
      "retrieval_terms": [
        "revenue",
        "gross_or_net",
        "principal_agent"
      ],
      "contains_copied_payload": false
    },
    {
      "chunk_id": "esb3-interpretive-001-c02",
      "fixture_id": "esb2-fixture-interpretive-001",
      "locator": "synthetic://interpretive-accounting-material/esb2-001#c02",
      "topic_tags": [
        "revenue",
        "variable_consideration"
      ],
      "synthetic_summary_label": "constraint_indicator_label",
      "retrieval_terms": [
        "revenue",
        "variable_consideration",
        "constraint"
      ],
      "contains_copied_payload": false
    },
    {
      "chunk_id": "esb3-interpretive-001-c03",
      "fixture_id": "esb2-fixture-interpretive-001",
      "locator": "synthetic://interpretive-accounting-material/esb2-001#c03",
      "topic_tags": [
        "disclosure",
        "judgement"
      ],
      "synthetic_summary_label": "disclosure_judgement_label",
      "retrieval_terms": [
        "disclosure",
        "judgement",
        "policy"
      ],
      "contains_copied_payload": false
    }
  ],
  "queries": [
    {
      "query_id": "esb3-q-revenue-principal-agent",
      "topic": "revenue principal agent review support",
      "expected_chunk": "esb3-interpretive-001-c01"
    },
    {
      "query_id": "esb3-q-variable-consideration",
      "topic": "variable consideration constraint support",
      "expected_chunk": "esb3-interpretive-001-c02"
    }
  ],
  "retrieval_results": [
    {
      "query_id": "esb3-q-revenue-principal-agent",
      "expected_chunk": "esb3-interpretive-001-c01",
      "top_chunk_id": "esb3-interpretive-001-c01",
      "top_score": 1,
      "top_locator": "synthetic://interpretive-accounting-material/esb2-001#c01",
      "top_summary_label": "principal_agent_indicator_label",
      "payload_rendered": false
    },
    {
      "query_id": "esb3-q-variable-consideration",
      "expected_chunk": "esb3-interpretive-001-c02",
      "top_chunk_id": "esb3-interpretive-001-c02",
      "top_score": 1,
      "top_locator": "synthetic://interpretive-accounting-material/esb2-001#c02",
      "top_summary_label": "constraint_indicator_label",
      "payload_rendered": false
    }
  ],
  "checks": {
    "chunks_present": true,
    "all_chunks_public_safe": true,
    "retrieval_results_present": true,
    "expected_chunks_top_ranked": true,
    "no_body_payload_in_results": true,
    "next_milestone_named": true
  },
  "errors": [],
  "next_leaf": "ESB4_connector_leak_and_policy_gate",
  "report_path": "docs/reports/2026-07-05-esb3-chunking-retrieval-dry-run.md"
}
```
