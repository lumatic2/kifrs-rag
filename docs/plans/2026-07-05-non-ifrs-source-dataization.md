# Plan: Non-IFRS Source Dataization

> Objective: `docs/OBJECTIVE.md`
> Horizon: `docs/horizons/non-ifrs-source-dataization.md`
> Previous gate: `docs/reports/2026-07-05-rr5-rag-promotion-gate.md`

## 산문 요약

이번 horizon은 K-IFRS RAG가 안정화된 상태에서, IFRS 본문만으로는 부족한 회계 실무 정보원을 실제
RAG/lookup 데이터 단위로 바꾸는 작업이다. 이미 source taxonomy, manifest prototype, connector scaffold가
여럿 있으므로 새로 크게 벌리기보다 먼저 inventory로 재사용 범위를 고정한다. 그 다음 record contract,
public-safe fixture, chunk/index policy, close gate 순서로 진행한다.

## Horizon Order

1. `non-ifrs-source-dataization` — KASB/FSS/법령/DART/client-private source lane을 실제 RAG 데이터화 단위로 확장.
2. `multi-authority-runtime-hardening` — K-IFRS, 법령, 질의회신, 공시, private facts를 권위별로 분리해 답변에 쓴다.
3. `client-private-parser-runtime` — 계약서/TB/회계정책서 같은 로컬 private 파일 parser와 deletion/runtime gate.
4. `firm-facing-product-surface` — 회계법인에 보여줄 demo surface, operator UX, install/readiness 패키지.

## Step Tree

- [x] NIS1 — Existing source asset inventory. (verify: report exists and classifies reusable vs superseded source assets)
- [ ] NIS2 — Source record contract. (verify: `python -m pytest tests\test_source_record_contract.py -q`)
- [ ] NIS3 — Dataization fixtures and validators. (verify: `python scripts\validate_non_ifrs_source_records.py --format text`)
- [ ] NIS4 — Chunking and embedding policy. (verify: `python scripts\validate_non_ifrs_chunking_policy.py --format text`)
- [ ] NIS5 — Dataization gate and runtime handoff. (verify: `python scripts\non_ifrs_dataization_gate.py --format text` + `python scripts\quality_preflight.py --format text`)

## 결정 로그

- 결정: live external connector/API 호출은 이 horizon의 기본값이 아니다. public-safe fixture와 validator를 먼저 만든다.
- 결정: 외부 문서 본문, 법령 본문, DART raw dump, embeddings, API key는 public repo에 넣지 않는다.
- 결정: KASB/FSS/FSC 해석 자료는 supporting interpretation이고 K-IFRS primary evidence를 대체하지 않는다.
- 결정: DART/OpenDART 계열은 structured fact lane으로 둔다.
- 결정: client-private 자료는 local-only placeholder/contract까지만 public repo에 둔다.
- 사용자 소유 결정: 현재 없음.

## 중단점

- protected body나 credential이 필요한 구현은 중단하고 policy/placeholder로 남긴다.
- source body ingestion이나 live API call이 필요해지면 별도 authorization gate로 넘긴다.
- RAG reliability regression command가 실패하면 source 확장보다 regression 원인을 먼저 고친다.

## Regression Commands Carried From RR5

- `python scripts\quality_preflight.py --format text`
- `python scripts\rag_quality_final_gate.py --format text`
- `python scripts\default_retriever_guard.py --format text`
- `python scripts\rag_reliability_retrieval_citation_diagnostics.py --format text`
