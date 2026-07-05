# Plan: RAG Reliability Revalidation

> Objective: `docs/OBJECTIVE.md`
> Horizon: `docs/horizons/rag-reliability-revalidation.md`
> Scope: 현재 진행할 horizon의 milestone/step tree

## 산문 요약

이번 horizon은 제품 기능을 새로 늘리기 전에 K-IFRS RAG의 신뢰도를 다시 재는 작업이다. 지금 레포는
review pack, source map, parser plan이 많이 생겼지만, default retriever를 바꾸거나 source를 더 붙이기
전에 검색/인용/답변 품질의 기준선이 필요하다. 따라서 먼저 public-safe 평가 명령과 기존 리포트를
정리하고, eval coverage와 실패 유형을 만든 뒤, opt-in repair retriever를 default로 올릴지 말지를
판단하는 gate까지 만든다.

## Horizon Order

1. `rag-reliability-revalidation` — K-IFRS RAG 품질 재검증과 default promotion 기준.
2. `non-ifrs-source-dataization` — KASB/FSS/법령/DART/client-private source lane을 실제 RAG 데이터화 단위로 확장.
3. `multi-authority-runtime-hardening` — K-IFRS, 법령, 질의회신, 공시, private facts를 권위별로 분리해 답변에 쓰는 runtime.
4. `client-private-parser-runtime` — 계약서/TB/회계정책서 같은 로컬 private 파일 parser와 deletion/runtime gate.
5. `firm-facing-product-surface` — 회계법인에 보여줄 demo surface, operator UX, install/readiness 패키지.

## Step Tree

- [x] RR1 — Baseline inventory. (verify: `python scripts\quality_preflight.py --format text` + report exists)
- [x] RR2 — Eval matrix and seed coverage. (verify: report lists buckets without protected source body)
- [x] RR3 — Retrieval and citation diagnostics. (verify: `python scripts\eval_quality_gate.py --runner local-rag --only Q019 Q020 Q021 Q022 Q023 --min-composite 0.6 --min-cite 0.45 --format text`)
- [x] RR4 — Repair policy candidate. (verify: `python scripts\default_retriever_guard.py --format text`)
- [ ] RR5 — Promotion gate and handoff. (verify: `python scripts\rag_quality_final_gate.py --format text` and `python scripts\quality_preflight.py --format text`)

## 결정 로그

- 결정: 실제 회계사 outreach/mail/invite는 이 horizon 범위에서 제외한다.
- 결정: default retriever promotion은 RR5 gate가 통과하기 전까지 하지 않는다.
- 결정: 보호 데이터, 기준서 원문, dogfood 본문은 report에 쓰지 않는다.
- 사용자 소유 결정: 현재 없음.

## 중단점

- public-safe gate가 실패하면 구현 확장을 멈추고 실패 원인을 먼저 고친다.
- default retriever 변경이 필요해지면 RR5에서 별도 승인 대상으로 남기고 자동 변경하지 않는다.
- protected source body가 필요한 작업은 이 horizon에서 제외한다.
