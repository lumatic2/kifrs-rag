# Step 1: statement-draft-surface-inventory

Status: completed

## 읽어야 할 파일

- `docs/horizons/f-acc-financial-statement-draft.md` — 왜: horizon 목표와 milestone sequence가 있다.
- `kifrs/workflows/kifrs1109/review_pack.py` — 왜: 금융상품 분류/분개 output source.
- `kifrs/workflows/kifrs1115/review_pack.py` — 왜: 수익/계약부채/금융요소 output source.
- `kifrs/workflows/kifrs1116/review_pack.py` — 왜: 리스 사용권자산/리스부채/주석 output source.

## 작업

기존 review pack output 중 재무제표 본문/표시 draft에 쓸 수 있는 field를 inventory로 정리한다.

## Acceptance Criteria

```powershell
git diff --check
```

## 결과물

- `docs/reports/2026-07-05-fs1-statement-draft-surface-inventory.md`

## 완료 요약

1109/1115/1116 review pack의 `journal_entry`, `journal_entries`, `classification`, `path`,
`measurement`, `disclosure_draft`, `needs_human_review` surface를 재무상태표/손익/OCI/주석 후보로
매핑했다. FS2는 이 inventory를 바탕으로 `StatementLineCandidate` schema와 기준서별 adapter를 만든다.
