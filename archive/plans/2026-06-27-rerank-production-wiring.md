# Plan — M2: Cross-encoder 리랭킹 프로덕션 wiring

> Horizon: 검색 파이프라인 고도화 (rag-goldstandard) · Milestone: M2 (active, P1)
> 작성: 2026-06-27 · 측정은 완료(reranked recall@5=0.640/MRR=0.612), 이번 run 은 wiring

## Scope (이번 horizon)

M2 리랭커(`kifrs/embed.py:search_reranked`)는 측정으로 채택 가치 확인 끝(top-5 정밀도 hybrid 대비 +4.3pp, MRR +10.3pp). 보류 사유였던 CPU 쿼리당 수 초 지연은 GPU 전환(2026-06-27)으로 per-query 0.44s 가 되어 해소. 이번 run 은 이 함수를 인터랙티브 경로(MCP + /accounting)에 꽂는다.

## 중단점

- MCP 서버 import·boot 무에러 + search_reranked tool 등록 + SKILL.md 반영 = 검증 체크포인트
- 실제 MCP 재기동 후 체감 확인은 사용자 세션 재시작 필요 (코드/스킬 반영까지가 이번 run)

## Step 트리

- [ ] **M2-1 — search_reranked MCP tool + 리랭커 warmup** (`kifrs/mcp_server.py`)
  - 읽기: `kifrs/mcp_server.py`(search_hybrid tool 패턴·_warmup 데몬 스레드), `kifrs/embed.py`(search_reranked·_load_reranker)
  - 작업: search_hybrid 미러로 `search_reranked` tool 추가(lazy import, candidates=50, default limit=10). `_warmup` 데몬 스레드에 `_load_reranker()` 추가 → cold-start 19s(모델 로드) 흡수, 핸드셰이크는 먼저 응답(M1 fix 패턴 유지).
  - AC: `python -c "import kifrs.mcp_server"` 무에러 (tool 등록 문법 검증). search_reranked 함수 자체는 검증됨(0.44s)
  - 금지: warmup 을 mcp.run() *앞* 동기 호출 금지(이유: 핸드셰이크 타임아웃 → 서버 死, M1 버그 재발). 기존 tool 시그니처 변경 금지
- [ ] **M2-2 — /accounting SKILL.md 정밀 인용 가이드** (`~/projects/custom-skills/accounting/SKILL.md` 원본 → 배포)
  - 읽기: SKILL.md §2 MCP 조회 전략, allowed-tools
  - 작업: allowed-tools 에 `mcp__kifrs__search_reranked` 추가. §2 에서 **정밀 인용(top-5 정확)** = search_reranked 1순위, **넓은 탐색·cross-standard·recall 필요** = search_hybrid 로 역할 분담 명시. reranked recall@20(0.853) < hybrid(0.907) tradeoff 한 줄.
  - AC: 배포본(`~/.claude/skills/accounting/SKILL.md`)에 반영
  - 금지: 배포본 직접 편집 금지(원본 수정 후 배포). search_hybrid 가이드 삭제 금지(역할 분담이지 대체 아님)

## DoD (milestone)

search_reranked MCP tool 노출 + warmup + SKILL.md 정밀 인용 1순위. MCP import·boot 무에러. → reranked 측정치(recall@5=0.640/MRR=0.612)가 인터랙티브 /accounting 경로에서 사용 가능.
