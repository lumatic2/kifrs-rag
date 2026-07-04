"""런타임 citation 존재 검증 (RGA1 — 1109 grounding.py 미러).

결정 엔진의 reasons 문자열에 하드코딩된 조항 인용(예: `[1116-24]`)이 실제 DB에 존재하는 조항을
가리키는지 검증한다. `kifrs.store`를 직접 import한다(MCP 프로토콜 경유 아님) — 엔진은 같은
프로세스 내부 코드이므로 프로세스 경계를 넘는 MCP 레이어가 필요 없다
(docs/horizons/rag-agent-integration.md 결정).

의미적 일치 검증(reason 문구가 조항 내용과 부합하는지)은 RGA1 범위에서 제외됐다 — keyword
overlap·cosine 유사도·cross-encoder 리랭커 실측 결과 정답/오답을 신뢰성 있게 구분하지 못했다
(docs/plans/2026-07-03-rga1-runtime-citation-grounding.md 결정 로그 참조).
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from kifrs.store import get_paragraph

_CITATION_BLOCK = re.compile(r"\[([^\]]+)\]")
_STD_PREFIX = re.compile(r"^(\d{4})-(.+)$")
_SUBCLAUSE = re.compile(r"\([a-z]\)$")


@dataclass
class CitationCheck:
    token: str
    standard: str
    base_no: str
    exists: bool


def extract_citations(reason: str) -> list[str]:
    """reason 문자열의 `[1116-...]` 블록에서 `표준-조항` 토큰 리스트를 추출한다."""
    tokens: list[str] = []
    for block in _CITATION_BLOCK.findall(reason):
        m = _STD_PREFIX.match(block.strip())
        if not m:
            continue
        standard, body = m.group(1), m.group(2)
        for item in body.split(","):
            for alt in item.split("/"):
                token = alt.strip()
                if token:
                    tokens.append(f"{standard}-{token}")
    return tokens


def _base_paragraph_no(token: str) -> str:
    """`46(a)` -> `46`, `23~24` -> `23` (범위 시작점·알파 하위조항 제거 후 조회)."""
    no = token.split("-", 1)[1]
    no = no.split("~", 1)[0]
    return _SUBCLAUSE.sub("", no)


def verify_citation_exists(token: str) -> CitationCheck:
    standard, _ = token.split("-", 1)
    base_no = _base_paragraph_no(token)
    row = get_paragraph(standard, base_no)
    return CitationCheck(token=token, standard=standard, base_no=base_no, exists=row is not None)


class GroundingFailure(Exception):
    def __init__(self, reason: str, token: str):
        self.reason = reason
        self.token = token
        super().__init__(f"citation not found in DB: {token!r} (reason: {reason!r})")


def ground_reasons(reasons: list[str]) -> None:
    """reasons 리스트의 모든 인용이 DB에 존재하는지 검증한다. 실패 시 `GroundingFailure`."""
    for reason in reasons:
        for token in extract_citations(reason):
            check = verify_citation_exists(token)
            if not check.exists:
                raise GroundingFailure(reason, token)
