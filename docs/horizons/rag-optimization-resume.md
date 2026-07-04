# RAG 최적화 재개 Horizon

> Created: 2026-07-03
> ROADMAP goal id: `rag-optimization-resume`
> Status: active
> Objective: `docs/OBJECTIVE.md`

## Why now

검색 파이프라인 고도화(`rag-goldstandard` horizon, M1~M4, 2026-06-27)에서 hybrid recall@20을
0.847→0.907로, hierarchical로 0.917까지 올렸다. 그 뒤 EQ1~5·EH1은 품질 *운영*(quality preflight,
authority source pack)·코드 *하드닝*(MCP 통합, 테스트 안전망)이었지 recall/MRR 자체를 더 올리려는
시도가 아니었다. 성공기준 A축 "정량 측정 철회"는 실사용 전환 결정이었지 더 못 올린다는 뜻은
아니다(ROADMAP.md 참조).

2026-07-03 재확인(이 horizon 계획 전 재측정): baseline 수치는 M4 종료 시점과 그대로다(hybrid
recall@20=0.907, hierarchical=0.910~0.917, reranked recall@5=0.640/MRR=0.612 — drift 없음). 50문항
goldset 기준 잔여 miss를 이번 계획 단계에서 재진단한 결과:

- **hybrid K=20 miss 9건**: Q001(1115-27), Q004(1001-69), Q006(1115-51), Q008(1109-2.1),
  Q029(1116-45), Q039(1037-14), Q040(1109-4.1.4), Q041(1102-11), Q048(1036-18)
- **hybrid K=100까지 넓히면 Q004·Q041 회복** — 얕은 랭킹 문제(순위 20~100 사이)
- **K=100에서도 여전히 miss 7건**: Q001, Q006, Q008, Q029, Q039, Q040, Q048 — 후보풀 확대로는
  못 잡는 깊은 문제. 해당 문단들의 본문을 직접 확인한 결과 어휘 자체는 질문과 상당히 겹친다(예:
  1116-45 "리스변경"↔Q029 "리스 범위를 좁히는 변경") — M4가 진단한 Q039(1037-14, 섹션 centroid
  전역순위 674)처럼 **어휘 부재가 아니라 임베딩 랭킹 자체가 얕게 매기는 문제**로 보인다.

## Goal

잔여 miss 문항을 카테고리별로 진단하고(얕은 랭킹 vs 깊은 랭킹 vs 진짜 어휘 부재), 카테고리에 맞는
개선을 적용해 recall을 재측정한다. 100% 회복이 목표가 아니라 — M4와 같은 정신으로 — "측정 가능한
개선 또는 정직한 한계 확인"이 목표다.

## Milestone candidates (2~5, horizon-run continuation용)

1. **RO1 — 잔여 miss 진단 + 얕은 랭킹 문제 1차 개선** (first, this planning round)
   9건을 얕은 랭킹(2건: Q004·Q041)과 깊은 랭킹(7건: Q001·Q006·Q008·Q029·Q039·Q040·Q048)으로
   재확인하고, 얕은 랭킹 그룹은 `search_reranked`/`search_hierarchical`의 candidate pool을
   50→더 크게 늘려 회복 여부 측정. 깊은 랭킹 그룹은 문항별 세부 진단(정답 문단 vs 실제 top-20의
   의미적 차이)까지만 이번 milestone에서 수행 — 원인 분류가 산출물.
2. **RO2 — 깊은 랭킹 문제 개선 실험** (candidate, RO1 진단 결과로 scope 확정)
   RO1이 분류한 원인(예: 섹션 misalignment, 임베딩 해상도 부족, 청크 경계)에 맞는 개선 — 임베딩
   모델 교체 비교, 청크 재분할, 추가 term bridge 등 중 RO1 결과가 가리키는 것.
