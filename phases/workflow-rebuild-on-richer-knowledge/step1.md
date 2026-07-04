# Step WR1: Source-Aware Rebuild Plan and Phase Setup

## 읽어야 할 파일

- `docs/horizons/accounting-intelligence-expansion.md` - 왜: Horizon 5의 의존 순서와 산출물 범위를 확인한다.
- `docs/horizons/multi-authority-runtime-integration.md` - 왜: runtime evidence가 어디까지 연결됐는지 확인한다.
- `docs/ARCHITECTURE.md` - 왜: review pack은 기존 판단 엔진을 감싸는 orchestration layer라는 경계를 지킨다.
- `CLAUDE.md` - 왜: 보호 자료 commit 금지와 제품 north star를 확인한다.

## 작업

`workflow-rebuild-on-richer-knowledge` horizon과 phase status machine을 생성한다. 이번 horizon은
1109/1115/1116 review pack을 대상으로 source-aware coverage를 측정한다.

## Acceptance Criteria

```powershell
Test-Path docs\horizons\workflow-rebuild-on-richer-knowledge.md
Test-Path phases\workflow-rebuild-on-richer-knowledge\index.json
```

## 검증 절차

1. 위 AC를 실행한다.
2. protected body/source text를 새 파일에 넣지 않았는지 확인한다.
3. `phases/workflow-rebuild-on-richer-knowledge/index.json`의 WR1을 completed로 업데이트한다.

## 금지사항

- 기준서 원문, KASB/FSS 본문, DART raw filing, private DB/embedding을 쓰지 않는다.
- 새 판단 로직을 이 step에서 만들지 않는다. 이유: WR1은 계획/장부 setup이다.
