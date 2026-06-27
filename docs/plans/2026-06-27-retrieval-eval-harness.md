# Plan — M1: Retrieval Eval Harness

> Horizon: 검색 파이프라인 고도화 (rag-goldstandard) · Milestone: M1 (active, P0)
> 작성: 2026-06-27 · 장부 정본: 이 trees 는 픽업용, step 실시간 상태는 본 문서 체크박스

## Scope (이번 horizon)

검색 단계를 *답변 생성 없이* 정량 측정하는 장치를 세운다. goldset `must_cite`(정답 문단)를 ground truth로 써서, lexical/semantic/hybrid 각각이 정답 문단을 top-k에 넣는지 recall@k·MRR·nDCG로 잰다. API·LLM 불필요(로컬 검색 함수만 호출). 이 하네스가 M2~M4의 before/after 게이트가 된다.

## 중단점

- M1-1 + M1-2 완료(evaluator + 8문항 baseline 숫자) = 이번 run 의 검증 가능 체크포인트
- M1-3(goldset 8→50)은 dogfood 검증 인용 수확이 필요한 큰 작업 → 다음 chunk

## Step 트리

- [x] **M1-1 — retrieval-only evaluator** (`kifrs/eval/retrieval.py`) ✅ 2026-06-27
  - 읽기: `kifrs/eval/models.py`(GoldItem·Citation), `kifrs/embed.py`(semantic_search·search_hybrid), `kifrs/store.py`(search_fts)
  - 작업: goldset 로드 → 각 문항을 3 retriever(lexical/semantic/hybrid)로 top-K 검색 → `must_cite (std,no)` 대비 recall@{1,3,5,10,20}·MRR·nDCG@10 계산 → goldset 평균 집계 → 비교표 출력 + JSON 저장(`data/eval/results/retrieval_<date>.json`)
  - 매칭: 정답 `(standard, str(no))` 가 retrieved 결과에 정확히 등장하면 hit
  - AC: `python -m kifrs.eval.retrieval --k 20` 가 3 retriever × 메트릭 표를 에러 없이 출력
  - 금지: 답변 생성/LLM 호출 금지(이유: API 의존이 M1 전제 위반). numpy 외 신규 의존성 금지
- [x] **M1-2 — 8문항 baseline 숫자 확정** ✅ 2026-06-27
  - 결과 (K=20): lexical `recall@20=0.000` / semantic = hybrid `recall@20=0.667 · MRR=0.440 · nDCG@10=0.396`
  - **발견 1**: `search_fts`는 full 질문(긴 문장)에 0 hits (FTS5 trigram 전 토큰 AND). 키워드형 쿼리에만 작동 → lexical은 query 가공 전제. **M3(query expansion) 동기 확정**
  - **발견 2**: full-question에서 hybrid는 semantic 대비 lift 0 (lexical 0 기여 → RRF 무효). hybrid 이득은 키워드 쿼리에서만
  - **miss**: Q001(1115-27), Q005(1115-60/61/63), Q006(1115-51), Q008(1109-2.1·1116-26)
  - 리포트: `data/eval/results/retrieval_20260627_152718.json` (gitignored)
- [ ] **M1-3 — goldset 8→50 확장** (다음 chunk)
  - dogfood(cpa2 q01~q08, textbook, 1109/1116 시나리오)의 검증된 인용을 goldset 항목으로 수확. 메타데이터(standard·no·keywords)만 — 원문 텍스트 commit 금지(저작권)
- [ ] **M1-4 — 50문항 baseline 확정**
  - 확장 goldset에 재실행 → 통계적으로 의미 있는 baseline 확정 → M2 리랭킹 진입 게이트 오픈

## DoD (milestone)

evaluator가 goldset을 돌려 baseline 숫자를 리포트로 산출 + goldset 50문항. → `roadmap_sync.py complete --milestone M1`
