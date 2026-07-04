from kifrs.eval.retrieval import miss_summary_by_retriever, query_variants, rrf_fuse_results


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
