# kifrs-rag ROADMAP

> 마지막 업데이트: 2026-06-30 (Engine Quality Ops 현재 scope 완료)
> K-IFRS 기준서 + AI 도구체인으로 회계사 실무의 상당 부분을 본인이 수행하는 개인용 시스템. 공개 레포에는 코드·아키텍처·평가 하네스만 두고, 기준서 원문·파싱 DB·임베딩·dogfood 자료는 로컬에서만 보관.
> 완료 이력(Phase 1~4 + M1~M5) → **`BACKLOG.md`** · 다음 세션 진입점 → **`CLAUDE.local.md`**

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
| **Phase 4 (현재)** | 시나리오 확장 + 누적 (리스·수익·공정가치·확정급여 + user_note) | 진행 중 (P4C1~P4C5 완료) |

> 상세 이력은 `BACKLOG.md` "Phase 이력" 참조.

---

## Current Horizon — Engine Hardening

<!-- harness:goal id="engine-hardening" -->
목표: 검색 엔진(mcp_server.py/embed.py)을 테스트 커버·비중복·MCP 통합 상태로 만들되 검색 품질(recall/MRR)은 비퇴행. 상세 계획: `docs/horizons/engine-hardening.md`

**상태**: Engine Quality Ops(EQ1~EQ5) 완료 후 코드 감사로 발견된 엔진 자체의 테스트 부재·N+1·MCP tool 중복을 다루는 새 horizon.
**세부 계획**: `docs/plans/2026-07-03-engine-hardening.md`

### Active Milestones
<!-- harness:milestone id="EH1" status="completed" priority="P0" evidence="changesets/20260703-engine-test-safety-net/README.md; changesets/20260703-engine-perf-refactor/README.md; changesets/20260703-mcp-server-dedup-errors/README.md; changesets/20260703-mcp-search-tool-consolidation/README.md; changesets/20260703-term-bridge-user-note-migration/README.md" -->
#### EH1 — Engine test safety net + refactor + MCP consolidation
- DoD: mcp_server.py/embed.py 테스트 추가, search_reranked N+1 및 임베딩/centroid 캐싱 수정, TERM_BRIDGE→user_note_v2 이관, search tool 5종→1종 통합(+ /accounting SKILL.md·README 동기화)을 각각 changeset으로 완료하고, quality_preflight.py + engine_quality_expanded_smoke.py 비퇴행을 통합 검증으로 남긴다.
- Evidence: `changesets/20260703-engine-test-safety-net/README.md`; `changesets/20260703-engine-perf-refactor/README.md`; `changesets/20260703-mcp-server-dedup-errors/README.md`; `changesets/20260703-mcp-search-tool-consolidation/README.md`; `changesets/20260703-term-bridge-user-note-migration/README.md`; `python -m pytest tests/ -q` (46 passed); `python scripts/quality_preflight.py --format text` (ok: True); `python scripts/engine_quality_expanded_smoke.py --format text` (ok: True)
- Gap: 검색 로직에 테스트가 없고, N+1/중복 임베딩 로딩이 있으며, MCP search tool이 5종 중복이고, TERM_BRIDGE가 하드코딩돼 있었다. 5개 changeset(CS-1~CS-5)으로 모두 닫힘.
- Status: [x] CS-1 테스트 안전망 / [x] CS-2 N+1+캐싱 / [x] CS-3 mcp_server dedup+에러 / [x] CS-4 tool 통합 / [x] CS-5 term_bridge 이관

- Completed at: 2026-07-03
- Summary: engine test safety net + N+1/caching perf fix + mcp_server dedup/structured errors + 5-tool search consolidation + TERM_BRIDGE migration, all verified non-regressing (recall/MRR unchanged, 46/46 tests, preflight ok)

### Next Candidates
- 없음. EH1(및 Engine Hardening horizon) 완료 — 다음 방향은 Phase 4 scenario expansion 복귀 또는 새 horizon 결정.
### Planning Rule
- 새 구현은 먼저 `docs/plans/2026-07-03-engine-hardening.md`의 changeset 순서(CS-1→CS-5)를 따른다.
- 각 changeset은 quality_preflight.py/engine_quality_expanded_smoke.py 비퇴행을 확인한 뒤에만 다음으로 넘어간다.

## 성공기준 4축

| 축 | 기준 |
|---|---|
| **A. 실사용** | 매 사용 시 그 자리에서 사용성 직접 확인·수정 (정량 측정 철회) |
| **B. 시험 정확도** | 2차 기출 5~10문항 본인 채점 **80%+** → ✅ 누적 86% |
| **C. 커버리지** | ✅ 100 기준서 / 8,328 paragraphs |
| **D. 포트폴리오** | ✅ M5 블로그 발행으로 1차 충족. 추가 글/README 리포트는 새 horizon 결정 시 별도 판단 |

---

## 다음 세션 진입점

> 현재 상태·다음 할 일 상세는 **`CLAUDE.local.md`** (gitignored handoff). 아래는 안정적 후보 목록.

**[현재 active 없음]**

**[다음 후보]**
- 없음. EQ5 완료 후 새 horizon 또는 Phase 4 scenario expansion 여부를 다시 결정.

다음 구현 전 먼저 확인할 문서: `docs/plans/2026-06-30-kifrs-direction-success-criteria.md`

**[콘텐츠 축] Phase 4 잔여**
- 1116 리스: 10/10 완료
- 다른 도메인: 1113(공정가치) entry 완료 / 1019(확정급여) entry 완료

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
| `cross_reference` / `amendment` | 🟡 스키마만 | 실사용 마찰 trigger |
| `user_note` / `user_note_v2` | 🟡 13건 seed + v2 runtime + legacy fallback | term_bridge/retriever_policy 검색 확장 + answer-time notes |

## 메모

- KASB 메일 v3.4 초안 보류. 외부 공개 단계 진입 시 재활용
- **KICPA K-IFRS 적용 부담 순위**: 공정가치/손상/재평가 27.08% > 금융상품 14.58% > 리스 13.44% > 수익 13.33% > 연결 10.83%
  - Phase 3 첫 시나리오를 금융상품(1109)으로 잡은 근거: DB 강점(556 paragraphs) + 워크플로 결정론적(SPPI→사업모형→분류) + 골든셋 Q003·Q008 재활용. 1순위 공정가치는 DCF·옵션모델·시장데이터까지 필요 → 후속 도전
