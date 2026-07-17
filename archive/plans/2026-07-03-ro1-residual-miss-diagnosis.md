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

- [x] **Step 1 — 얕은 랭킹 후보풀 확대 실험** — **불필요로 판명**. Q004/Q041을 `search_reranked`로
  직접 조회하니 이미 top-20 안(순위 6, 13)이었다 — `kifrs/eval/retrieval.py`의 miss 출력이 항상
  hybrid 기준이라 리포트가 오해를 유발했을 뿐, 코드는 이미 정상 동작. 후보풀 확대 실험 자체가
  불필요해졌다. (verify: `docs/reports/2026-07-03-ro1-deep-miss-diagnosis.md` §1 — 실측 rank 표)

- [x] **Step 2 — 깊은 랭킹 7건 원인 진단** (verify: `docs/reports/2026-07-03-ro1-deep-miss-diagnosis.md`
  §2 — 3개 카테고리 A(순수 어휘 부재)/B(일반어 판별력 부족)/C(크로스 개념 쏠림)로 분류, 근거 포함)

- [x] **Step 3 (integration) — 재측정 + RO2 필요성 판단** — 코드 변경이 없었으므로 재측정은
  이미 진행한 전역 rank 조회로 충분(before/after 표 불필요 — recall 수치 자체는 불변). RO2 권고:
  카테고리 C(멀티 쿼리 분해, 2건)만 좁게 시도, A/B는 보류(가치 낮음) — 리포트 §RO2 착수 판단 참조.
  (verify: `python -m pytest tests/ -q` 92/92 통과 — eval 조회만 했고 소스 변경 없어 비퇴행 확인됨)

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

- [x] `docs/reports/2026-07-03-ro1-deep-miss-diagnosis.md` — 얕은 랭킹 2건 해결 확인 + 깊은 랭킹
  7건 원인 카테고리 리포트, RO2 권고 포함
- [x] `python -m pytest tests/ -q` — 92/92 통과, 비퇴행(소스 코드 변경 없음)
- [x] `docs/horizons/rag-optimization-resume.md` RO2 착수 범위(카테고리 C만) 기록
