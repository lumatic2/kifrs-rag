# RR3 Retrieval and Citation Diagnostics

> Scope: public-safe bucket-level retrieval/citation comparison between default and opt-in K-IFRS retrievers.

## 한 줄 결론

`ifrs1109_classification_hybrid` improves recall@20 from 0.887 to 1.000; target top-20 required-citation misses: 0.

## Retrieval Aggregate

| Retriever | recall@1 | recall@3 | recall@5 | recall@10 | recall@20 | MRR | nDCG@10 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `hybrid` | 0.197 | 0.387 | 0.547 | 0.713 | 0.887 | 0.464 | 0.482 |
| `ifrs1109_classification_hybrid` | 0.233 | 0.397 | 0.563 | 0.773 | 1.000 | 0.518 | 0.528 |

## Required-Citation Rank Buckets

| Retriever | hit@5 | hit@10 | hit@20 | beyond@20 | absent |
|---|---:|---:|---:|---:|---:|
| `hybrid` | 45 | 14 | 14 | 0 | 9 |
| `ifrs1109_classification_hybrid` | 47 | 18 | 17 | 0 | 0 |

## Bucket Diagnostics

| Eval Bucket | Citations | Recovered | Still Absent | Target Worse | Target Hit@20 |
|---|---:|---:|---:|---:|---:|
| direct_standard_lookup | 5 | 0 | 0 | 0 | 5 |
| disclosure_question | 6 | 5 | 0 | 0 | 6 |
| judgment_paragraph_combination | 80 | 15 | 0 | 2 | 80 |
| term_bridge_or_exam_convention_dependent | 43 | 6 | 0 | 0 | 43 |
| workflow_seed_question | 24 | 3 | 0 | 1 | 24 |

## Failure Taxonomy

- rank_improved: 6
- rank_worse: 2
- recovered_from_absent: 9
- target_items_with_misses: 0
- unchanged: 65

## Item Summary

| ID | Buckets | Baseline Misses | Target Misses | Best Target Bucket |
|---|---|---:|---:|---|
| Q001 | judgment_paragraph_combination | 1 | 0 | hit@5 |
| Q002 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent | 0 | 0 | hit@5 |
| Q003 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent | 0 | 0 | hit@10 |
| Q004 | disclosure_question, judgment_paragraph_combination | 1 | 0 | hit@5 |
| Q005 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent, workflow_seed_question | 0 | 0 | hit@5 |
| Q006 | disclosure_question, judgment_paragraph_combination, workflow_seed_question | 1 | 0 | hit@5 |
| Q007 | judgment_paragraph_combination | 0 | 0 | hit@5 |
| Q008 | judgment_paragraph_combination, workflow_seed_question | 1 | 0 | hit@5 |
| Q009 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent, workflow_seed_question | 0 | 0 | hit@5 |
| Q010 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent, workflow_seed_question | 0 | 0 | hit@5 |
| Q011 | direct_standard_lookup, term_bridge_or_exam_convention_dependent | 0 | 0 | hit@5 |
| Q012 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent | 0 | 0 | hit@5 |
| Q013 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent | 1 | 0 | hit@5 |
| Q014 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent | 0 | 0 | hit@5 |
| Q015 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent | 0 | 0 | hit@20 |
| Q016 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent | 0 | 0 | hit@5 |
| Q017 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent | 0 | 0 | hit@5 |
| Q018 | direct_standard_lookup, judgment_paragraph_combination, term_bridge_or_exam_convention_dependent | 0 | 0 | hit@10 |
| Q019 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent, workflow_seed_question | 0 | 0 | hit@5 |
| Q020 | direct_standard_lookup, judgment_paragraph_combination, term_bridge_or_exam_convention_dependent | 0 | 0 | hit@5 |
| Q021 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent, workflow_seed_question | 0 | 0 | hit@5 |
| Q022 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent | 0 | 0 | hit@5 |
| Q023 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent | 0 | 0 | hit@5 |
| Q024 | direct_standard_lookup, judgment_paragraph_combination, term_bridge_or_exam_convention_dependent | 0 | 0 | hit@5 |
| Q025 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent | 1 | 0 | hit@20 |
| Q026 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent | 1 | 0 | hit@10 |
| Q027 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent, workflow_seed_question | 0 | 0 | hit@5 |
| Q028 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent, workflow_seed_question | 0 | 0 | hit@20 |
| Q029 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent | 0 | 0 | hit@5 |
| Q030 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent | 0 | 0 | hit@5 |
| Q031 | judgment_paragraph_combination | 0 | 0 | hit@10 |
| Q032 | judgment_paragraph_combination | 0 | 0 | hit@20 |
| Q033 | direct_standard_lookup | 0 | 0 | hit@20 |
| Q034 | judgment_paragraph_combination | 0 | 0 | hit@10 |
| Q035 | judgment_paragraph_combination | 0 | 0 | hit@5 |
| Q036 | judgment_paragraph_combination | 0 | 0 | hit@20 |
| Q037 | disclosure_question, judgment_paragraph_combination | 0 | 0 | hit@5 |
| Q038 | judgment_paragraph_combination | 0 | 0 | hit@5 |
| Q039 | judgment_paragraph_combination | 0 | 0 | hit@5 |
| Q040 | judgment_paragraph_combination | 1 | 0 | hit@5 |
| Q041 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent | 1 | 0 | hit@5 |
| Q042 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent, workflow_seed_question | 0 | 0 | hit@5 |
| Q043 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent, workflow_seed_question | 0 | 0 | hit@5 |
| Q044 | judgment_paragraph_combination | 0 | 0 | hit@5 |
| Q045 | judgment_paragraph_combination | 0 | 0 | hit@10 |
| Q046 | judgment_paragraph_combination | 0 | 0 | hit@5 |
| Q047 | judgment_paragraph_combination | 0 | 0 | hit@5 |
| Q048 | judgment_paragraph_combination | 0 | 0 | hit@20 |
| Q049 | judgment_paragraph_combination | 0 | 0 | hit@5 |
| Q050 | judgment_paragraph_combination, workflow_seed_question | 0 | 0 | hit@10 |

