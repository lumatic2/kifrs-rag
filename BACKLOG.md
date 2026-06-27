# BACKLOG

> Compressed milestone archive. ROADMAP.md is capped at 150 lines.

## Completed

### 2026-06 — 검색 파이프라인 고도화 (Current Horizon)
- M1 — 측정 기반 구축 (Retrieval Eval Harness)
  - Completed: 2026-06-27
  - Result: retrieval-only evaluator(recall@k·MRR·nDCG, API 不要)가 goldset을 lexical/semantic/hybrid로 돌려 baseline 산출. goldset 8→50 확장. Baseline(50문항,K=20): semantic=hybrid recall@5=0.557/@10=0.720/@20=0.847, MRR=0.555, nDCG@10=0.538
  - Evidence: `kifrs/eval/retrieval.py` + `data/eval/results/retrieval_20260627_154807.json` + `data/eval/goldset.json`(50문항, must_cite 50/50 DB 검증)
  - Plan: `docs/plans/2026-06-27-retrieval-eval-harness.md`

- M3 — Query 가공 / 용어 브리지 (천장 상승)
  - Completed: 2026-06-27
  - Result: hybrid recall@20 0.847 → M3a 0.877(lexical 0→0.693 부활) → M3b 0.907(+6.0pp 누적). M3b 동의어로 Q005·Q022 hit 전환. reranked(M3+M2) recall@5=0.640/MRR=0.612
  - Evidence: data/eval/results/retrieval_20260627_165615.json
  - Plan: `docs/plans/2026-06-27-query-expansion.md`

- M2 — Cross-encoder 리랭킹 프로덕션 wiring
  - Completed: 2026-06-27
  - Result: search_reranked MCP tool + 리랭커 warmup(데몬 스레드) + /accounting SKILL.md 정밀 인용 1순위. GPU per-query 0.44s로 인터랙티브 viable
  - Evidence: kifrs/mcp_server.py
  - Plan: `docs/plans/2026-06-27-rerank-production-wiring.md`

---

## Phase 이력 (Phase 1~4, 콘텐츠·시나리오 축 — 2026-04~05 압축)

### Phase 1 — PoC ✅ (2026-04-14)
인프라 구축. tax-agent 패턴 재사용 + KASB 일괄 다운로더 + 파서 + SQLite + FastMCP.
- 100 기준서(K-IFRS 63 + 일반기업회계기준 36 + special 1) / **8,328 paragraphs**(2026-04-24 letter-suffix 616건 복구 포함)
- SQLite DB 29MB + paragraph_fts(trigram + LIKE fallback). FastMCP tools 7종. /accounting 스킬 + dogfood 10건 통과. goldset 8문항(Q001~Q008)

### Phase 2 — 시험 수준 검증 ✅ 졸업 (2026-04-28)
목표: 회계사 2차 기출 정확도 80%+. **누적 86%(cpa2 5 + textbook 21)로 졸업**.
- Dogfood R1(2026-04-27): cpa2 5문항 풀이+직관 채점. 검색 실패 5건 식별
- 검색 품질 개선: bge-m3 임베딩(1024d, 8,328 인덱싱) + hybrid RRF(search_semantic/search_hybrid). 검색 실패 5건 중 3 완벽/1 부분/1 본문부재(공매도)
- 답변 포맷 유연화: SKILL.md §3 `(고정)`→`가치는 고정, 형태는 질문에 맞춘다`. 5 질문유형 매핑표
- Dogfood R2: hybrid 재풀이 → 검색 매칭 60%→80%. R3 mini: 계산형/서술형 두 형태 새 가이드 검증
- Textbook dogfood: 1102 6/6 + 1033 9/9 + 1116 6/6 = **21/21 100%**(모범답안 포함 정량)
- Baseline A/B: ch14 Engine 9/9 vs Naive Claude 5/9(+44%p). 엔진 우위 = 매 단계 본문 검증
- cpa2 정량 채점: q01 71%/q02 70%/q03 82%/q04 100%/q05 50% = 평균 75%(해석 인정 85%). q04 상법 영역도 본인 지식 정확. q05 IFRIC19[2119] 해석 약점

### Phase 3 — 실무 시나리오(1109 금융상품 분류·측정) ✅ 10/10 (2026-04-28)
신규 거래 입력 → 1109 분류 워크플로 자동 산출. `data/scenarios/1109_classification/`.
- WORKFLOW.md: §1 SPPI 결정트리 → §2 사업모형 4축 → §3 분류 매트릭스 → §4·5 분개 → §6 검토메모 7섹션
- 기본 분류 5건: AC / FVOCI(부채) / SPPI Fail→FVPL / FVOCI(자본·지분) / IFRIC19[2119] 자기지분 부채소멸
- 경계 케이스 5건: 변동금리 SPPI nuance[B4.1.9C] / 전환사채 발행자[1032-31]vs보유자[1109] / 재분류 6패턴[4.4.1] / FVPL 지정[4.1.5] / 외화채권 1109+1021
- 학습: 같은 SPPI Pass라도 사업모형이 분류 결정 / FVOCI 부채vs자본 처분 OCI 차이 / "측정 불가=대체 공정가치"

### Phase 4 — 시나리오 확장 + 누적 (2026-04-29~05-02, 진행 중 → 현재 콘텐츠 축)
- 1116 리스 WORKFLOW.md + template. 시나리오 1·2·5·9·10 완성(5/10):
  - 시1 단순 사무실(부채/자산 3,545,950) / 시2 복구의무+선급(자산 4,107,300, 1116+1037)
  - 시5 운용→금융 변경(textbook ch15 물음1, 6/6) / 시9 추가+축소 동시(q08 물음1, 분리트랙 정정, 모범답안 3/3) / 시10 기간연장(q08 물음2, 2/2)
- cpa2 q06(1019+1037) 풀이+채점: 직관 1/5 + 해석 인정 4/5 ≈ 80%(2026-05-02)
- 잔여 1116 시나리오: 3(단기·저가 면제) / 6(금융→금융) / 7(기간 재평가) / 8(매수선택권)
- 다른 도메인 미착수: 1115 수익 / 1113 공정가치(KICPA 부담 1위 27.08%) / user_note 활성화
