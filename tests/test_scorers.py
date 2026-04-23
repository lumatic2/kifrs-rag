"""Scorer + citation 추출 단위 테스트."""
from kifrs.eval.scorers import (
    _extract_citations, CiteScorer, KeywordScorer, GlobalRulesScorer,
)
from kifrs.eval.models import GoldItem, RunResult, Citation


def _mk_run(answer: str) -> RunResult:
    return RunResult(item_id="T", runner="test", question="", answer=answer)


def _mk_item(must, may=None, keywords=None, forbidden=None) -> GoldItem:
    return GoldItem(
        id="T", source="test", source_ref="", question="",
        must_cite=[Citation(*t) for t in must],
        may_cite=[Citation(*t) for t in (may or [])],
        keywords=keywords or [],
        forbidden_keywords=forbidden or [],
    )


# ── citation 추출 ─────────────────────────────────────────────────────────
def test_extract_bracketed():
    cites = _extract_citations("근거는 [1115-27] 과 [1109-4.1.2A] 이다.")
    assert ("1115", "27") in cites
    assert ("1109", "4.1.2A") in cites


def test_extract_no_bracket():
    cites = _extract_citations("기업회계기준서 제1116호 문단 24에 따르면,")
    assert ("1116", "24") in cites


def test_extract_dedup():
    cites = _extract_citations("[1115-27] ... [1115-27] 다시 언급")
    assert cites.count(("1115", "27")) == 1


# ── CiteScorer ────────────────────────────────────────────────────────────
def test_cite_full_hit():
    item = _mk_item(must=[("1115", "27")])
    run = _mk_run("근거 [1115-27]")
    s = CiteScorer().score(item, run)
    assert s.score >= 0.99  # f1=1.0
    assert s.details["recall"] == 1.0


def test_cite_miss():
    item = _mk_item(must=[("1115", "27"), ("1115", "22")])
    run = _mk_run("근거 [1115-27] 만 인용")
    s = CiteScorer().score(item, run)
    assert s.details["recall"] == 0.5
    assert ("1115", "22") in [tuple(x) for x in s.details["must_miss"]]


def test_cite_noise_penalty():
    # 무관한 인용이 많으면 precision 감소
    item = _mk_item(must=[("1115", "27")])
    run = _mk_run("근거 [1115-27], 그리고 [9999-1], [9999-2], [9999-3]")
    s = CiteScorer().score(item, run)
    assert s.details["precision"] == 0.25
    assert s.score < 0.5  # f1=0.4, 가점 없음


# ── KeywordScorer ─────────────────────────────────────────────────────────
def test_keyword_hit_rate():
    item = _mk_item(must=[("1115", "27")],
                    keywords=["구별되는 재화", "수행의무 2개", "단독 효익"])
    run = _mk_run("답: 구별되는 재화가 맞고 수행의무 2개로 식별된다.")
    s = KeywordScorer().score(item, run)
    assert abs(s.score - 2/3) < 0.01


def test_keyword_forbidden_penalty():
    item = _mk_item(must=[("1115", "27")],
                    keywords=["구별"],
                    forbidden=["단일 수행의무"])
    run = _mk_run("구별된다. 하지만 단일 수행의무로 본다면...")
    s = KeywordScorer().score(item, run)
    # hit_rate=1.0, penalty=0.2 → 0.8
    assert abs(s.score - 0.8) < 0.01


# ── GlobalRulesScorer ─────────────────────────────────────────────────────
def test_global_rules_invalid_standard():
    """존재하지 않는 기준서 9999를 인용하면 감점."""
    item = _mk_item(must=[("1115", "27")])
    run = _mk_run("[1115-27] 과 [9999-1] 인용")
    s = GlobalRulesScorer().score(item, run)
    # total=2, bad=1 (9999 unknown) → 0.5
    assert s.score == 0.5
    assert ("9999", "1") in [tuple(x) for x in s.details["invalid_standard"]]


def test_global_rules_all_valid():
    item = _mk_item(must=[("1115", "27")])
    run = _mk_run("[1115-27] 정확한 인용")
    s = GlobalRulesScorer().score(item, run)
    # Note: 1115-27 가 실제 DB에 있어야 통과 — Phase 1 데이터로 있음
    assert s.score == 1.0
    assert ("1115", "27") in [tuple(x) for x in s.details["valid"]]


def test_global_rules_empty_cites():
    item = _mk_item(must=[("1115", "27")])
    run = _mk_run("인용 없이 답함.")
    s = GlobalRulesScorer().score(item, run)
    # 인용 없음 → 중립 1.0 (cite scorer에서 감점)
    assert s.score == 1.0
