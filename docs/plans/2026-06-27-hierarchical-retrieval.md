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

## Step 트리

- [ ] **M4-1 — 계층 검색 retriever** (leaf)
  - `kifrs/embed.py`: `search_hierarchical(query, standard, limit)` 추가
    - ① hybrid 풀(50) 확보 (기존 문단 recall 천장 보존)
    - ② (standard, section) centroid = 멤버 문단 벡터 평균 (numpy groupby, 쿼리 시점 계산)
    - ③ 쿼리 vs centroid cosine → 상위 S 섹션
    - ④ 상위 섹션 내 best 문단(쿼리 vs 문단 cosine)을 풀에 union
    - ⑤ RRF 융합(문단 hybrid rank + 섹션 membership 신호) → top-k
  - `kifrs/eval/retrieval.py`: `RETRIEVERS["hierarchical"]` 등록
  - AC: `python -m kifrs.eval.retrieval --k 20 --retrievers hybrid hierarchical` 가 hierarchical recall@20 ≥ hybrid(0.907) **AND** Q029·Q039·Q048 중 ≥2건 hit 전환, recall@5 비퇴행. before/after JSON 저장
  - 중단점: 측정 PASS → 커밋. recall 퇴행·잡음만 늘면 파라미터(S, 보강 수) 튜닝 후 재측정, 그래도 안 되면 보고 후 멈춤

- [ ] **M4-2 — evidence curation 임계값** (M4-1 후 재결정, *이번 run 범위 밖 가능*)
  - reranked/hierarchical 출력에 rerank_score < τ 결과 제거
  - AC: goldset 에서 recall@5 비퇴행하는 τ 선택 + 제거된 저신뢰 결과 수 보고. precision/UX 레버(recall 중립 설계)

## DoD (milestone)

M4-1 측정 PASS + (선택)M4-2 → `roadmap_sync.py complete --milestone M4`. before/after JSON = evidence.
