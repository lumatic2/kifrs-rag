"""평가 하네스 Scorer 구현.

3종 (Eng review에서 5→3 통합):
1. CiteScorer — must_cite precision/recall + may_cite 가점 + DB miss 감지
2. KeywordScorer — keywords 히트율 + forbidden_keywords 감점
3. GlobalRulesScorer — 존재하지 않는 기준서/문단 인용 검증

Runner 직접 store 호출 — eval 시간 동안 DB 연결 유지.
DB miss 시 silent 0점 방지 — ScoreResult.details["db_miss"] 에 명시.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Protocol

from kifrs import store
from .models import GoldItem, RunResult, ScoreResult


# 답변에서 [기준서-문단] 인용 추출.
# parse.py:RE_PARA_INLINE 과 동일한 suffix 체계. 부록 A1/B5 형식 허용.
# 매칭 예: [1115-27], [1109-4.1.2A], [1116-B5], (1115.60), 1115호 문단 27
RE_CITATION_BRACKETED = re.compile(r"\[(\d{4}|gaap_\w+|special_\w+|한)-([\w가-힣\.]+?)\]")
# parse.py RE_PARA_INLINE 와 공유: 숫자(.숫자)*[A-Z]?
RE_CITATION_PARA_NO = re.compile(r"\d+(?:\.\d+)*[A-Z]?")


def _extract_citations(answer: str) -> list[tuple[str, str]]:
    """답변 텍스트에서 (standard, no) 튜플 리스트 추출. 중복 제거."""
    cites: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()

    for m in RE_CITATION_BRACKETED.finditer(answer):
        std = m.group(1)
        no = m.group(2)
        key = (std, no)
        if key not in seen:
            seen.add(key)
            cites.append(key)

    # fallback: "1115호 문단 27", "1115호 27", "1115-27" (괄호 없이)
    # 패턴: <4자리>호?\s*(문단|제|paragraph)?\s*<no>
    for m in re.finditer(
        r"(\d{4})\s*호?\s*(?:문단|제|para(?:graph)?)?\s*(\d+(?:\.\d+)*[A-Z]?)",
        answer,
    ):
        key = (m.group(1), m.group(2))
        if key not in seen:
            seen.add(key)
            cites.append(key)
    return cites


class Scorer(Protocol):
    name: str
    def score(self, item: GoldItem, run: RunResult) -> ScoreResult: ...


# ── CiteScorer ────────────────────────────────────────────────────────────
@dataclass
class CiteScorer:
    name: str = "cite"

    def score(self, item: GoldItem, run: RunResult) -> ScoreResult:
        cites = _extract_citations(run.answer)
        must = {(c.standard, c.no) for c in item.must_cite}
        may = {(c.standard, c.no) for c in item.may_cite}
        cites_set = set(cites)

        must_hit = must & cites_set
        may_hit = may & cites_set

        # Precision: 찾은 인용 중 must∪may 에 속하는 비율
        relevant = must | may
        precision = (len(relevant & cites_set) / len(cites_set)) if cites_set else 0.0
        # Recall: must_cite 중 인용된 비율
        recall = (len(must_hit) / len(must)) if must else 1.0
        # F1 (must 우선) + may 가점 (+0.1 max)
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
        bonus = min(0.1, 0.05 * len(may_hit))
        final = min(1.0, f1 + bonus)

        return ScoreResult(
            scorer=self.name,
            score=final,
            details={
                "must_cite": sorted(list(must)),
                "must_hit": sorted(list(must_hit)),
                "must_miss": sorted(list(must - must_hit)),
                "may_hit": sorted(list(may_hit)),
                "cites_extracted": cites,
                "precision": round(precision, 3),
                "recall": round(recall, 3),
                "f1": round(f1, 3),
                "may_bonus": round(bonus, 3),
            },
        )


# ── KeywordScorer ─────────────────────────────────────────────────────────
@dataclass
class KeywordScorer:
    name: str = "keyword"

    def score(self, item: GoldItem, run: RunResult) -> ScoreResult:
        ans = run.answer.lower()

        def _contains(kw: str) -> bool:
            # 공백·한자 차이에 관대하게 — 한글은 그대로, 영문은 lowercase
            return kw.lower() in ans

        kw_hits = [k for k in item.keywords if _contains(k)]
        forbidden_hits = [k for k in item.forbidden_keywords if _contains(k)]

        hit_rate = (len(kw_hits) / len(item.keywords)) if item.keywords else 1.0
        # forbidden 1개당 -0.2 감점
        penalty = min(1.0, 0.2 * len(forbidden_hits))
        final = max(0.0, hit_rate - penalty)

        return ScoreResult(
            scorer=self.name,
            score=final,
            details={
                "keywords_total": len(item.keywords),
                "keywords_hit": kw_hits,
                "keywords_miss": [k for k in item.keywords if k not in kw_hits],
                "forbidden_hit": forbidden_hits,
                "hit_rate": round(hit_rate, 3),
                "penalty": round(penalty, 3),
            },
        )


# ── GlobalRulesScorer ─────────────────────────────────────────────────────
@dataclass
class GlobalRulesScorer:
    """답변에서 인용된 조항이 실제 DB에 존재하는지 검증.

    Iron Law (Eng review CRITICAL 2): DB miss 는 silent 0점이 아니라 명시 로깅."""
    name: str = "global_rules"

    def score(self, item: GoldItem, run: RunResult) -> ScoreResult:
        cites = _extract_citations(run.answer)
        invalid_std: list[tuple[str, str]] = []
        invalid_no: list[tuple[str, str]] = []
        valid: list[tuple[str, str]] = []
        db_miss_note = []

        known_standards = {s["standard"] for s in store.list_standards()}

        for std, no in cites:
            if std not in known_standards:
                invalid_std.append((std, no))
                continue
            row = store.get_paragraph(std, no)
            if row is None:
                invalid_no.append((std, no))
                db_miss_note.append(f"[{std}-{no}] 기준서 존재하지만 문단 없음 (DB 기준)")
            else:
                valid.append((std, no))

        total = len(cites)
        if total == 0:
            # 인용 없음 → 이 scorer는 중립 (cite scorer가 이미 reward 0으로 처리)
            return ScoreResult(
                scorer=self.name,
                score=1.0,
                details={"note": "인용 0건 — 규칙 위반 없음(cite scorer에서 감점)"},
            )

        bad = len(invalid_std) + len(invalid_no)
        final = max(0.0, 1.0 - (bad / total))

        return ScoreResult(
            scorer=self.name,
            score=final,
            details={
                "total_cites": total,
                "invalid_standard": invalid_std,
                "invalid_paragraph_no": invalid_no,
                "valid": valid,
                "db_miss_log": db_miss_note,
            },
        )


ALL_SCORERS: list[Scorer] = [CiteScorer(), KeywordScorer(), GlobalRulesScorer()]