3. **RO3 — 종합 재측정 + 문서화** (candidate, RO1/RO2 완료 후)
   전체 goldset 재측정, M1~M4와 같은 before/after 표로 기록, horizon 닫는 기준 충족 확인.

## Close criteria

RO1(진단 + 얕은 랭킹 회복 시도)이 닫히고, 깊은 랭킹 7건의 원인이 카테고리화되면 이 horizon의 첫
phase가 닫힌다. RO2/RO3 여부는 RO1 결과(개선 여지가 실제로 있는지, 비용 대비 가치가 있는지)를 보고
판단 — M4가 M4-2(evidence curation)를 "가치 낮음"으로 보류한 것과 같은 정직한 판단 기준 적용.

## RO1 결과 (2026-07-03)

`docs/reports/2026-07-03-ro1-deep-miss-diagnosis.md` 전체 참조. 핵심:

- **얕은 랭킹 2건(Q004/Q041)은 이미 해결돼 있었다** — `search_reranked`가 이미 top-20 안(순위 6,
  13)에 넣고 있었고, 원래 horizon을 열게 한 "9건 miss"라는 인식 자체가 eval 스크립트 출력이 항상
  hybrid 기준이라 생긴 오독이었다. 코드 변경 없음.
- **깊은 랭킹 7건은 3개 카테고리**: A(순수 어휘 부재, 2건, 확장성 낮아 착수 보류) / B(일반어 매칭
  판별력 부족, 3건, hierarchical도 못 잡아 난이도·불확실성 높음, 착수 보류) / C(크로스 개념/표준
  쏠림, 2건, 멀티 쿼리 분해라는 새 접근 — 일반화 가능성 있어 RO2 후보).

**RO2 scope 결정**: 카테고리 C(멀티 쿼리 분해, Q039/Q048)만 좁게 시도. A/B는 보류(비용 대비 가치
낮음 — M4-2와 같은 판단). RO2 착수는 별도 세션에서 사용자와 재확인 후 진행.

## RO2 결과 (2026-07-05)

`docs/reports/2026-07-05-ro2-multi-query-experiment.md` 참조. Q039/Q048만 대상으로
`multi_query_hybrid` 실험 retriever를 추가해 원문 쿼리, literal concept phrase, 작은 concept
expansion을 RRF로 합쳤다.

결과: **기본 검색으로 승격하지 않는다.** `hybrid` 대비 recall@20은 개선되지 않았고, MRR/nDCG는
낮아졌다. 단순 split-and-fuse 방식은 category C miss를 회복하지 못했다. 다음 후보는 generic
multi-query가 아니라 reviewed `user_note_v2` term bridge, structured source routing, per-must-cite
retrieval 평가 쪽이다. `gold_ranks` 진단상 Q039는 `1116-24`만 잡고 `1037-14`가 absent, Q048은
`1036-59`만 잡고 `1036-18`이 absent다.

## RO2 term bridge 후보 평가 (2026-07-05)

`docs/reports/2026-07-05-ro2-term-bridge-candidate-eval.md` 참조. DB를 바꾸지 않고 후보 expansion을
붙여 평가한 결과, Q039는 `충당부채 -> 현재의무 과거사건 자원 유출 가능성 신뢰성 있는 추정`, Q048은
`손상차손 -> 회수가능액 순공정가치 사용가치`가 seed 후보로 남았다. 두 후보 모두 누락 target을 top-20
안으로 회복하면서 기존 top-20 required citation을 보존했다. 다음 leaf는 이 두 후보만 reviewed
`user_note_v2` seed로 승격할지 결정하고 적용/재측정하는 것이다.

## RO2 reviewed seed 적용 결과 (2026-07-05)

`scripts/seed_user_notes.py`에 위 두 후보를 추가하고 `--apply`로 로컬 DB에 반영했다. 적용 후
`python -m kifrs.eval.retrieval --k 20 --retrievers hybrid --only Q039 Q048 --no-save` 결과,
focused hybrid recall@20은 0.500에서 1.000으로 회복됐다. 다만 MRR/nDCG는 하락했으므로 이 변경은
general ranking improvement가 아니라 targeted recall repair로 해석한다.

