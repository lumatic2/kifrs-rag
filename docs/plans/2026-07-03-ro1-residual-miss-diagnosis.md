# Plan: RO1 — 잔여 miss 진단 + 얕은 랭킹 1차 개선

> Objective: `docs/OBJECTIVE.md`
> Horizon: `docs/horizons/rag-optimization-resume.md` (`rag-optimization-resume`)
> Milestone: RO1 — 잔여 miss 진단 + 얕은 랭킹 문제 1차 개선
> Created: 2026-07-03

## Scope boundary

M4(2026-06-27) 종료 시점 이후 처음 재측정한 50문항 goldset 기준, hybrid recall@20 miss 9건을
얕은 랭킹(K=100에서 회복되는 2건: Q004, Q041)과 깊은 랭킹(K=100에서도 miss인 7건: Q001, Q006,
Q008, Q029, Q039, Q040, Q048)으로 재확인했다(계획 단계 재측정, 위 horizon doc §Why now 참조).
이번 milestone은 ① 얕은 랭킹 2건에 candidate pool 확대를 적용해 회복 여부를 측정하고, ② 깊은
랭킹 7건은 문항별 원인을 분류한 진단 리포트까지만 산출한다 — 깊은 랭킹의 실제 개선책(RO2)은
이 진단 결과를 본 뒤 별도로 scope한다("아는 만큼만 펼친다" — 원인을 모른 채 개선책부터 고정하지
않는다).

Out of scope (이번 milestone에서 다루지 않음, 이유):
- **깊은 랭킹 7건의 실제 개선 적용** — RO2 후보. 원인 분류가 먼저.
- **임베딩 모델 교체** — 재인덱싱 비용이 크고(GPU라도 8,328 문단 재인코딩 수분), 채택 가치가
  불확실(이미 recall 천장 0.907~0.917로 높음). RO1 진단에서 "모델 해상도 부족"이 명확한 원인으로
  나오면 RO2 후보로만 승격.
- **goldset 확장(50→더 많이)** — 이번 horizon은 기존 50문항의 잔여 miss 공략이 목표. 확장은 별도
  신호(D축 욕구) 필요.

## Step tree (leaf test 적용 — 시그니처 수준)

- [ ] **Step 1 — 얕은 랭킹 후보풀 확대 실험** (`kifrs/embed.py::search_reranked`/`search_hierarchical`
  candidates 파라미터, 코드 변경 없이 `--candidates` 플래그로 우선 측정)
  Q004(1001-69)·Q041(1102-11)이 hybrid K=100에서 회복됨을 확인했다(이번 계획 단계). reranked/
  hierarchical의 기본 candidate pool(50)을 100으로 늘려 재측정 — 두 문항이 top-20 안으로 들어오는지,
  다른 지표(recall@5, MRR)가 퇴행하지 않는지 확인. (verify: `python -m kifrs.eval.retrieval
  --retrievers hybrid hierarchical reranked --k 20 --no-save`로 before/after 비교, Q004/Q041
  hit 전환 + 전 지표 비퇴행)

- [ ] **Step 2 — 깊은 랭킹 7건 원인 진단** (`kifrs/eval/` 진단 스크립트 또는 1회성 분석, 산출물은
  리포트 문서)
  Q001(1115-27), Q006(1115-51), Q008(1109-2.1), Q029(1116-45), Q039(1037-14), Q040(1109-4.1.4),
  Q048(1036-18) 각각에 대해: 정답 문단의 실제 전역 순위(쿼리 vs 문단 cosine 전체 순위), 현재
  top-20에 랭크된 문단과의 의미적 차이, 어휘 중첩 여부(`extract_keywords` 교집합)를 확인해 원인을
  카테고리화(예: "섹션/문맥 misalignment", "다의어·상위개념 경쟁", "쿼리가 다른 조항으로 쏠림",
  "진짜 어휘 부재"). (verify: `docs/reports/2026-07-03-ro1-deep-miss-diagnosis.md`에 7건 전부
  카테고리 + 근거(전역 순위·top-20 비교) 기록)

- [ ] **Step 3 (integration) — 재측정 + RO2 필요성 판단** (`docs/horizons/rag-optimization-resume.md`
  갱신)
  Step 1 적용 후(채택됐다면) 전체 goldset 재측정, before/after 표 기록. Step 2 진단 결과를 보고
  RO2(깊은 랭킹 개선) 착수 가치가 있는지 — M4-2가 "가치 낮음"으로 보류했던 것과 같은 기준(비용 대비
  회복 가능 문항 수)으로 판단해 horizon doc에 기록. (verify: horizon doc에 판단 근거 기록 +
  `python -m pytest tests/ -q` 비퇴행 — 이번 milestone은 eval 스크립트/파라미터만 건드리므로 기존
  92개 테스트에 영향 없어야 함)

## 결정 로그

- **얕은 랭킹 vs 깊은 랭킹 분류 기준: K=20→K=100 회복 여부** — 계획 단계에서 이미 확정(재측정으로
  확인). 사용자 재확인 불필요 — 관측된 사실.
- **candidate pool 확대 폭(50→100)** — 1차 시도값. Step 1 측정 결과 회복 안 되거나 다른 지표가
  퇴행하면 75 등 중간값으로 재시도 — 새 리스크는 아니므로 무중단 진행.
- **깊은 랭킹 7건 실제 개선책은 RO2로 이관** — 사용자 결정(horizon 논의 시 "잔여 miss 공략" 방향
  확정, 개선책은 진단 후 결정). Step 2 결과가 "임베딩 모델 교체가 유일한 해법"으로 나오면, 그건
  비용이 크므로(재인덱싱) RO2 착수 전에 다시 사용자 승인 필요 — 예상된 후속 결정.
- 이 외 예상되는 사용자 소유 결정 없음.

## Integration verification (milestone close)

- `python -m kifrs.eval.retrieval --retrievers hybrid hierarchical reranked --k 20 --no-save` —
  Step 1 candidate pool 확대 전/후 비교표
- `docs/reports/2026-07-03-ro1-deep-miss-diagnosis.md` — 깊은 랭킹 7건 원인 카테고리 리포트
- `python -m pytest tests/ -q` — 92개 비퇴행
- `docs/horizons/rag-optimization-resume.md` RO2 착수 여부 판단 기록
