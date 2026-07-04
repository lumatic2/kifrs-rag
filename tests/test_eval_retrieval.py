from kifrs.eval.retrieval import (
    citation_rank_bucket,
    gold_rank_summary,
    ifrs1109_classification_subquery,
    ifrs1109_scope_subquery,
    ifrs1115_subquery,
    insert_supplemental_results,
    miss_summary_by_retriever,
    must_cite_rank_rows,
    must_cite_rank_summary,
    query_variants,
    rrf_fuse_results,
    source_route_standard,
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


def test_source_route_standard_accepts_only_reviewed_clusters():
    assert source_route_standard(
        "보고기간 말 이후 차환 계약을 체결했다. 이 차입금은 유동부채인가 비유동부채인가?"
    ) == "1001"
    assert source_route_standard(
        "충당부채를 측정할 때 예상되는 자산 처분이익은 충당부채 금액에 반영하는가?"
    ) == "1037"
    assert source_route_standard(
        "주식결제형 주식기준보상거래에서 종업원의 경우 측정기준일은 언제인가?"
    ) == "1102"


def test_source_route_standard_rejects_known_failed_clusters():
    assert source_route_standard("리스부채는 1109호 금융부채로 회계처리해야 하는가?") is None
    assert source_route_standard("SPPI 불충족 채무상품은 어떻게 분류 측정하는가?") is None


def test_ifrs1115_subquery_accepts_reviewed_1115_gaps():
    assert ifrs1115_subquery(
        "소프트웨어 라이선스와 설치용역을 패키지로 판매한다. 수행의무를 몇 개로 구분해야 하는가?"
    ) == "고객 효익 쉽게 구할 수 있는 다른 자원 별도 식별 계약 내 다른 약속 구별"
    assert ifrs1115_subquery(
        "누적 구매액을 초과하면 초과분의 5%를 현금으로 환불하는 리베이트 프로그램"
    ) == "리베이트 환불 가격할인 변동대가 미래 사건 거래가격 환불부채"


def test_ifrs1115_subquery_rejects_non_1115_scope_gap():
    assert ifrs1115_subquery("리스부채는 1109호 금융부채로 회계처리해야 하는가?") is None


def test_ifrs1109_scope_subquery_accepts_reviewed_scope_gap():
    assert ifrs1109_scope_subquery(
        "리스이용자가 인식한 리스부채는 1109호 금융상품의 금융부채로 회계처리해야 하는가?"
    ) == "리스 계약 권리 의무 금융상품 적용범위 제외 1109 1116"


def test_ifrs1109_scope_subquery_rejects_unrelated_1109_question():
    assert ifrs1109_scope_subquery("SPPI 불충족 채무상품은 어떻게 분류 측정하는가?") is None


def test_insert_supplemental_results_preserves_baseline_order_and_deduplicates():
    baseline = [
        {"standard": "1116", "no": "22"},
        {"standard": "1116", "no": "26"},
        {"standard": "1115", "no": "22"},
    ]
    supplemental = [
        {"standard": "1109", "no": "2.1"},
        {"standard": "1116", "no": "26"},
    ]

    fused = insert_supplemental_results(
        baseline,
        supplemental,
        insert_after=1,
        supplemental_limit=1,
        limit=4,
    )

    assert [(row["standard"], row["no"]) for row in fused] == [
        ("1116", "22"),
        ("1109", "2.1"),
        ("1116", "26"),
        ("1115", "22"),
    ]


def test_ifrs1109_classification_subquery_accepts_reviewed_sppi_gap():
    assert ifrs1109_classification_subquery(
        "SPPI 불충족 채무상품은 당기손익 공정가치로 분류하는가?"
    ) == "상각후원가 기타포괄손익 공정가치 조건 아니라면 당기손익 공정가치 측정 금융자산"


def test_ifrs1109_classification_subquery_rejects_scope_gap():
    assert ifrs1109_classification_subquery("리스부채는 1109호 금융부채로 회계처리해야 하는가?") is None
