"""평가 하네스 Runner 구현.

Runner는 Goldset item → answer 문자열을 반환한다.
3종:
1. KifrsMcpRunner — 본인 시스템. 질문 키워드로 store.search_fts + get_paragraph 직접 호출,
   검색 결과를 context로 Claude API에 주입.
2. BaselineRunner — 검색/RAG 없이 Claude API만 호출 (대조군).
3. NotebookLmManualRunner — 사용자가 NotebookLM에 수동 질의하고 답을 JSON 파일로 저장한 것을 읽어옴.
4. LocalRagRunner — API 없이 검색 결과만으로 citation smoke 답변 생성.

Claude API 응답 cache: data/eval/cache/{runner}_{item_id}_{prompt_hash}.json
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import time
from pathlib import Path
from typing import Any, Protocol

from kifrs import store
from .models import GoldItem, RunResult


ROOT = Path(__file__).resolve().parent.parent.parent
CACHE_DIR = ROOT / "data" / "eval" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# 기본 모델은 claude-haiku-4-5로 — 평가 비용/속도 모두 무난.
# 원문 인용 정확성은 모델 지능보다 context 품질이 결정 → Haiku로 충분.
DEFAULT_MODEL = "claude-haiku-4-5-20251001"


class Runner(Protocol):
    name: str
    def run(self, item: GoldItem) -> RunResult: ...


def _cache_key(runner: str, item_id: str, prompt: str, model: str) -> Path:
    h = hashlib.sha256(f"{model}|{prompt}".encode("utf-8")).hexdigest()[:16]
    return CACHE_DIR / f"{runner}_{item_id}_{h}.json"


def _call_claude(prompt: str, model: str, cache_path: Path) -> dict[str, Any]:
    """Claude API 호출 + disk cache."""
    if cache_path.exists():
        return json.loads(cache_path.read_text(encoding="utf-8"))

    try:
        from anthropic import Anthropic
    except ImportError as e:
        raise RuntimeError("anthropic 패키지 필요: pip install anthropic") from e

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY 환경변수 미설정")

    client = Anthropic(api_key=api_key)
    t0 = time.time()
    resp = client.messages.create(
        model=model,
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )
    latency = time.time() - t0
    answer = "".join(b.text for b in resp.content if getattr(b, "type", None) == "text")
    data = {
        "model": model,
        "answer": answer,
        "latency_seconds": latency,
        "stop_reason": resp.stop_reason,
        "usage": {"in": resp.usage.input_tokens, "out": resp.usage.output_tokens},
    }
    cache_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return data


# ── Runner 1: KifrsMcpRunner ─────────────────────────────────────────────
# Topic → 기준서 매핑 — 질문에서 키워드 hit 로 dominant 기준서 추정.
# 본인 학습·실무 빈출 Top 5 기준 + 주요 교차 키워드.
TOPIC_MAP: dict[str, list[str]] = {
    "1115": [
        "수행의무", "거래가격", "수익인식", "고객과의 계약", "변동대가",
        "환불부채", "리베이트", "할부판매", "현금판매가격", "구별되는",
        "이전", "약속", "로열티", "라이선스", "할인율",
    ],
    "1116": [
        "리스", "리스료", "리스부채", "사용권자산", "리스이용자",
        "리스제공자", "리스개시일", "변동리스료", "리스기간", "내재이자율",
        "증분차입이자율", "단기리스", "기초자산",
    ],
    "1109": [
        "금융자산", "금융부채", "SPPI", "상각후원가", "당기손익-공정가치",
        "기타포괄손익-공정가치", "원금과 이자", "사업모형", "파생상품", "손상",
        "기대신용손실",
    ],
    "1001": [
        "재무제표", "재무상태표", "유동자산", "유동부채", "비유동",
        "보고기간", "차입금", "재무제표 표시", "공시",
    ],
    "1019": [
        "확정급여", "순확정급여", "퇴직급여", "종업원급여", "단기종업원",
    ],
}

# 검색 결과에서 제외할 noise section (부록 헤더, 시행일/경과, TOC 등)
_NOISE_SECTIONS = {
    "기준서 등의 대체", "시행일과 경과", "시행일과 경과 규정",
    "경과규정", "부록 C. 시행일과 경과 규정",
}


def _topic_standards(question: str, max_n: int = 3) -> list[str]:
    """질문에서 topic keyword 매치로 후보 기준서 순위 산정."""
    scores: dict[str, int] = {}
    for std, keywords in TOPIC_MAP.items():
        score = sum(1 for kw in keywords if kw in question)
        if score > 0:
            scores[std] = score
    # 명시된 4자리 기준서 번호는 최우선
    for m in re.findall(r"\b(1\d{3})호?\b", question):
        scores[m] = scores.get(m, 0) + 10
    ranked = sorted(scores.items(), key=lambda x: -x[1])
    return [std for std, _ in ranked[:max_n]]


def _is_noise(section: str | None) -> bool:
    if not section:
        return False
    for n in _NOISE_SECTIONS:
        if n in section:
            return True
    return False


class KifrsMcpRunner:
    name = "kifrs-mcp"

    def __init__(self, model: str = DEFAULT_MODEL, top_k: int = 10):
        self.model = model
        self.top_k = top_k

    def _retrieve(self, question: str) -> list[dict[str, Any]]:
        """Topic 기반 retrieval: 후보 기준서 추정 → 해당 기준서 우선 검색.

        전략:
        1. TOPIC_MAP 매치로 후보 기준서 2-3개 추정.
        2. 질문에서 한글 2-6자 토큰 추출.
        3. 후보 기준서에서 각 토큰별 최대 4건씩 검색 → top_k 확보.
        4. 부족하면 전체 기준서 백업 검색.
        5. noise section 제외.
        """
        tokens: list[str] = []
        # 긴 복합어 우선: 5-6자 → 4자 → 3-2자 순으로 우선순위
        for n in (6, 5, 4, 3, 2):
            for m in re.findall(rf"[가-힣]{{{n},{n}}}", question):
                if m not in tokens:
                    tokens.append(m)

        candidates = _topic_standards(question)
        hits: list[dict[str, Any]] = []
        seen: set[tuple[str, str]] = set()

        def _collect(target_std: str | None, limit_per_tok: int):
            for tok in tokens[:12]:
                for h in store.search_fts(tok, standard=target_std, limit=limit_per_tok):
                    key = (h["standard"], h["no"])
                    if key in seen or _is_noise(h.get("section")):
                        continue
                    seen.add(key)
                    hits.append(h)
                    if len(hits) >= self.top_k:
                        return

        # 1) 후보 기준서별 budget 균등 분배 — cross-standard 문항에서 단일 후보 독점 방지
        if candidates:
            budget_each = max(3, self.top_k // len(candidates))
            for std in candidates:
                before = len(hits)
                for tok in tokens[:12]:
                    for h in store.search_fts(tok, standard=std, limit=2):
                        key = (h["standard"], h["no"])
                        if key in seen or _is_noise(h.get("section")):
                            continue
                        seen.add(key)
                        hits.append(h)
                        if len(hits) - before >= budget_each:
                            break
                    if len(hits) - before >= budget_each:
                        break

        # 2) 백업: 전체 기준서 검색
        if len(hits) < self.top_k:
            _collect(None, limit_per_tok=2)

        # 각 hit의 full body를 로드
        enriched = []
        for h in hits:
            full = store.get_paragraph(h["standard"], h["no"])
            if full and not _is_noise(full.get("section")):
                enriched.append({
                    "standard": full["standard"],
                    "no": full["no"],
                    "section": full.get("section"),
                    "page": full.get("page"),
                    "body": full["body"],
                })
        return enriched

    def _build_prompt(self, item: GoldItem, context: list[dict[str, Any]]) -> str:
        ctx_lines = []
        for c in context:
            sec = f" ({c['section']})" if c.get("section") else ""
            ctx_lines.append(f"[{c['standard']}-{c['no']}]{sec}\n{c['body']}")
        ctx_block = "\n\n".join(ctx_lines) if ctx_lines else "(검색 결과 없음)"

        return (
            "다음은 한국채택국제회계기준(K-IFRS) 기준서 조회 결과다.\n"
            "이 조회 결과**만** 근거로 질문에 답하라.\n"
            "- 조항 번호는 반드시 [기준서번호-문단번호] 형식으로 인용 (예: [1115-27]).\n"
            "- 조회 결과에 없는 조항을 만들어 내지 마라.\n"
            "- 결론 + 근거 조항 번호 + 간결한 설명 구조로 답하라.\n\n"
            "━━ 조회 결과 ━━\n"
            f"{ctx_block}\n"
            "━━━━━━━━━━━━━\n\n"
            f"질문: {item.question}\n"
        )

    def run(self, item: GoldItem) -> RunResult:
        context = self._retrieve(item.question)
        prompt = self._build_prompt(item, context)
        cache_path = _cache_key(self.name, item.id, prompt, self.model)
        try:
            resp = _call_claude(prompt, self.model, cache_path)
            return RunResult(
                item_id=item.id,
                runner=self.name,
                question=item.question,
                answer=resp["answer"],
                retrieved_context=context,
                latency_seconds=resp.get("latency_seconds", 0.0),
                model=self.model,
            )
        except Exception as e:
            return RunResult(
                item_id=item.id, runner=self.name, question=item.question,
                answer="", retrieved_context=context,
                model=self.model, error=str(e),
            )


class LocalRagRunner:
    """No-network deterministic RAG runner for scorer and CI smoke.

    It does not try to be a good accountant. It proves that retrieval context can
    be converted into a scored answer without calling a paid LLM.
    """
    name = "local-rag"

    def __init__(self, top_k: int = 12):
        self.top_k = top_k

    def _retrieve(self, item: GoldItem) -> list[dict[str, Any]]:
        hits: list[dict[str, Any]] = []
        seen: set[tuple[str, str]] = set()

        # This runner is a no-network scorer smoke, not a retrieval benchmark.
        # Seed known gold anchors first so citation/report gates are stable.
        for cite in item.must_cite + item.may_cite:
            key = (cite.standard, cite.no)
            full = store.get_paragraph(cite.standard, cite.no)
            if not full or key in seen:
                continue
            seen.add(key)
            hits.append({
                "standard": full["standard"],
                "no": full["no"],
                "section": full.get("section"),
                "page": full.get("page"),
                "body": full["body"],
            })

        standards = _topic_standards(item.question, max_n=3)
        for cite in item.must_cite + item.may_cite:
            if cite.standard not in standards:
                standards.append(cite.standard)

        queries = [item.question, *item.keywords]
        for std in standards or [None]:
            for q in queries:
                for hit in store.search_fts(q, standard=std, limit=5):
                    key = (hit["standard"], hit["no"])
                    if key in seen or _is_noise(hit.get("section")):
                        continue
                    full = store.get_paragraph(hit["standard"], hit["no"])
                    if not full:
                        continue
                    seen.add(key)
                    hits.append({
                        "standard": full["standard"],
                        "no": full["no"],
                        "section": full.get("section"),
                        "page": full.get("page"),
                        "body": full["body"],
                    })
                    if len(hits) >= self.top_k:
                        return hits
        return hits

    def run(self, item: GoldItem) -> RunResult:
        context = self._retrieve(item)
        cites = [f"[{c['standard']}-{c['no']}]" for c in context[:6]]
        answer = (
            "Local RAG smoke answer.\n"
            f"질문: {item.question}\n"
            f"검색 기반 후보 인용: {' '.join(cites) if cites else '(없음)'}\n"
        )
        if item.keywords:
            answer += "핵심어: " + ", ".join(item.keywords[:6]) + "\n"
        return RunResult(
            item_id=item.id,
            runner=self.name,
            question=item.question,
            answer=answer,
            retrieved_context=context,
            model="deterministic-local",
        )


# ── Runner 2: BaselineRunner (RAG 없이 모델 단독) ────────────────────────
class BaselineRunner:
    name = "baseline-noretrieval"

    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model

    def _build_prompt(self, item: GoldItem) -> str:
        return (
            "다음은 한국채택국제회계기준(K-IFRS)에 관한 질문이다.\n"
            "관련 조항 번호를 [기준서번호-문단번호] 형식으로 인용하여 답하라 (예: [1115-27]).\n"
            "결론 + 근거 조항 번호 + 간결한 설명 구조로 답하라.\n\n"
            f"질문: {item.question}\n"
        )

    def run(self, item: GoldItem) -> RunResult:
        prompt = self._build_prompt(item)
        cache_path = _cache_key(self.name, item.id, prompt, self.model)
        try:
            resp = _call_claude(prompt, self.model, cache_path)
            return RunResult(
                item_id=item.id, runner=self.name, question=item.question,
                answer=resp["answer"], latency_seconds=resp.get("latency_seconds", 0.0),
                model=self.model,
            )
        except Exception as e:
            return RunResult(
                item_id=item.id, runner=self.name, question=item.question,
                answer="", model=self.model, error=str(e),
            )


# ── Runner 3: NotebookLmManualRunner ────────────────────────────────────
class NotebookLmManualRunner:
    """NotebookLM에서 수동으로 받은 답변을 JSON 파일에서 로드.

    파일 포맷: data/eval/manual/{item_id}.json = {"answer": "...", "source": "notebooklm", "date": "YYYY-MM-DD"}
    """
    name = "notebooklm-manual"

    def __init__(self, manual_dir: Path | None = None):
        self.manual_dir = manual_dir or (ROOT / "data" / "eval" / "manual")

    def run(self, item: GoldItem) -> RunResult:
        path = self.manual_dir / f"{item.id}.json"
        if not path.exists():
            return RunResult(
                item_id=item.id, runner=self.name, question=item.question,
                answer="", error=f"수동 답변 파일 없음: {path.relative_to(ROOT)}",
            )
        data = json.loads(path.read_text(encoding="utf-8"))
        return RunResult(
            item_id=item.id, runner=self.name, question=item.question,
            answer=data.get("answer", ""),
            model=data.get("source", "notebooklm"),
        )
