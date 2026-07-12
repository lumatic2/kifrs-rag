# Close Report: portfolio-viz-polish

> Date: 2026-07-12
> Horizon: `docs/horizons/portfolio-viz-polish.md` (closed)
> Input: 사용자 발제 예외 4건째 (3축 범위 확정 + 3D 우주 추가 승인)
> Close Result: `portfolio_viz_polished`

## 산출물 (changeset #47~#51)

- **PP1 비주얼 보강**: 한지/서가/인주 컨셉 정물 imagegen 6장(#49 codex 생성 + #50 반입) —
  히어로 도판(장서각) + 섹션 배너 4(원장/실제본/묵 번짐/인장). 어스회계법인(기업 실사)과
  의도적 차별화. texture-hanji.jpg 예비.
- **PP2-S1 3D 기준서 우주**(#47): obsidian poc-graph viewer 이식 — `/universe/` 풀스크린,
  515 노드(기준서 100·절 위성 398·계층 17)·1,166 엣지, RAG/auth UI 제거, 팔레트 사이트
  토큰화. graph.json 은 DB→`scripts/export_universe_graph.py` 재생성 가능.
- **PP2-S2 콘텐츠 확장**(#48): Ⅴ. drift 감시 루프 스토리(4단계+스탯 4타일) + Ⅵ. 수리 루프
  연대기(2회전 타임라인, before/after 지표) + account.askewly.com 상호 링크.
- **PP2-S3 재배포**(#51): kifrs.askewly.com 라이브 재검증.

## 경계 검증

- public-safe gate 5파일 PASS(universe/graph.json 스캔 대상 추가 — 최장 문자열 56자,
  본문 표본 17,244건 비포함). 신규 콘텐츠는 하드코딩 지표·날짜만. 우주 노드는
  번호·제목·개수·참조 관계만.

## 운영 노트

- **background `codex exec` 는 stdin 을 닫고(`</dev/null`) 실행** — stdin 대기로 startup
  hang(세션 파일 미생성, CPU 0.08s) 사례. kill 후 재실행으로 해결.
- codex 가 자기 몫 changeset(#49)을 스스로 기록 — 정본 채택, 오케스트레이터 changeset(#50)과
  범위 분리. 스크린샷 1장이 커밋에 섞여 즉시 untrack(4c4c217).
- 워커가 뷰어 이식 중 원본 잔존 버그 3건(ask 참조) 발견·수리.

## 크기 회고 (§A1)

- PP1 changeset 2개(생성+반입)로 적정 경계였으나 roadmap_sync 는 참조 형식 문제로 1개로
  집계(INFLATION 경고) — 실질은 step 2개짜리 milestone, 다음에도 같은 규모면 유지.
- PP2 는 changeset 3개(우주/콘텐츠/배포)로 적정.

## 잔여 (자체 착수 금지)

- 우주: 절 위성 노드에 시간축(개정일) 시각화, 모바일 터치 최적화 — 반응이 오면.
- texture-hanji.jpg 미사용 — 다음 비주얼 니즈 시 소비.
