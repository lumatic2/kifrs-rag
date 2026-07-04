from kifrs.eval.retrieval import (
    citation_rank_bucket,
    gold_rank_summary,
    miss_summary_by_retriever,
    must_cite_rank_rows,
    must_cite_rank_summary,
    query_variants,
    rrf_fuse_results,
)


def test_miss_summary_by_retriever_keeps_retrievers_separate():
    report = {
        "retrievers": {
            "hybrid": {
                "per_item": [
                    {"id": "Q004", "miss": [("1001", "69")]},
                    {"id": "Q041", "miss": []},
                ],
            },
            "reranked": {
                "per_item": [
                    {"id": "Q004", "miss": []},
                    {"id": "Q041", "miss": [("1102", "11")]},
                ],
            },
        },
    }

    assert miss_summary_by_retriever(report) == {
        "hybrid": [("Q004", [("1001", "69")])],
        "reranked": [("Q041", [("1102", "11")])],
    }


def test_miss_summary_by_retriever_omits_clean_retrievers():
    report = {
        "retrievers": {
            "hybrid": {"per_item": [{"id": "Q001", "miss": []}]},
            "reranked": {"per_item": [{"id": "Q001", "miss": []}]},
        },
    }

    assert miss_summary_by_retriever(report) == {}


def test_query_variants_adds_literal_cross_concept_phrases():
    variants = query_variants("리스 종료 원상복구 의무에 대한 충당부채 인식요건은 무엇인가?")

    assert variants[0] == "리스 종료 원상복구 의무에 대한 충당부채 인식요건은 무엇인가?"
    assert "원상복구 의무" in variants
    assert "충당부채" in variants
    assert "인식요건" in variants
    assert "현재의무 자원 유출 가능성 신뢰성 있게 추정" in variants


def test_query_variants_splits_delimited_concepts():
    variants = query_variants("회수가능액 정의 및 손상차손 인식 기준은 무엇인가?")

    assert "회수가능액 정의" in variants
    assert "손상차손 인식 기준은 무엇인가" in variants
    assert "회수가능액" in variants
    assert "손상차손" in variants
    assert "공정가치 처분부대원가 사용가치" in variants
    assert "장부금액 회수가능액 초과" in variants


def test_rrf_fuse_results_merges_duplicate_hits_and_preserves_best_metadata():
    fused = rrf_fuse_results(
        [
            [{"standard": "1116", "no": "45", "snippet": "lease"}],
            [
                {"standard": "1037", "no": "14", "snippet": "provision"},
                {"standard": "1116", "no": "45", "snippet": "lease duplicate"},
            ],
        ],
        limit=2,
    )

    assert [(row["standard"], row["no"]) for row in fused] == [("1116", "45"), ("1037", "14")]
    assert fused[0]["snippet"] == "lease"


def test_gold_rank_summary_reports_each_required_citation_rank():
    ranks = gold_rank_summary(
        {("1116", "24"), ("1037", "14")},
        [("1116", "24"), ("1001", "69"), ("1037", "14")],
    )

    assert ranks == {"1037-14": 3, "1116-24": 1}


def test_gold_rank_summary_marks_absent_citation_as_none():
    ranks = gold_rank_summary({("1036", "18")}, [("1036", "59")])

    assert ranks == {"1036-18": None}


def test_citation_rank_bucket_classifies_rank_bands():
    assert citation_rank_bucket(1) == "hit@5"
    assert citation_rank_bucket(10) == "hit@10"
    assert citation_rank_bucket(20) == "hit@20"
    assert citation_rank_bucket(21) == "beyond@20"
    assert citation_rank_bucket(None) == "absent"


def test_must_cite_rank_rows_flattens_gold_ranks():
    report = {
        "retrievers": {
            "hybrid": {
                "per_item": [
                    {"id": "Q039", "gold_ranks": {"1037-14": 16, "1116-24": 4}},
                    {"id": "Q048", "gold_ranks": {"1036-18": None}},
                ]
            }
        }
    }

    assert must_cite_rank_rows(report) == [
        {
            "retriever": "hybrid",
            "item_id": "Q039",
            "citation": "1037-14",
            "rank": 16,
            "bucket": "hit@20",
        },
        {
            "retriever": "hybrid",
            "item_id": "Q039",
            "citation": "1116-24",
            "rank": 4,
            "bucket": "hit@5",
        },
        {
            "retriever": "hybrid",
            "item_id": "Q048",
            "citation": "1036-18",
            "rank": None,
            "bucket": "absent",
        },
    ]


def test_must_cite_rank_summary_counts_buckets_per_retriever():
    report = {
        "retrievers": {
            "hybrid": {
                "per_item": [
                    {
                        "id": "Q001",
                        "gold_ranks": {
                            "1115-27": 3,
                            "1115-31": 8,
                            "1115-35": 18,
                            "1115-40": 21,
                            "1115-45": None,
                        },
                    }
                ]
            }
        }
    }

    assert must_cite_rank_summary(report) == {
        "hybrid": {
            "hit@5": 1,
            "hit@10": 1,
            "hit@20": 1,
            "beyond@20": 1,
            "absent": 1,
        }
    }
