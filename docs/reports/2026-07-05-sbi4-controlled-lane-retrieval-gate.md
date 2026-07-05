# SBI4 Controlled Lane Retrieval Gate

> Scope: prove synthetic controlled chunks are discoverable only as supporting interpretation.

## 한 줄 결론

SBI4 retrieves the synthetic interpretive chunk for a lease/payment query while preserving K-IFRS primary evidence. Controlled chunks are discoverable as supporting interpretation only.

## Gate Result

- ok: True
- query: lease payment pattern supporting interpretation
- retrieved count: 3
- primary evidence preserved: True

## Retrieved Chunks

| Chunk | Score | Lane | Role | Authority | Text |
|---|---|---|---|---|---|
| `sbi3-kasb-fss-interpretive-synthetic-chunk-2` | 5 | `controlled_supporting_interpretation` | `supporting_interpretation` | `interpretive` | Lease guidance summary: confirm control of use, term evidence, and payment pattern. |
| `sbi3-kasb-fss-interpretive-synthetic-chunk-1` | 4 | `controlled_supporting_interpretation` | `supporting_interpretation` | `interpretive` | Revenue guidance summary: identify the contract, promised goods, and timing pattern. |
| `sbi3-kasb-fss-interpretive-synthetic-chunk-3` | 3 | `controlled_supporting_interpretation` | `supporting_interpretation` | `interpretive` | This synthetic note supports interpretation only and does not replace K-IFRS paragraph evidence. |

## Boundary

- Controlled chunks are not K-IFRS primary evidence.
- This gate does not change the default retriever.
- This gate does not fetch, store, or embed external body text.

## Errors

- none

## Next Leaf

SBI5_controlled_lane_close_gate

## Machine Result

```json
{
  "title": "SBI4 Controlled Lane Retrieval Gate",
  "ok": true,
  "query": "lease payment pattern supporting interpretation",
  "retrieved": [
    {
      "chunk_id": "sbi3-kasb-fss-interpretive-synthetic-chunk-2",
      "source_id": "kasb-interpretation-material",
      "section_index": 2,
      "text": "Lease guidance summary: confirm control of use, term evidence, and payment pattern.",
      "citation_role": "supporting_interpretation",
      "authority_level": "interpretive",
      "topic_tags": [
        "revenue",
        "lease",
        "supporting interpretation"
      ],
      "score": 5,
      "retrieval_lane": "controlled_supporting_interpretation",
      "primary_evidence_replacement_allowed": false
    },
    {
      "chunk_id": "sbi3-kasb-fss-interpretive-synthetic-chunk-1",
      "source_id": "kasb-interpretation-material",
      "section_index": 1,
      "text": "Revenue guidance summary: identify the contract, promised goods, and timing pattern.",
      "citation_role": "supporting_interpretation",
      "authority_level": "interpretive",
      "topic_tags": [
        "revenue",
        "lease",
        "supporting interpretation"
      ],
      "score": 4,
      "retrieval_lane": "controlled_supporting_interpretation",
      "primary_evidence_replacement_allowed": false
    },
    {
      "chunk_id": "sbi3-kasb-fss-interpretive-synthetic-chunk-3",
      "source_id": "kasb-interpretation-material",
      "section_index": 3,
      "text": "This synthetic note supports interpretation only and does not replace K-IFRS paragraph evidence.",
      "citation_role": "supporting_interpretation",
      "authority_level": "interpretive",
      "topic_tags": [
        "revenue",
        "lease",
        "supporting interpretation"
      ],
      "score": 3,
      "retrieval_lane": "controlled_supporting_interpretation",
      "primary_evidence_replacement_allowed": false
    }
  ],
  "retrieved_count": 3,
  "primary_evidence_preserved": true,
  "errors": [],
  "completed_milestone": "SBI4",
  "next_leaf": "SBI5_controlled_lane_close_gate",
  "report_path": "docs/reports/2026-07-05-sbi4-controlled-lane-retrieval-gate.md"
}
```
