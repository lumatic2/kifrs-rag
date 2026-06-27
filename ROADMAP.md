# kifrs-rag ROADMAP

> 마지막 업데이트: 2026-06-27 (검색 파이프라인 M1·M2·M3 완료. ROADMAP compact → 완료 이력은 `BACKLOG.md`)
> K-IFRS 기준서 + AI 도구체인으로 회계사 실무의 상당 부분을 본인이 수행하는 개인용 시스템. 공개 레포에는 코드·아키텍처·평가 하네스만 두고, 기준서 원문·파싱 DB·임베딩·dogfood 자료는 로컬에서만 보관.
> 완료 이력(Phase 1~4 + M1·M2·M3) → **`BACKLOG.md`** · 다음 세션 진입점 → **`CLAUDE.local.md`**

## 배경 / 포지셔닝

K-IFRS 기준서를 프로그램적으로 조회할 공식 API/MCP 부재. 빅4 사내 AI는 비공개, 기준서 원문·파싱 텍스트·DB·임베딩·dogfood 자료는 KASB·IFRS Foundation 저작권 장벽 때문에 공개하지 않는다.
- 공개 범위: 코드, 아키텍처 설명, 평가 하네스, 메트릭, 운영 문서
- 비공개 범위: 기준서 PDF, 파싱 텍스트, SQLite DB, 임베딩, 회계사 기출 dogfood 자료
- `tax-agent` 패턴 재사용 → 신규 개발 비용 최소화

## 야망 (CLAUDE.md 동기화)

회계사가 아닌 본인이 AI 도구체인으로 **회계사 수준의 결과물**(분개·검토 메모·분류 판단·주석 초안)을 낸다. 각 단계는 이전 단계 검증 후에만 진행.

| 단계 | 목표 | 상태 |
|---|---|---|
| **Phase 1** | 인프라 — 100 기준서 DB + MCP + /accounting | ✅ (2026-04-14) |
| **Phase 2** | 시험 수준 — 2차 기출 정확 인용 + 적용 해설 | ✅ 졸업 누적 86% (2026-04-28) |
| **Phase 3** | 실무 시나리오 1개 — 금융상품 분류·측정(1109) | ✅ 10/10 (2026-04-28) |
| **Phase 4 (현재)** | 시나리오 확장 + 누적 (리스·수익·공정가치 + user_note) | 진행 중 (1116 5/10) |

> 상세 이력은 `BACKLOG.md` "Phase 이력" 참조.

---

## Current Horizon — 검색 파이프라인 고도화 (Phase 와 직교한 *엔진* 트랙)

