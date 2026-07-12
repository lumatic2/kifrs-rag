# Changeset: PP2-S1 — 3D 기준서 우주 (/universe)

## Target

- ROADMAP milestone: PP2 — 인터랙션 + 콘텐츠 + close (`portfolio-viz-polish` horizon)
- Plan: `docs/plans/2026-07-12-portfolio-viz-polish.md` PP2-S1 (사용자 발제·승인 2026-07-12)

## Scope

- Files: `scripts/export_universe_graph.py`(신규), `web/public/universe/{index.html,graph.json}`(신규),
  `scripts/check_web_data_safety.py`(스캔 대상 +1), `web/src/pages/index.astro`(진입 링크)
- Reason: 기준서 관계망을 obsidian poc-graph(brain.askewly.com) 3D 뷰어로 탐색 —
  기존 2D d3 그래프는 개요용 유지, 우주는 심화 탐색용. 사이트 내 검색은 저작권 경계로 제외.
- Expected effect: `/universe/` 풀스크린 3D 그래프 — 기준서 star 100 + 절 위성 398 +
  계층 가상 노드 17(galaxy 4·cluster 13), 엣지 1,166(상호참조 655·contains 398·hierarchy 113).

## Contract

- Source of truth: `data/kifrs.db` → `export_universe_graph.py` → graph.json (재생성 가능).
  뷰어 원본은 poc-graph viewer.html — RAG/질문/auth UI 전부 제거(시각화 전용).
- Compatibility: **graph.json 에 body/gist/context 필드 금지** — 절 제목·개수·참조 관계만.
  gate(check_web_data_safety.py) 스캔 대상에 포함(최장 문자열 56자, 본문 스니펫 0건).
- Out of scope: system 레벨 계층(2계층으로 충분), 사이트 내 기준서 검색.

## Verification

- [x] Targeted tests: export 재실행 → 515 노드/1,166 엣지, 전 기준서 cluster 매핑(폴백 0) +
      no-body assert PASS + gate 5파일 PASS
- [x] CLI smoke: `npm run build` 통과, dist 에 universe/ 복사 확인
- [x] Integrated smoke: 실브라우저(localhost preview) — 3D 렌더·렌즈 전환(클러스터별)·계층
      태그·콘솔 에러 0. 오케스트레이터 게이트에서 엣지 불투명도 .46→.24, vault 잔재 문구
      5건(본문 패널/실제 노트/기억 우주) 교정
- [x] Dirty-tree review: 위 Scope 파일 + 계획 문서만

## Result

- Status: completed (2026-07-12)
- Evidence: universe-v3 스크린샷(스크래치패드), graph.json 통계 stdout
- Notes: 워커가 이식 중 원본 뷰어의 ask 참조 잔존 버그 3건(applyImmediateDetailState 등)을
  발견·수리. 재생성 = `.venv/Scripts/python scripts/export_universe_graph.py`.
