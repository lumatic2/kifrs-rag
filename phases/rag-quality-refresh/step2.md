# RQ2 — Eval Coverage Refresh

## Objective

RQ1에서 확인한 품질 gate를 질문 유형별 coverage 관점으로 재분류한다. 이번 step은 새 최적화를 바로
하지 않고, 어떤 질문군이 평가되고 있고 어떤 질문군이 비어 있는지 명확히 만든다.

## 읽어야 할 파일

- `docs/reports/2026-07-05-rq1-current-quality-baseline.md` — 왜: RQ1의 command inventory, timeout, miss ID를 이어받는다.
- `data/eval/goldset.json` — 왜: 현재 goldset 문항을 bucket별로 분류한다. 내용은 local-only boundary로 다룬다.
- `kifrs/eval/models.py` — 왜: GoldItem/Citation schema를 확인한다.
- `kifrs/eval/retrieval.py` — 왜: retrieval-only 평가가 어떤 ground truth를 쓰는지 확인한다.
- `scripts/eval_quality_gate.py` — 왜: 현재 answer gate가 어떤 문항만 쓰는지 확인한다.

## 작업

1. 현재 goldset 문항을 가능한 한 metadata 중심으로 분류한다.
2. RQ1에서 정한 coverage bucket별로 "covered / partial / missing"을 적는다.
3. public-safe gate에 들어갈 수 있는 최소 대표 문항군을 제안한다.
4. private/local-only로만 돌려야 하는 평가를 분리한다.

## Acceptance Criteria

```powershell
python scripts\quality_preflight.py --format text
git diff --check
```

## Deliverable

- `docs/reports/2026-07-05-rq2-eval-coverage-refresh.md`

## 금지사항

- 기준서 원문, 문제 원문, manual answer 전문을 report에 복사하지 않는다. 이유: 공개 레포 저작권/비공개 자료 경계.
- RQ2에서는 retrieval 최적화 코드를 고치지 않는다. 이유: coverage map을 먼저 고정해야 RQ3/RQ4 변경이 측정 가능하다.

