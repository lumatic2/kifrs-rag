from kifrs.eval.harness import build_runner
from kifrs.eval.models import GoldItem, Citation


def test_build_local_rag_runner():
    runner = build_runner("local-rag")
    assert runner.name == "local-rag"


def test_local_rag_runner_returns_answer_and_context():
    item = GoldItem(
        id="T",
        source="test",
        source_ref="",
        question="확정급여제도의 일부를 정산할 때 정산손익은 어떻게 계산하는가?",
        must_cite=[Citation("1019", "109"), Citation("1019", "110")],
        keywords=["정산", "확정급여채무"],
    )
    run = build_runner("local-rag").run(item)
    assert run.answer
    assert run.runner == "local-rag"
    assert run.retrieved_context
