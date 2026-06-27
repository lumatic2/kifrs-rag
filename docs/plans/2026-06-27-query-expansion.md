# Plan — M3: Query 가공 / 용어 브리지 (query expansion)

> Horizon: 검색 파이프라인 고도화 (rag-goldstandard) · Milestone: M3 (active, P0)
> 작성: 2026-06-27 · 장부 정본: 이 트리는 픽업용, step 실시간 상태는 본 문서 체크박스 + ROADMAP marker

## Scope (이번 horizon)

M1 baseline에서 `lexical=0.000`(구조적). FTS5 trigram이 full 질문(긴 문장)의 전 토큰을 AND로 묶어 0 hits → RRF가 두 신호가 아닌 semantic 단일 신호로 동작. 천장(recall@20)을 올리는 정공법은 1차 검색(BM25)을 부활시키는 것. M3는 두 갈래:
- **M3a** — 쿼리 정상화: 질문에서 키워드 추출 → FTS5 OR(bm25 정렬) → lexical 부활 → RRF에 실제 두 신호.
- **M3b** — 용어 브리지: 시험표현↔본문표현 동의어 매핑(한계 #1 "공매도") + user_note. 검색 전 쿼리에 동의어 확장.

## 중단점

- M3a 완료(lexical>0 + hybrid가 semantic 대비 천장 lift) = 이번 run 의 검증 가능 체크포인트
- M3b(동의어 매핑)는 curatorial 작업(시험표현↔본문표현 페어 수집) → M3a 결과 본 뒤 별도 chunk

## Step 트리

- [x] **M3a — 쿼리 정상화로 lexical 부활** (`kifrs/store.py`) ✅ 2026-06-27
  - 읽기: `kifrs/store.py`(search_fts·_like_snippet), `kifrs/embed.py`(search_hybrid RRF), `kifrs/eval/retrieval.py`(측정 진입점)
  - 작업: `extract_keywords()` 추가(한글 어절 조사 strip + 불용어 제거, **신규 의존성 없음** — konlpy/mecab은 Windows/Smart App Control 마찰) → `search_fts`를 키워드 OR + `ORDER BY rank`(bm25)로 재작성 → LIKE fallback을 AND→키워드 hit count 스코어로 완화. ≥3자만 FTS5 MATCH(trigram 제약), 나머지는 fallback.
  - AC: `python -m kifrs.eval.retrieval --retrievers lexical --k 20` 에서 lexical recall@20 > 0
  - 금지: 신규 ML 의존성 추가 금지(이유: Windows CUDA DLL/네이티브 빌드 마찰). search_hybrid/MCP 시그니처 변경 금지(search_fts 내부만 고쳐 전 caller 자동 혜택)
  - **결과 (50문항, K=20)**:
    | retriever | recall@5 | recall@10 | recall@20 | MRR | nDCG@10 |
    |---|---|---|---|---|---|
    | lexical (before) | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
    | **lexical (after)** | 0.377 | 0.487 | **0.693** | 0.345 | 0.340 |
    | semantic | 0.557 | 0.720 | 0.847 | 0.555 | 0.538 |
    | **hybrid (after)** | 0.583 | 0.733 | **0.877** | 0.499 | 0.509 |
  - **발견**: ① lexical 부활(0→0.693). ② hybrid 천장 0.847→**0.877**(+3.0pp), @5/@10/@20 모두 semantic 대비 lift. ③ hybrid MRR 0.555→0.499 하락 = RRF top-noise tradeoff(lexical top-rank 노이즈). **이 top-precision 손실은 M2 리랭커가 정확히 메우는 부분** → "M3 먼저(천장↑), M2 나중(top 정밀↑)" 순서 재확인.
  - 리포트: `data/eval/results/retrieval_20260627_162640.json` (gitignored)
- [ ] **M3b — 시험표현↔본문표현 동의어 매핑** (다음 chunk)
  - 한계 #1 "공매도"(Q005류) 등 본문 부재 키워드를 본문 표현으로 확장. user_note 테이블 활용 검토.
  - M3a 후 잔여 miss(Q005 1115-60/61/63, Q006 1115-51, Q008 1109-2.1, Q040 1109-4.1.4 등)에서 "본문 어휘 부재형"을 식별해 매핑 대상 선정.

## DoD (milestone)

lexical recall>0 + hybrid가 M1 baseline(semantic) 대비 천장 lift, M1 하네스로 before/after 측정. → M3a로 충족(천장 0.847→0.877). M3b는 잔여 본문-부재 miss 타겟(옵션 확장).
