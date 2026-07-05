# RR2 Eval Matrix and Seed Coverage

> Scope: public-safe eval coverage matrix for K-IFRS RAG reliability revalidation.

## 한 줄 결론

The goldset covers the required RAG evaluation buckets; RR3 can proceed to retrieval and citation diagnostics by bucket.

## Methodology Source

Knowledge-graph nodes used:
- `rag-evaluation-metrics`
- `rag-retrieval-rank-debugging-playbook`
- `rag-retrieval-strategy`
- `rag-reranking-strategy`

Applied rule: compare RAG variants on a stable golden set, separating retrieval/citation metrics from answer metrics such as faithfulness, answer relevance, context precision, context recall, latency, and cost.

## Coverage Summary

- Items: 50
- Standards covered: 1001, 1002, 1016, 1019, 1032, 1033, 1036, 1037, 1038, 1102, 1109, 1115, 1116, 2119

| Bucket | Count | Metric Focus |
|---|---:|---|
| direct_standard_lookup | 5 | context_recall, citation_hit_rate, latency |
| judgment_paragraph_combination | 48 | faithfulness, answer_relevance, context_recall, citation_coverage |
| workflow_seed_question | 12 | answer_relevance, faithfulness, global_rules, needs_human_review_boundary |
| disclosure_question | 3 | context_precision, context_recall, citation_coverage |
| term_bridge_or_exam_convention_dependent | 28 | context_recall, term_bridge_hit, faithfulness |

## Public-Safe Item Matrix

| ID | Source | Standards | Must Cite Count | May Cite Count | Keyword Count | Buckets |
|---|---|---|---:|---:|---:|---|
| Q001 | synth | 1115 | 2 | 3 | 5 | judgment_paragraph_combination |
| Q002 | cpa-2 | 1116 | 2 | 1 | 4 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent |
| Q003 | cpa-1 | 1109 | 1 | 2 | 4 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent |
| Q004 | synth | 1001 | 3 | 2 | 4 | disclosure_question, judgment_paragraph_combination |
| Q005 | cpa-2 | 1109, 1115 | 3 | 3 | 4 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent, workflow_seed_question |
| Q006 | synth | 1109, 1115 | 2 | 4 | 4 | disclosure_question, judgment_paragraph_combination, workflow_seed_question |
| Q007 | synth | 1116 | 2 | 2 | 5 | judgment_paragraph_combination |
| Q008 | synth | 1109, 1116 | 3 | 3 | 5 | judgment_paragraph_combination, workflow_seed_question |
| Q009 | cpa-2 | 1115 | 2 | 2 | 5 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent, workflow_seed_question |
| Q010 | cpa-2 | 1115 | 2 | 1 | 4 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent, workflow_seed_question |
| Q011 | cpa-2 | 1002 | 1 | 2 | 5 | direct_standard_lookup, term_bridge_or_exam_convention_dependent |
| Q012 | cpa-2 | 1002 | 1 | 1 | 3 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent |
| Q013 | cpa-2 | 1037 | 2 | 1 | 5 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent |
| Q014 | cpa-2 | 1109 | 1 | 1 | 4 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent |
| Q015 | cpa-2 | 1109 | 1 | 2 | 3 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent |
| Q016 | cpa-2 | 1109 | 2 | 1 | 3 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent |
| Q017 | cpa-2 | 1109 | 1 | 2 | 4 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent |
| Q018 | cpa-2 | 1032 | 1 | 2 | 5 | direct_standard_lookup, judgment_paragraph_combination, term_bridge_or_exam_convention_dependent |
| Q019 | cpa-2 | 1019 | 2 | 1 | 4 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent, workflow_seed_question |
| Q020 | cpa-2 | 1019 | 1 | 2 | 4 | direct_standard_lookup, judgment_paragraph_combination, term_bridge_or_exam_convention_dependent |
| Q021 | cpa-2 | 1019 | 2 | 1 | 4 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent, workflow_seed_question |
| Q022 | cpa-2 | 1019 | 2 | 1 | 4 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent |
| Q023 | cpa-2 | 1037 | 2 | 2 | 4 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent |
| Q024 | cpa-2 | 1037 | 1 | 1 | 3 | direct_standard_lookup, judgment_paragraph_combination, term_bridge_or_exam_convention_dependent |
| Q025 | cpa-2 | 1037 | 1 | 1 | 3 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent |
| Q026 | cpa-2 | 1037 | 1 | 2 | 4 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent |
| Q027 | cpa-2 | 1115 | 1 | 2 | 4 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent, workflow_seed_question |
| Q028 | cpa-2 | 1116 | 1 | 1 | 4 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent, workflow_seed_question |
| Q029 | cpa-2 | 1116 | 2 | 1 | 4 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent |
| Q030 | cpa-2 | 1116 | 1 | 1 | 4 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent |
| Q031 | scenario | 1116 | 2 | 2 | 6 | judgment_paragraph_combination |
| Q032 | scenario | 1109 | 1 | 2 | 4 | judgment_paragraph_combination |
| Q033 | scenario | 1109 | 1 | 1 | 4 | direct_standard_lookup |
| Q034 | scenario | 1109 | 1 | 1 | 4 | judgment_paragraph_combination |
| Q035 | scenario | 1109 | 1 | 2 | 4 | judgment_paragraph_combination |
| Q036 | scenario | 1109 | 1 | 2 | 3 | judgment_paragraph_combination |
| Q037 | scenario | 1109 | 1 | 2 | 4 | disclosure_question, judgment_paragraph_combination |
| Q038 | scenario | 2119 | 2 | 2 | 5 | judgment_paragraph_combination |
| Q039 | scenario | 1037, 1116 | 2 | 2 | 4 | judgment_paragraph_combination |
| Q040 | scenario | 1109 | 1 | 3 | 3 | judgment_paragraph_combination |
| Q041 | textbook | 1102 | 2 | 2 | 4 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent |
| Q042 | textbook | 1033 | 2 | 3 | 4 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent, workflow_seed_question |
| Q043 | textbook | 1033 | 2 | 2 | 4 | judgment_paragraph_combination, term_bridge_or_exam_convention_dependent, workflow_seed_question |
| Q044 | synth | 1115 | 2 | 2 | 3 | judgment_paragraph_combination |
| Q045 | synth | 1115 | 2 | 2 | 4 | judgment_paragraph_combination |
| Q046 | synth | 1116 | 2 | 2 | 4 | judgment_paragraph_combination |
| Q047 | synth | 1116 | 2 | 2 | 5 | judgment_paragraph_combination |
| Q048 | synth | 1036 | 2 | 2 | 5 | judgment_paragraph_combination |
| Q049 | synth | 1016 | 2 | 2 | 4 | judgment_paragraph_combination |
| Q050 | synth | 1038 | 2 | 2 | 5 | judgment_paragraph_combination, workflow_seed_question |

