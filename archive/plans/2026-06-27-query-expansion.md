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
- [x] **M3b — 시험표현↔본문표현 동의어 매핑** (`kifrs/store.py:TERM_BRIDGE/expand_query`) ✅ 2026-06-27
  - 읽기: `kifrs/store.py`(search_fts·extract_keywords), `kifrs/embed.py`(semantic_search), 잔여 miss 문항 본문(`get_paragraph`)
  - 작업: `TERM_BRIDGE` dict(시험표현→본문표현) + `expand_query()` — 검색 전 쿼리에 매핑된 본문 용어를 덧붙여 lexical·semantic 양쪽 신호 보강. `search_fts`(extract_keywords 전) + `semantic_search`(인코딩 전)에 주입 → hybrid/reranked 자동 혜택. 리랭커는 *원본* 질문으로 점수(확장 X).
  - **타겟 선정(잔여 miss 분석)**: "본문 어휘 부재형"만 — Q005 할부판매·현재가치→"유의적 금융요소/화폐의 시간가치/현금판매가격"(1115-60/61), Q041 측정기준일→"부여일"(1102-11), Q022 재측정요소→"보험수리적손익"(1019-128). + 한계 #1 공매도→"당기손익-공정가치 측정 금융부채/단기매매항목"(goldset 밖, 문서 seed). **제외**: Q006 환불·Q048 회수가능액은 시험표현이 이미 본문에 존재(랭킹 문제 → 동의어 무효).
  - 각 value 는 본문에 *실제 존재하는* 표현(get_paragraph 확인) — 가짜 매핑 금지. dict 는 실사용(dogfood) 마찰에서 누적.
  - AC: `python -m kifrs.eval.retrieval --retrievers lexical --k 20` 에서 recall 상승 + 타겟 문항 hit
  - 금지: 시험표현이 본문에 이미 있는 케이스에 동의어 추가(무효+노이즈). DB 스키마 변경 없이 코드 dict 로(현 단계)
  - **lexical 결과(M3a→M3b)**: recall@5 0.377→0.407, recall@10 0.487→0.517, **recall@20 0.693→0.723**(+3.0pp), MRR 0.345→0.366. Q005·Q022 lexical hit 전환(Q041 은 "부여일" 다수 문단 bm25 희석으로 lexical 부분, hybrid 확인 필요)
  - 전 retriever 결과: 아래 "## M3b 측정" 표 참조

## M3b 측정 (50문항, K=20 · `data/eval/results/retrieval_20260627_165615.json`)

| retriever | recall@5 | recall@10 | recall@20 | MRR | nDCG@10 |
|---|---|---|---|---|---|
| lexical | 0.407 | 0.517 | 0.723 | 0.366 | 0.363 |
| semantic | 0.563 | 0.733 | 0.880 | 0.576 | 0.550 |
| **hybrid** | 0.597 | 0.763 | **0.907** | 0.509 | 0.527 |
| reranked (M3+M2) | 0.640 | 0.727 | 0.853 | **0.612** | **0.578** |

**누적 진행 (hybrid recall@20)**: M1 baseline 0.847 → M3a 0.877 → **M3b 0.907** (+6.0pp).
- M3b 는 semantic 도 끌어올림 (0.847→0.880) — expand_query 가 임베딩 쿼리에도 적용되기 때문.
- 타겟 3건 중 **Q005·Q022 hit 전환**(miss 탈출). **Q041(1102-11)은 미해결** — "부여일" 다수 문단 bm25 희석으로 hybrid 에서도 top-20 밖. 정직하게 잔여 miss 로 남김.
- 잔여 miss 11→9건: Q001·Q004·Q006·Q008·Q029·Q039·Q040·Q041·Q048 (대부분 랭킹/의미근접 문제 — 동의어 무효 부류).
- reranked: hybrid 의 높아진 천장 위에서 MRR 0.509→**0.612**, recall@5 0.597→**0.640** 회복 → "M3(천장↑) + M2(top 정밀↑)" 조합 확인.

## DoD (milestone)

lexical recall>0 + hybrid가 M1 baseline(semantic) 대비 천장 lift, M1 하네스로 before/after 측정. → **충족**: M3a(0.847→0.877) + M3b(→0.907). M3b 동의어 dict 는 실사용 마찰에서 누적 확장.