## Target Misses

- none

## Excluded Protected Fields

- question
- source_ref
- notes
- answer body
- paragraph body

## Machine Result

```json
{
  "ok": true,
  "title": "RR3 Retrieval and Citation Diagnostics",
  "milestone": "RR3",
  "k": 20,
  "retrievers": [
    "hybrid",
    "ifrs1109_classification_hybrid"
  ],
  "retrieval_aggregate": {
    "hybrid": {
      "recall@1": 0.1967,
      "recall@3": 0.3867,
      "recall@5": 0.5467,
      "recall@10": 0.7133,
      "recall@20": 0.8867,
      "mrr": 0.4635,
      "ndcg@10": 0.4824
    },
    "ifrs1109_classification_hybrid": {
      "recall@1": 0.2333,
      "recall@3": 0.3967,
      "recall@5": 0.5633,
      "recall@10": 0.7733,
      "recall@20": 1.0,
      "mrr": 0.5184,
      "ndcg@10": 0.5279
    }
  },
  "citation_rank_summary": {
    "hybrid": {
      "hit@5": 45,
      "hit@10": 14,
      "hit@20": 14,
      "beyond@20": 0,
      "absent": 9
    },
    "ifrs1109_classification_hybrid": {
      "hit@5": 47,
      "hit@10": 18,
      "hit@20": 17,
      "beyond@20": 0,
      "absent": 0
    }
  },
  "bucket_summary": {
    "direct_standard_lookup": {
      "citations": 5,
      "recovered": 0,
      "still_absent": 0,
      "target_worse": 0,
      "target_hit20": 5
    },
    "disclosure_question": {
      "citations": 6,
      "recovered": 5,
      "still_absent": 0,
      "target_worse": 0,
      "target_hit20": 6
    },
    "judgment_paragraph_combination": {
      "citations": 80,
      "recovered": 15,
      "still_absent": 0,
      "target_worse": 2,
      "target_hit20": 80
    },
    "term_bridge_or_exam_convention_dependent": {
      "citations": 43,
      "recovered": 6,
      "still_absent": 0,
      "target_worse": 0,
      "target_hit20": 43
    },
    "workflow_seed_question": {
      "citations": 24,
      "recovered": 3,
      "still_absent": 0,
      "target_worse": 1,
      "target_hit20": 24
    }
  },
  "item_summary": [
    {
      "id": "Q001",
      "buckets": [
        "judgment_paragraph_combination"
      ],
      "baseline_miss_count": 1,
      "target_miss_count": 0,
      "best_target_bucket": "hit@5"
    },
    {
      "id": "Q002",
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@5"
    },
    {
      "id": "Q003",
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@10"
    },
    {
      "id": "Q004",
      "buckets": [
        "disclosure_question",
        "judgment_paragraph_combination"
      ],
      "baseline_miss_count": 1,
      "target_miss_count": 0,
      "best_target_bucket": "hit@5"
    },
    {
      "id": "Q005",
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent",
        "workflow_seed_question"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@5"
    },
    {
      "id": "Q006",
      "buckets": [
        "disclosure_question",
        "judgment_paragraph_combination",
        "workflow_seed_question"
      ],
      "baseline_miss_count": 1,
      "target_miss_count": 0,
      "best_target_bucket": "hit@5"
    },
    {
      "id": "Q007",
      "buckets": [
        "judgment_paragraph_combination"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@5"
    },
    {
      "id": "Q008",
      "buckets": [
        "judgment_paragraph_combination",
        "workflow_seed_question"
      ],
      "baseline_miss_count": 1,
      "target_miss_count": 0,
      "best_target_bucket": "hit@5"
    },
    {
      "id": "Q009",
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent",
        "workflow_seed_question"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@5"
    },
    {
      "id": "Q010",
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent",
        "workflow_seed_question"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@5"
    },
    {
      "id": "Q011",
      "buckets": [
        "direct_standard_lookup",
        "term_bridge_or_exam_convention_dependent"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@5"
    },
    {
      "id": "Q012",
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@5"
    },
    {
      "id": "Q013",
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent"
      ],
      "baseline_miss_count": 1,
      "target_miss_count": 0,
      "best_target_bucket": "hit@5"
    },
    {
      "id": "Q014",
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@5"
    },
    {
      "id": "Q015",
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@20"
    },
    {
      "id": "Q016",
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@5"
    },
    {
      "id": "Q017",
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@5"
    },
    {
      "id": "Q018",
      "buckets": [
        "direct_standard_lookup",
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@10"
    },
    {
      "id": "Q019",
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent",
        "workflow_seed_question"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@5"
    },
    {
      "id": "Q020",
      "buckets": [
        "direct_standard_lookup",
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@5"
    },
    {
      "id": "Q021",
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent",
        "workflow_seed_question"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@5"
    },
    {
      "id": "Q022",
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@5"
    },
    {
      "id": "Q023",
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@5"
    },
    {
      "id": "Q024",
      "buckets": [
        "direct_standard_lookup",
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@5"
    },
    {
      "id": "Q025",
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent"
      ],
      "baseline_miss_count": 1,
      "target_miss_count": 0,
      "best_target_bucket": "hit@20"
    },
    {
      "id": "Q026",
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent"
      ],
      "baseline_miss_count": 1,
      "target_miss_count": 0,
      "best_target_bucket": "hit@10"
    },
    {
      "id": "Q027",
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent",
        "workflow_seed_question"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@5"
    },
    {
      "id": "Q028",
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent",
        "workflow_seed_question"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@20"
    },
    {
      "id": "Q029",
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@5"
    },
    {
      "id": "Q030",
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@5"
    },
    {
      "id": "Q031",
      "buckets": [
        "judgment_paragraph_combination"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@10"
    },
    {
      "id": "Q032",
      "buckets": [
        "judgment_paragraph_combination"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@20"
    },
    {
      "id": "Q033",
      "buckets": [
        "direct_standard_lookup"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@20"
    },
    {
      "id": "Q034",
      "buckets": [
        "judgment_paragraph_combination"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@10"
    },
    {
      "id": "Q035",
      "buckets": [
        "judgment_paragraph_combination"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@5"
    },
    {
      "id": "Q036",
      "buckets": [
        "judgment_paragraph_combination"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@20"
    },
    {
      "id": "Q037",
      "buckets": [
        "disclosure_question",
        "judgment_paragraph_combination"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@5"
    },
    {
      "id": "Q038",
      "buckets": [
        "judgment_paragraph_combination"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@5"
    },
    {
      "id": "Q039",
      "buckets": [
        "judgment_paragraph_combination"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@5"
    },
    {
      "id": "Q040",
      "buckets": [
        "judgment_paragraph_combination"
      ],
      "baseline_miss_count": 1,
      "target_miss_count": 0,
      "best_target_bucket": "hit@5"
    },
    {
      "id": "Q041",
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent"
      ],
      "baseline_miss_count": 1,
      "target_miss_count": 0,
      "best_target_bucket": "hit@5"
    },
    {
      "id": "Q042",
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent",
        "workflow_seed_question"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@5"
    },
    {
      "id": "Q043",
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent",
        "workflow_seed_question"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@5"
    },
    {
      "id": "Q044",
      "buckets": [
        "judgment_paragraph_combination"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@5"
    },
    {
      "id": "Q045",
      "buckets": [
        "judgment_paragraph_combination"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@10"
    },
    {
      "id": "Q046",
      "buckets": [
        "judgment_paragraph_combination"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@5"
    },
    {
      "id": "Q047",
      "buckets": [
        "judgment_paragraph_combination"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@5"
    },
    {
      "id": "Q048",
      "buckets": [
        "judgment_paragraph_combination"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@20"
    },
    {
      "id": "Q049",
      "buckets": [
        "judgment_paragraph_combination"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@5"
    },
    {
      "id": "Q050",
      "buckets": [
        "judgment_paragraph_combination",
        "workflow_seed_question"
      ],
      "baseline_miss_count": 0,
      "target_miss_count": 0,
      "best_target_bucket": "hit@10"
    }
  ],
  "target_misses": [],
  "recovered_item_ids": [
    "Q001",
    "Q004",
    "Q006",
    "Q008",
    "Q013",
    "Q025",
    "Q026",
    "Q040",
    "Q041"
  ],
  "failure_taxonomy": {
    "rank_improved": 6,
    "rank_worse": 2,
    "recovered_from_absent": 9,
    "target_items_with_misses": 0,
    "unchanged": 65
  },
  "protected_fields_excluded": [
    "question",
    "source_ref",
    "notes",
    "answer body",
    "paragraph body"
  ],
  "errors": [],
  "report_path": "docs/reports/2026-07-05-rr3-retrieval-citation-diagnostics.md"
}
```
