"""K-IFRS 문단 임베딩 — bge-m3 + SQLite BLOB + 하이브리드 검색.

사용:
    python -m kifrs.embed build                       # 전체 인덱싱
    python -m kifrs.embed build --standard 1115       # 특정 기준서만
    python -m kifrs.embed query "환매약정"             # 하이브리드 검색
    python -m kifrs.embed query "수익" --mode semantic
    python -m kifrs.embed stats                       # 인덱싱 현황

저작권 안전선: 모든 임베딩 추론은 로컬 (sentence-transformers + 로컬 모델).
외부 API 미사용 — KASB 본문이 외부로 나가지 않음.
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime
from typing import Any

import numpy as np

from .store import _conn, search_fts, expand_query

DEFAULT_MODEL = "BAAI/bge-m3"


# ── 모델 로드 (지연) ─────────────────────────────────────────────────────
import threading

_model_cache: dict[str, Any] = {}
_model_lock = threading.Lock()


def _log(msg: str) -> None:
    """stderr 로그 — MCP stdio 모드에서 stdout 충돌 방지."""
    print(msg, file=sys.stderr)


def _load_model(name: str = DEFAULT_MODEL):
    # 락 — 백그라운드 warmup 스레드와 첫 tool 호출이 겹쳐 모델을 이중 로드하지 않게.
    with _model_lock:
        if name not in _model_cache:
            from sentence_transformers import SentenceTransformer
            _log(f"[embed] loading model: {name}")
            _model_cache[name] = SentenceTransformer(name)
    return _model_cache[name]


def encode_texts(
    texts: list[str],
    model_name: str = DEFAULT_MODEL,
    batch_size: int = 32,
    show_progress: bool = True,
) -> np.ndarray:
    """문단·쿼리 텍스트 → L2-정규화된 float32 임베딩 행렬."""
    model = _load_model(model_name)
    vecs = model.encode(
        texts,
        normalize_embeddings=True,
        batch_size=batch_size,
        show_progress_bar=show_progress,
        convert_to_numpy=True,
    )
    return vecs.astype(np.float32)


# ── BLOB 직렬화 ──────────────────────────────────────────────────────────
def _vec_to_blob(v: np.ndarray) -> bytes:
    return v.astype(np.float32).tobytes()


# ── 인덱싱 ───────────────────────────────────────────────────────────────
def build_embeddings(
    standard: str | None = None,
    model_name: str = DEFAULT_MODEL,
    batch_size: int = 32,
) -> dict[str, Any]:
    """paragraph 테이블의 본문을 인코딩해 embedding 테이블에 upsert."""
    with _conn() as conn:
        q = "SELECT standard, no, body FROM paragraph"
        params: list[Any] = []
        if standard:
            q += " WHERE standard=?"
            params.append(standard)
        q += " ORDER BY standard, ord"
        rows = conn.execute(q, params).fetchall()

    if not rows:
        return {"indexed": 0, "model": model_name}

    texts = [r["body"] or "" for r in rows]
    _log(f"[embed] {len(texts):,} paragraphs → encoding with {model_name}")
    vectors = encode_texts(texts, model_name, batch_size, show_progress=True)
    dim = int(vectors.shape[1])
    now = datetime.now().isoformat(timespec="seconds")

    with _conn() as conn:
        conn.executemany(
            """
            INSERT INTO embedding (standard, no, model, dim, vector, indexed_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(standard, no, model) DO UPDATE SET
                dim=excluded.dim,
                vector=excluded.vector,
                indexed_at=excluded.indexed_at
            """,
            [
                (r["standard"], r["no"], model_name, dim, _vec_to_blob(v), now)
                for r, v in zip(rows, vectors)
            ],
        )
    return {"indexed": len(rows), "model": model_name, "dim": dim, "scope": standard or "all"}


# ── 검색 ────────────────────────────────────────────────────────────────
def semantic_search(
    query: str,
    standard: str | None = None,
    limit: int = 20,
    model_name: str = DEFAULT_MODEL,
) -> list[dict[str, Any]]:
    """쿼리 임베딩 vs 인덱스 cosine top-k.
    임베딩이 정규화돼 있어 cosine = dot product."""
    qvec = encode_texts([expand_query(query)], model_name, show_progress=False)[0]

    with _conn() as conn:
        q = """
            SELECT e.standard, e.no, e.dim, e.vector,
                   p.appendix, p.section, p.page, p.body
            FROM embedding e
            JOIN paragraph p ON p.standard = e.standard AND p.no = e.no
            WHERE e.model = ?
        """
        params: list[Any] = [model_name]
        if standard:
            q += " AND e.standard=?"
            params.append(standard)
        rows = conn.execute(q, params).fetchall()

    if not rows:
        return []

    dim = rows[0]["dim"]
    mat = np.frombuffer(
        b"".join(r["vector"] for r in rows), dtype=np.float32
    ).reshape(len(rows), dim)
    scores = mat @ qvec  # cosine (normalized)
    top_idx = np.argsort(-scores)[:limit]

    out = []
    for i in top_idx:
        r = rows[int(i)]
        body = r["body"] or ""
        out.append({
            "standard": r["standard"],
            "no": r["no"],
            "appendix": r["appendix"],
            "section": r["section"],
            "page": r["page"],
            "snippet": body[:160],
            "score": float(scores[int(i)]),
        })
    return out


def search_hybrid(
    query: str,
    standard: str | None = None,
    limit: int = 20,
    model_name: str = DEFAULT_MODEL,
    k: int = 60,
) -> list[dict[str, Any]]:
    """RRF (Reciprocal Rank Fusion) — lexical(FTS5) + semantic.

    score = sum(1 / (k + rank_i)) for each retriever that returned this item.
    k=60 은 RRF 표준 파라미터 (Cormack et al. 2009).
    """
    lex = search_fts(query, standard, limit=50)
    sem = semantic_search(query, standard, limit=50, model_name=model_name)

    rrf: dict[tuple[str, str], float] = {}
    for rank, r in enumerate(lex):
        key = (r["standard"], r["no"])
        rrf[key] = rrf.get(key, 0.0) + 1.0 / (k + rank)
    for rank, r in enumerate(sem):
        key = (r["standard"], r["no"])
        rrf[key] = rrf.get(key, 0.0) + 1.0 / (k + rank)

    # 메타 통합: lexical 우선, 없으면 semantic
    info: dict[tuple[str, str], dict[str, Any]] = {
        (r["standard"], r["no"]): r for r in lex
    }
    for r in sem:
        key = (r["standard"], r["no"])
        info.setdefault(key, r)

    sorted_keys = sorted(rrf, key=lambda kk: -rrf[kk])[:limit]
    return [{**info[kk], "rrf": rrf[kk]} for kk in sorted_keys]


# ── 리랭킹 (M2 — cross-encoder) ───────────────────────────────────────────
DEFAULT_RERANKER = "BAAI/bge-reranker-v2-m3"
_reranker_cache: dict[str, Any] = {}
_reranker_lock = threading.Lock()


def _load_reranker(name: str = DEFAULT_RERANKER):
    with _reranker_lock:
        if name not in _reranker_cache:
            from sentence_transformers import CrossEncoder
            _log(f"[rerank] loading reranker: {name}")
            _reranker_cache[name] = CrossEncoder(name, max_length=512)
    return _reranker_cache[name]


def search_reranked(
    query: str,
    standard: str | None = None,
    limit: int = 20,
    candidates: int = 50,
    model_name: str = DEFAULT_MODEL,
    reranker_name: str = DEFAULT_RERANKER,
) -> list[dict[str, Any]]:
    """1차 hybrid 로 candidates 개 후보를 뽑아 cross-encoder 로 재점수 → top-limit.

    골드 스탠다드 4단계(BM25+dense+RRF+rerank)의 마지막 단계.
    깊은 후보 풀(candidates)을 리랭킹해 천장(1차 recall@candidates)까지 활용.
    """
    pool = search_hybrid(query, standard, limit=candidates, model_name=model_name)
    if not pool:
        return []
    reranker = _load_reranker(reranker_name)
    # 리랭커는 truncated snippet 이 아닌 전체 본문에서 정확. 본문 fetch.
    from .store import get_paragraph
    pairs, metas = [], []
    for r in pool:
        row = get_paragraph(r["standard"], r["no"])
        body = (row or {}).get("body") or r.get("snippet") or ""
        pairs.append((query, body))
        metas.append(r)
    scores = reranker.predict(pairs)
    order = sorted(range(len(metas)), key=lambda i: -float(scores[i]))[:limit]
    return [{**metas[i], "rerank_score": float(scores[i])} for i in order]


# ── 운영 헬퍼 ────────────────────────────────────────────────────────────
def stats() -> dict[str, Any]:
    with _conn() as conn:
        total_para = conn.execute("SELECT COUNT(*) FROM paragraph").fetchone()[0]
        rows = conn.execute(
            "SELECT model, COUNT(*) AS n, MIN(indexed_at) AS first, MAX(indexed_at) AS last "
            "FROM embedding GROUP BY model"
        ).fetchall()
    return {
        "paragraphs_total": total_para,
        "models": [dict(r) for r in rows],
    }


# ── CLI ────────────────────────────────────────────────────────────────
def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(prog="kifrs.embed")
    sub = p.add_subparsers(dest="cmd", required=True)

    sb = sub.add_parser("build", help="paragraph → 임베딩 인덱스")
    sb.add_argument("--standard")
    sb.add_argument("--model", default=DEFAULT_MODEL)
    sb.add_argument("--batch-size", type=int, default=32)

    sq = sub.add_parser("query", help="임베딩 또는 하이브리드 검색")
    sq.add_argument("text")
    sq.add_argument("--standard")
    sq.add_argument("--limit", type=int, default=10)
    sq.add_argument("--mode", choices=["semantic", "hybrid"], default="hybrid")
    sq.add_argument("--model", default=DEFAULT_MODEL)

    sub.add_parser("stats", help="인덱싱 현황")

    args = p.parse_args(argv)

    if args.cmd == "build":
        info = build_embeddings(args.standard, args.model, args.batch_size)
        print(f"[ok] {info}")
    elif args.cmd == "query":
        if args.mode == "semantic":
            results = semantic_search(args.text, args.standard, args.limit, args.model)
        else:
            results = search_hybrid(args.text, args.standard, args.limit, args.model)
        for r in results:
            score = r.get("score") or r.get("rrf", 0.0)
            print(f"  [{r['standard']}-{r['no']}] {score:.4f} | {r.get('section') or '-'} | {r['snippet'][:90]}")
    elif args.cmd == "stats":
        info = stats()
        print(info)


if __name__ == "__main__":
    main()
