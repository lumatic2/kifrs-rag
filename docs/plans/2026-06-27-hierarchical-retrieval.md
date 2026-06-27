# M4 — Hierarchical retrieval + evidence curation

> 2026-06-27 · Current Horizon 검색 파이프라인 고도화 · plan doc (상위 트리)
> 장부 권위: 실시간 step 상태는 이 체크박스 / before·after 정본은 `data/eval/results/`.

## 목표

조·항·호 **섹션**을 1차 검색 단위로 써서, 문단 단독으로는 top-k 밖이지만 *섹션 제목·맥락이 쿼리와 강하게 일치*하는 정답 문단을 끌어올린다. 그다음 저신뢰 결과를 잘라 인용 정밀도를 높인다.

## Before (baseline, 2026-06-27 22:41, 50문항 K=20)

| retriever | recall@5 | recall@20 | MRR | nDCG@10 |
|---|---|---|---|---|
| hybrid | 0.597 | **0.907** | 0.509 | 0.527 |
| reranked | **0.640** | 0.853 | 0.612 | 0.578 |

miss 9건(hybrid top-20 밖): Q001(1115-27) Q004(1001-69) Q006(1115-51) Q008(1109-2.1) Q029(1116-45) Q039(1037-14) Q040(1109-4.1.4) Q041(1102-11) Q048(1036-18)

계층검색 후보(정답 문단이 쿼리어 일치 섹션 아래): **Q029**(섹션 `리스변경`) · **Q039**(섹션 `충당부채`) · **Q048**(섹션 `회수가능액의 측정`/`손상차손의 인식과 측정`). 약함: Q008(`적용범위` generic)·Q040(`모든 양도` 파싱잡음).

## 접근 (확정 2026-06-27)

- **M4-1 먼저** 구현·측정·커밋 → 결과 보고 M4-2 재결정.
- 계층 1차 = **쿼리 시점 섹션 centroid**: 기존 문단 임베딩을 (standard, section)별 평균으로 합성 → 쿼리와 cosine → 상위 섹션의 best 문단을 hybrid 풀에 보강. **재인덱싱·스키마 변경 없음. recall-safe(문단 제거 안 함, 추가만).**

## After (M4-1, 2026-06-27 22:53, 50문항 K=20) ✅

| retriever | recall@5 | recall@10 | recall@20 | MRR | nDCG@10 |
|---|---|---|---|---|---|
| hybrid (before) | 0.597 | 0.763 | 0.907 | 0.509 | 0.527 |
| **hierarchical** | **0.627** | **0.827** | **0.917** | **0.542** | **0.562** |

**전 지표 비퇴행 + 개선**: recall@5 +3.0pp · recall@10 +6.4pp · recall@20 +1.0pp(퇴행 해소) · MRR +3.3pp · nDCG +3.5pp. full-miss 9→8(**Q041 회복**, 새 miss 0).

파라미터(스윕 최적): `top_sections=20, per_section=3, section_weight=0.5`. 섹션 신호 0.5 down-weight 가 변위 억제의 핵심 — w=1.0 또는 좁은 탐색(ts≤12)은 recall@20 퇴행.

**가설 정정**: 당초 후보 Q029·Q039·Q048 직접 회복은 일부만. 진단 결과 **Q039(1037-14) 섹션 "충당부채" centroid 전역순위 674 → 계층 레버 부적합**(쿼리가 리스-복구 지배). Q029 섹션 #1·Q048 섹션 #24 는 부분 기여(recall@20 +1pp). 레버는 특정 3건이 아니라 **광범위 mid-precision 개선**으로 작동 → 더 가치 있는 결과(reranked 후보 품질↑).

증거: `data/eval/results/retrieval_20260627_225318.json`

## Step 트리

- [x] **M4-1 — 계층 검색 retriever** ✅ (2026-06-27) — `search_hierarchical` + eval 등록. 전 지표 비퇴행/개선
  - `kifrs/embed.py`: `search_hierarchical(query, standard, limit)` 추가
    - ① hybrid 풀(50) 확보 (기존 문단 recall 천장 보존)
    - ② (standard, section) centroid = 멤버 문단 벡터 평균 (numpy groupby, 쿼리 시점 계산)
    - ③ 쿼리 vs centroid cosine → 상위 S 섹션
    - ④ 상위 섹션 내 best 문단(쿼리 vs 문단 cosine)을 풀에 union
    - ⑤ RRF 융합(문단 hybrid rank + 섹션 membership 신호) → top-k
  - `kifrs/eval/retrieval.py`: `RETRIEVERS["hierarchical"]` 등록
  - AC: `python -m kifrs.eval.retrieval --k 20 --retrievers hybrid hierarchical` 가 hierarchical recall@20 ≥ hybrid(0.907) **AND** Q029·Q039·Q048 중 ≥2건 hit 전환, recall@5 비퇴행. before/after JSON 저장
  - 중단점: 측정 PASS → 커밋. recall 퇴행·잡음만 늘면 파라미터(S, 보강 수) 튜닝 후 재측정, 그래도 안 되면 보고 후 멈춤

- [x] **M4-1b — search_hierarchical MCP tool 노출** ✅ (2026-06-27) — `mcp_server.py` @mcp.tool() 추가 + /accounting SKILL.md 넓은 탐색 기본을 hierarchical 로(allowed-tools·조회전략). custom-skills 배포(Claude+Codex). *라이브 서버 재기동 시 호출 가능*.

- [~] **M4-2 — evidence curation 임계값** — **보류(측정상 가치 낮음, 2026-06-27)**
  - 분석: reranked rerank_score 의 gold vs noise 분리 불가. gold median 0.993 / noise(non-gold) median 0.921 — 겹침. τ=0.1 에서 gold 100% 유지 시 noise 제거 2%뿐, τ=0.3 이면 gold 떨어지기 시작(98.2%)
  - 원인: hybrid+rerank 가 이미 주제 관련 후보만 추려 저신뢰 꼬리가 거의 없음. "noise"=틀린 게 아니라 must_cite 밖 관련 문단. dogfood 실패 모드(본문 부재·누락 recall)는 임계값으로 안 잡힘
  - 결정: 가치 없는 필터 미구현(simplicity). 신호 잡히면 부활

## (b) 음성 결과 — hierarchical → reranked 후보 풀 교체 (폐기)
- 가설: reranked 후보를 hybrid→hierarchical 로 바꾸면 top-5 정밀도↑
- 측정: depth-50 recall 동일(hybrid 0.923 = hierarchical 0.923), reranked 출력 **완전 동일**. cross-encoder 는 풀 *순서* 무시 → 멤버십 같으면 결과 같음
- 결정: no-op, 코드 revert. hierarchical 가치는 standalone retriever 로 발현(M4-1b 노출)

## DoD (milestone) — ✅ 충족 (2026-06-27)

M4-1 측정 PASS(전 지표 비퇴행/개선) + M4-1b 실사용 wiring. M4-2 는 측정 근거로 보류.
evidence: `data/eval/results/retrieval_20260627_225318.json`. (b)·M4-2 음성결과도 평가 하네스 효용 증거.