<!-- harness:goal id="rag-goldstandard" -->
목표: K-IFRS RAG 검색을 **trendy legal/financial RAG 골드 스탠다드**(BM25 + dense + RRF + rerank + query expansion + **hierarchical retrieval** + **evidence curation**) 수준으로 완성. 모든 개선을 **retrieval eval 정량 측정** 기반으로 운영.
> 레퍼런스: [FinDER](https://arxiv.org/pdf/2504.15800) · [bge-m3](https://huggingface.co/BAAI/bge-m3) · [FinSage](https://arxiv.org/html/2504.14493v3) · [재무 QA 계층검색 2505.20368](https://arxiv.org/pdf/2505.20368)

**현재 천장(50문항)**: hybrid recall@20=**0.907** · reranked recall@5=**0.640**/MRR=0.612 · GPU per-query 0.44s.
**완료**: M1(측정 하네스) ✅ · M3(query expansion 천장 0.847→0.907) ✅ · M2(리랭킹 wiring) ✅ → 상세 `BACKLOG.md`.

### Active Milestones

<!-- harness:milestone id="M4" status="active" priority="P0" -->
#### M4 — Hierarchical retrieval + evidence curation
- DoD: 섹션(조·항·호)→문단 2단계 검색 retriever가 M1 하네스에서 hybrid 대비 recall lift(특히 섹션제목-쿼리 일치 miss Q029·Q039·Q048 회복), recall@5 비퇴행 + 저신뢰 임계값 필터로 약한 인용 제거. before/after JSON 증거
- Evidence: M4-1 ✅ `data/eval/results/retrieval_20260627_225318.json` — hierarchical 이 hybrid 전 지표 비퇴행/개선(recall@5 .597→.627, @10 .763→.827, @20 .907→.917, MRR .509→.542). M4-2 미결
- Gap: hybrid recall@20=0.907 천장. 잔여 miss 9건 중 3~4건은 정답 문단이 쿼리어 일치 섹션 아래 있음 → 계층검색 레버
- Status: [ ]
- Steps (plan: `docs/plans/2026-06-27-hierarchical-retrieval.md`): M4-1 ✅ 계층 검색(쿼리시점 섹션 centroid, 전 지표 lift) ▸ M4-2 evidence curation 임계값 — *재결정 대기*

### Next Candidates
- **M5 (옵션) — 평가 리포트 + 아키텍처 글** — before/after 메트릭으로 "trendy RAG 수준 달성" 증명 → D축 부활

## 성공기준 4축

| 축 | 기준 |
|---|---|
| **A. 실사용** | 매 사용 시 그 자리에서 사용성 직접 확인·수정 (정량 측정 철회) |
| **B. 시험 정확도** | 2차 기출 5~10문항 본인 채점 **80%+** → ✅ 누적 86% |
| **C. 커버리지** | ✅ 100 기준서 / 8,328 paragraphs |
| **D. 포트폴리오** | 보류 — 옵션 트랙(M5). Phase 4 종료 후 재검토 |

---

## 다음 세션 진입점

> 현재 상태·다음 할 일 상세는 **`CLAUDE.local.md`** (gitignored handoff). 아래는 안정적 후보 목록.

**[엔진 축] M4 착수** — 계층 검색. `./.venv/Scripts/python.exe -m kifrs.eval.retrieval [--k 20] [--only Q008]` 으로 측정.

**[콘텐츠 축] Phase 4 잔여**
- q07 (1115 수익) 본인 풀이 + 채점 — `data/dogfood/cpa2/q/q07.md`. *데이터 오염 방지 위해 새 세션에서* 시작. 토픽: 갱신선택권/외상거래할인권/선수금 금융요소/콜옵션 재매입약정
- 잔여 1116 시나리오 3(단기·저가 면제)·6(금융→금융)·7(기간 재평가)·8(매수선택권)
- 다른 도메인: 1019(확정급여, q06 재활용) / 1115(수익, q07 재활용) / 1113(공정가치, KICPA 부담 1위)

**[옵션, 신호 발생 시 trigger]**
- user_note 활성화 (본문 부재 키워드 매핑 — Q05 공매도 등). 마찰 누적 시 일부 당겨오기
- 한국 상법 인덱싱 (Q04 자본거래만 마찰, 빈도 낮음 → 보류)
- 평가 하네스 50문항 자동 채점 (D축 욕구 살아나면 부활)

---

## 작업 원칙 (저작권·보안)

- **기준서 PDF·텍스트·임베딩·DB 덤프 절대 git commit 금지** (`.gitignore` 최상단)
- 회계사 2차 기출 dogfood 자료도 commit 금지 (`data/dogfood/`)
- 기준서 PDF·텍스트·임베딩·DB·기출 자료는 공유하지 않음
- 공개 협업 범위는 코드·검색 파이프라인·평가 하네스에 한정

## DB 테이블 채우기 일정

| 테이블 | 현재 | 시점 |
|---|---|---|
| `standard` / `paragraph` / `paragraph_fts` | ✅ 100개 / 8,328행 / trigram | Phase 1·2 완료 |
| `embedding` | ✅ bge-m3 1024d, 100% | Phase 2 완료 |
| `cross_reference` / `amendment` | 🟡 스키마만 | Phase 4 — 실사용 마찰 trigger |
| `user_note` | 🟡 스키마만 | Phase 4 — 본인 해설 누적 시작 |

## 메모

- KASB 메일 v3.4 초안 보류. 외부 공개 단계 진입 시 재활용
- **KICPA K-IFRS 적용 부담 순위**: 공정가치/손상/재평가 27.08% > 금융상품 14.58% > 리스 13.44% > 수익 13.33% > 연결 10.83%
  - Phase 3 첫 시나리오를 금융상품(1109)으로 잡은 근거: DB 강점(556 paragraphs) + 워크플로 결정론적(SPPI→사업모형→분류) + 골든셋 Q003·Q008 재활용. 1순위 공정가치는 DCF·옵션모델·시장데이터까지 필요 → 후속 도전