재발 방지용 focused gate도 추가했다. `python scripts\ro2_term_bridge_gate.py --format text`는 Q039/Q048
hybrid top-20 miss가 비어 있고 recall@20이 1.000인지 확인한다. 이 gate는 랭킹 품질 개선을 주장하지 않고,
seed가 빠지거나 DB 재생성 후 term bridge가 누락되는 회귀만 잡는다.

## Citation-level 진단 추가 (2026-07-05)

`scripts/retrieval_must_cite_report.py`를 추가해 문항 단위가 아니라 필수 인용 문단 단위로 rank bucket을
볼 수 있게 했다. `docs/reports/2026-07-05-must-cite-rank-report.md` 기준 hybrid 50문항/82개 필수 인용 중
45개는 top-5, 14개는 top-10, 13개는 top-20, 10개는 top-20 밖이다. 이 리포트는 다음 개선 후보를
source routing(1115·1109·1037 cluster), 추가 term bridge, standard-specific routing으로 나누는 진단
층이며, 그 자체를 RAG 품질 개선으로 해석하지 않는다.

## Source routing 후보 평가 (2026-07-05)

`scripts/source_routing_candidate_eval.py`로 top-20 밖 10개 필수 인용에 대해 supplemental standard routing
후보를 평가했다. `docs/reports/2026-07-05-source-routing-candidate-eval.md` 기준 Q004(1001), Q013/Q025/Q026
(1037), Q041(1102)만 candidate다. Q001/Q006(1115), Q008/Q040(1109), Q029(1116)는 reject다. 결론:
source routing은 부분 후보일 뿐이며 기본 retriever로 승격하지 않는다. 다음 구현을 한다면 blanket filter가
아니라 accepted cluster에 한정한 supplemental retriever/gate여야 한다.

## Source routed hybrid 구현 (2026-07-05)

`source_routed_hybrid` opt-in retriever를 추가했다. 기본 `hybrid`는 변경하지 않고, accepted cluster인
1001/1037/1102 trigger에 한해서만 baseline hybrid와 standard-restricted hybrid를 RRF로 섞는다.
`docs/reports/2026-07-05-source-routed-hybrid-implementation.md` 기준 full 50-item recall@20은
0.877에서 0.943으로 올랐고, citation-level absent는 10개에서 5개로 줄었다. `source_routed_hybrid_gate.py`
는 accepted 5개가 회복되고 rejected 5개는 기존 hard miss로 남는지 확인한다. 아직 rule-triggered 실험
retriever이므로 기본 retriever로 승격하지 않는다.

## 남은 hard miss 후보 평가 (2026-07-05)

`scripts/hard_miss_candidate_eval.py`로 source_routed_hybrid 이후에도 남은 Q001/Q006/Q008/Q029/Q040을
각각 expansion 후보 1개씩 평가했다. `docs/reports/2026-07-05-hard-miss-candidate-eval.md` 기준 Q029
`1116-45`만 candidate다. Q001/Q006/Q008/Q040은 reject다. 다음 leaf는 Q029 bridge만 reviewed
`user_note_v2` seed로 승격하고 focused retrieval을 재측정하는 것이다.

## Objective 임팩트

이 horizon(RO1)이 실제로 움직인 것은 recall 수치가 아니라 **진단의 정확성**이다 — "9건 miss"라는
잘못된 전제가 "2건은 이미 해결·7건은 3개 원인"으로 교정됐다. Objective의 "K-IFRS 기반" 축에는
간접적으로만 기여(검색 품질 자체는 M4 이후 변화 없음). 재측정 필요 여부: 아니다 — RO2(카테고리 C)
결과를 보고 recall 수치가 실제로 움직이면 그때 재평가.