## Coverage Gaps

- none

## RR3 Input

- Needed: retrieval and citation diagnostics by bucket
- Compare: hybrid, ifrs1109_classification_hybrid
- Metrics: recall@k, MRR, nDCG@10, required-citation rank bucket, target misses

## Excluded Protected Fields

- question
- source_ref
- notes
- raw answer body

## Machine Result

```json
{
  "ok": true,
  "title": "RR2 Eval Matrix and Seed Coverage",
  "milestone": "RR2",
  "methodology_nodes": [
    "rag-evaluation-metrics",
    "rag-retrieval-rank-debugging-playbook",
    "rag-retrieval-strategy",
    "rag-reranking-strategy"
  ],
  "item_count": 50,
  "standards": [
    "1001",
    "1002",
    "1016",
    "1019",
    "1032",
    "1033",
    "1036",
    "1037",
    "1038",
    "1102",
    "1109",
    "1115",
    "1116",
    "2119"
  ],
  "bucket_counts": {
    "direct_standard_lookup": 5,
    "disclosure_question": 3,
    "judgment_paragraph_combination": 48,
    "term_bridge_or_exam_convention_dependent": 28,
    "workflow_seed_question": 12
  },
  "coverage_gaps": [],
  "metric_policy": {
    "direct_standard_lookup": [
      "context_recall",
      "citation_hit_rate",
      "latency"
    ],
    "judgment_paragraph_combination": [
      "faithfulness",
      "answer_relevance",
      "context_recall",
      "citation_coverage"
    ],
    "workflow_seed_question": [
      "answer_relevance",
      "faithfulness",
      "global_rules",
      "needs_human_review_boundary"
    ],
    "disclosure_question": [
      "context_precision",
      "context_recall",
      "citation_coverage"
    ],
    "term_bridge_or_exam_convention_dependent": [
      "context_recall",
      "term_bridge_hit",
      "faithfulness"
    ]
  },
  "public_safe_matrix": [
    {
      "id": "Q001",
      "source": "synth",
      "standards": [
        "1115"
      ],
      "must_cite_count": 2,
      "may_cite_count": 3,
      "keyword_count": 5,
      "buckets": [
        "judgment_paragraph_combination"
      ]
    },
    {
      "id": "Q002",
      "source": "cpa-2",
      "standards": [
        "1116"
      ],
      "must_cite_count": 2,
      "may_cite_count": 1,
      "keyword_count": 4,
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent"
      ]
    },
    {
      "id": "Q003",
      "source": "cpa-1",
      "standards": [
        "1109"
      ],
      "must_cite_count": 1,
      "may_cite_count": 2,
      "keyword_count": 4,
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent"
      ]
    },
    {
      "id": "Q004",
      "source": "synth",
      "standards": [
        "1001"
      ],
      "must_cite_count": 3,
      "may_cite_count": 2,
      "keyword_count": 4,
      "buckets": [
        "disclosure_question",
        "judgment_paragraph_combination"
      ]
    },
    {
      "id": "Q005",
      "source": "cpa-2",
      "standards": [
        "1109",
        "1115"
      ],
      "must_cite_count": 3,
      "may_cite_count": 3,
      "keyword_count": 4,
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent",
        "workflow_seed_question"
      ]
    },
    {
      "id": "Q006",
      "source": "synth",
      "standards": [
        "1109",
        "1115"
      ],
      "must_cite_count": 2,
      "may_cite_count": 4,
      "keyword_count": 4,
      "buckets": [
        "disclosure_question",
        "judgment_paragraph_combination",
        "workflow_seed_question"
      ]
    },
    {
      "id": "Q007",
      "source": "synth",
      "standards": [
        "1116"
      ],
      "must_cite_count": 2,
      "may_cite_count": 2,
      "keyword_count": 5,
      "buckets": [
        "judgment_paragraph_combination"
      ]
    },
    {
      "id": "Q008",
      "source": "synth",
      "standards": [
        "1109",
        "1116"
      ],
      "must_cite_count": 3,
      "may_cite_count": 3,
      "keyword_count": 5,
      "buckets": [
        "judgment_paragraph_combination",
        "workflow_seed_question"
      ]
    },
    {
      "id": "Q009",
      "source": "cpa-2",
      "standards": [
        "1115"
      ],
      "must_cite_count": 2,
      "may_cite_count": 2,
      "keyword_count": 5,
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent",
        "workflow_seed_question"
      ]
    },
    {
      "id": "Q010",
      "source": "cpa-2",
      "standards": [
        "1115"
      ],
      "must_cite_count": 2,
      "may_cite_count": 1,
      "keyword_count": 4,
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent",
        "workflow_seed_question"
      ]
    },
    {
      "id": "Q011",
      "source": "cpa-2",
      "standards": [
        "1002"
      ],
      "must_cite_count": 1,
      "may_cite_count": 2,
      "keyword_count": 5,
      "buckets": [
        "direct_standard_lookup",
        "term_bridge_or_exam_convention_dependent"
      ]
    },
    {
      "id": "Q012",
      "source": "cpa-2",
      "standards": [
        "1002"
      ],
      "must_cite_count": 1,
      "may_cite_count": 1,
      "keyword_count": 3,
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent"
      ]
    },
    {
      "id": "Q013",
      "source": "cpa-2",
      "standards": [
        "1037"
      ],
      "must_cite_count": 2,
      "may_cite_count": 1,
      "keyword_count": 5,
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent"
      ]
    },
    {
      "id": "Q014",
      "source": "cpa-2",
      "standards": [
        "1109"
      ],
      "must_cite_count": 1,
      "may_cite_count": 1,
      "keyword_count": 4,
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent"
      ]
    },
    {
      "id": "Q015",
      "source": "cpa-2",
      "standards": [
        "1109"
      ],
      "must_cite_count": 1,
      "may_cite_count": 2,
      "keyword_count": 3,
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent"
      ]
    },
    {
      "id": "Q016",
      "source": "cpa-2",
      "standards": [
        "1109"
      ],
      "must_cite_count": 2,
      "may_cite_count": 1,
      "keyword_count": 3,
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent"
      ]
    },
    {
      "id": "Q017",
      "source": "cpa-2",
      "standards": [
        "1109"
      ],
      "must_cite_count": 1,
      "may_cite_count": 2,
      "keyword_count": 4,
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent"
      ]
    },
    {
      "id": "Q018",
      "source": "cpa-2",
      "standards": [
        "1032"
      ],
      "must_cite_count": 1,
      "may_cite_count": 2,
      "keyword_count": 5,
      "buckets": [
        "direct_standard_lookup",
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent"
      ]
    },
    {
      "id": "Q019",
      "source": "cpa-2",
      "standards": [
        "1019"
      ],
      "must_cite_count": 2,
      "may_cite_count": 1,
      "keyword_count": 4,
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent",
        "workflow_seed_question"
      ]
    },
    {
      "id": "Q020",
      "source": "cpa-2",
      "standards": [
        "1019"
      ],
      "must_cite_count": 1,
      "may_cite_count": 2,
      "keyword_count": 4,
      "buckets": [
        "direct_standard_lookup",
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent"
      ]
    },
    {
      "id": "Q021",
      "source": "cpa-2",
      "standards": [
        "1019"
      ],
      "must_cite_count": 2,
      "may_cite_count": 1,
      "keyword_count": 4,
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent",
        "workflow_seed_question"
      ]
    },
    {
      "id": "Q022",
      "source": "cpa-2",
      "standards": [
        "1019"
      ],
      "must_cite_count": 2,
      "may_cite_count": 1,
      "keyword_count": 4,
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent"
      ]
    },
    {
      "id": "Q023",
      "source": "cpa-2",
      "standards": [
        "1037"
      ],
      "must_cite_count": 2,
      "may_cite_count": 2,
      "keyword_count": 4,
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent"
      ]
    },
    {
      "id": "Q024",
      "source": "cpa-2",
      "standards": [
        "1037"
      ],
      "must_cite_count": 1,
      "may_cite_count": 1,
      "keyword_count": 3,
      "buckets": [
        "direct_standard_lookup",
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent"
      ]
    },
    {
      "id": "Q025",
      "source": "cpa-2",
      "standards": [
        "1037"
      ],
      "must_cite_count": 1,
      "may_cite_count": 1,
      "keyword_count": 3,
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent"
      ]
    },
    {
      "id": "Q026",
      "source": "cpa-2",
      "standards": [
        "1037"
      ],
      "must_cite_count": 1,
      "may_cite_count": 2,
      "keyword_count": 4,
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent"
      ]
    },
    {
      "id": "Q027",
      "source": "cpa-2",
      "standards": [
        "1115"
      ],
      "must_cite_count": 1,
      "may_cite_count": 2,
      "keyword_count": 4,
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent",
        "workflow_seed_question"
      ]
    },
    {
      "id": "Q028",
      "source": "cpa-2",
      "standards": [
        "1116"
      ],
      "must_cite_count": 1,
      "may_cite_count": 1,
      "keyword_count": 4,
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent",
        "workflow_seed_question"
      ]
    },
    {
      "id": "Q029",
      "source": "cpa-2",
      "standards": [
        "1116"
      ],
      "must_cite_count": 2,
      "may_cite_count": 1,
      "keyword_count": 4,
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent"
      ]
    },
    {
      "id": "Q030",
      "source": "cpa-2",
      "standards": [
        "1116"
      ],
      "must_cite_count": 1,
      "may_cite_count": 1,
      "keyword_count": 4,
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent"
      ]
    },
    {
      "id": "Q031",
      "source": "scenario",
      "standards": [
        "1116"
      ],
      "must_cite_count": 2,
      "may_cite_count": 2,
      "keyword_count": 6,
      "buckets": [
        "judgment_paragraph_combination"
      ]
    },
    {
      "id": "Q032",
      "source": "scenario",
      "standards": [
        "1109"
      ],
      "must_cite_count": 1,
      "may_cite_count": 2,
      "keyword_count": 4,
      "buckets": [
        "judgment_paragraph_combination"
      ]
    },
    {
      "id": "Q033",
      "source": "scenario",
      "standards": [
        "1109"
      ],
      "must_cite_count": 1,
      "may_cite_count": 1,
      "keyword_count": 4,
      "buckets": [
        "direct_standard_lookup"
      ]
    },
    {
      "id": "Q034",
      "source": "scenario",
      "standards": [
        "1109"
      ],
      "must_cite_count": 1,
      "may_cite_count": 1,
      "keyword_count": 4,
      "buckets": [
        "judgment_paragraph_combination"
      ]
    },
    {
      "id": "Q035",
      "source": "scenario",
      "standards": [
        "1109"
      ],
      "must_cite_count": 1,
      "may_cite_count": 2,
      "keyword_count": 4,
      "buckets": [
        "judgment_paragraph_combination"
      ]
    },
    {
      "id": "Q036",
      "source": "scenario",
      "standards": [
        "1109"
      ],
      "must_cite_count": 1,
      "may_cite_count": 2,
      "keyword_count": 3,
      "buckets": [
        "judgment_paragraph_combination"
      ]
    },
    {
      "id": "Q037",
      "source": "scenario",
      "standards": [
        "1109"
      ],
      "must_cite_count": 1,
      "may_cite_count": 2,
      "keyword_count": 4,
      "buckets": [
        "disclosure_question",
        "judgment_paragraph_combination"
      ]
    },
    {
      "id": "Q038",
      "source": "scenario",
      "standards": [
        "2119"
      ],
      "must_cite_count": 2,
      "may_cite_count": 2,
      "keyword_count": 5,
      "buckets": [
        "judgment_paragraph_combination"
      ]
    },
    {
      "id": "Q039",
      "source": "scenario",
      "standards": [
        "1037",
        "1116"
      ],
      "must_cite_count": 2,
      "may_cite_count": 2,
      "keyword_count": 4,
      "buckets": [
        "judgment_paragraph_combination"
      ]
    },
    {
      "id": "Q040",
      "source": "scenario",
      "standards": [
        "1109"
      ],
      "must_cite_count": 1,
      "may_cite_count": 3,
      "keyword_count": 3,
      "buckets": [
        "judgment_paragraph_combination"
      ]
    },
    {
      "id": "Q041",
      "source": "textbook",
      "standards": [
        "1102"
      ],
      "must_cite_count": 2,
      "may_cite_count": 2,
      "keyword_count": 4,
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent"
      ]
    },
    {
      "id": "Q042",
      "source": "textbook",
      "standards": [
        "1033"
      ],
      "must_cite_count": 2,
      "may_cite_count": 3,
      "keyword_count": 4,
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent",
        "workflow_seed_question"
      ]
    },
    {
      "id": "Q043",
      "source": "textbook",
      "standards": [
        "1033"
      ],
      "must_cite_count": 2,
      "may_cite_count": 2,
      "keyword_count": 4,
      "buckets": [
        "judgment_paragraph_combination",
        "term_bridge_or_exam_convention_dependent",
        "workflow_seed_question"
      ]
    },
    {
      "id": "Q044",
      "source": "synth",
      "standards": [
        "1115"
      ],
      "must_cite_count": 2,
      "may_cite_count": 2,
      "keyword_count": 3,
      "buckets": [
        "judgment_paragraph_combination"
      ]
    },
    {
      "id": "Q045",
      "source": "synth",
      "standards": [
        "1115"
      ],
      "must_cite_count": 2,
      "may_cite_count": 2,
      "keyword_count": 4,
      "buckets": [
        "judgment_paragraph_combination"
      ]
    },
    {
      "id": "Q046",
      "source": "synth",
      "standards": [
        "1116"
      ],
      "must_cite_count": 2,
      "may_cite_count": 2,
      "keyword_count": 4,
      "buckets": [
        "judgment_paragraph_combination"
      ]
    },
    {
      "id": "Q047",
      "source": "synth",
      "standards": [
        "1116"
      ],
      "must_cite_count": 2,
      "may_cite_count": 2,
      "keyword_count": 5,
      "buckets": [
        "judgment_paragraph_combination"
      ]
    },
    {
      "id": "Q048",
      "source": "synth",
      "standards": [
        "1036"
      ],
      "must_cite_count": 2,
      "may_cite_count": 2,
      "keyword_count": 5,
      "buckets": [
        "judgment_paragraph_combination"
      ]
    },
    {
      "id": "Q049",
      "source": "synth",
      "standards": [
        "1016"
      ],
      "must_cite_count": 2,
      "may_cite_count": 2,
      "keyword_count": 4,
      "buckets": [
        "judgment_paragraph_combination"
      ]
    },
    {
      "id": "Q050",
      "source": "synth",
      "standards": [
        "1038"
      ],
      "must_cite_count": 2,
      "may_cite_count": 2,
      "keyword_count": 5,
      "buckets": [
        "judgment_paragraph_combination",
        "workflow_seed_question"
      ]
    }
  ],
  "protected_fields_excluded": [
    "question",
    "source_ref",
    "notes",
    "raw answer body"
  ],
  "rr3_input": {
    "needed": "retrieval and citation diagnostics by bucket",
    "compare": [
      "hybrid",
      "ifrs1109_classification_hybrid"
    ],
    "metrics": [
      "recall@k",
      "MRR",
      "nDCG@10",
      "required-citation rank bucket",
      "target misses"
    ]
  },
  "report_path": "docs/reports/2026-07-05-rr2-eval-matrix.md"
}
```
