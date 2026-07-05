# SBI3 Synthetic Body Parser And Chunker

> Scope: synthetic-only parser/chunker dry-run for the selected interpretive lane.

## 한 줄 결론

SBI3 turns a short synthetic interpretive fixture into public-safe chunks with supporting-interpretation citation role. No protected external text, live fetch, OCR, embedding, or body cache is created.

## Fixture

- fixture id: `sbi3-kasb-fss-interpretive-synthetic`
- source id: `kasb-interpretation-material`
- title: Synthetic revenue and lease interpretation note
- issuer: synthetic KASB/FSS-style source
- topic tags: revenue, lease, supporting interpretation

## Chunks

| Chunk | Source | Role | Authority | Text |
|---|---|---|---|---|
| `sbi3-kasb-fss-interpretive-synthetic-chunk-1` | `kasb-interpretation-material` | `supporting_interpretation` | `interpretive` | Revenue guidance summary: identify the contract, promised goods, and timing pattern. |
| `sbi3-kasb-fss-interpretive-synthetic-chunk-2` | `kasb-interpretation-material` | `supporting_interpretation` | `interpretive` | Lease guidance summary: confirm control of use, term evidence, and payment pattern. |
| `sbi3-kasb-fss-interpretive-synthetic-chunk-3` | `kasb-interpretation-material` | `supporting_interpretation` | `interpretive` | This synthetic note supports interpretation only and does not replace K-IFRS paragraph evidence. |

## Errors

- none

## Boundary

- This is synthetic-only parser/chunker evidence.
- It does not fetch, copy, cache, OCR, embed, or index external body text.
- K-IFRS paragraph evidence remains primary.

## Next Leaf

SBI4_controlled_lane_retrieval_gate

## Machine Result

```json
{
  "title": "SBI3 Synthetic Body Parser And Chunker",
  "ok": true,
  "fixture": {
    "fixture_id": "sbi3-kasb-fss-interpretive-synthetic",
    "source_id": "kasb-interpretation-material",
    "title": "Synthetic revenue and lease interpretation note",
    "issuer": "synthetic KASB/FSS-style source",
    "topic_tags": [
      "revenue",
      "lease",
      "supporting interpretation"
    ],
    "synthetic_body": "Revenue guidance summary: identify the contract, promised goods, and timing pattern. Lease guidance summary: confirm control of use, term evidence, and payment pattern. This synthetic note supports interpretation only and does not replace K-IFRS paragraph evidence."
  },
  "chunks": [
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
      ]
    },
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
      ]
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
      ]
    }
  ],
  "chunk_count": 3,
  "errors": [],
  "completed_milestone": "SBI3",
  "next_leaf": "SBI4_controlled_lane_retrieval_gate",
  "report_path": "docs/reports/2026-07-05-sbi3-synthetic-body-parser-chunker.md"
}
```
