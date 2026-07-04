from kifrs.eval.retrieval import miss_summary_by_retriever


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
