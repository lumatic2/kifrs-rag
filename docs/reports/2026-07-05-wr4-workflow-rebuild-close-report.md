# WR4 Workflow Rebuild Close Report

> Horizon: `workflow-rebuild-on-richer-knowledge`
> Date: 2026-07-05

## 한 줄 결론

`workflow-rebuild-on-richer-knowledge` horizon은 닫을 수 있다. 기존 1109/1115/1116 F-ACC review pack
24개를 multi-authority runtime evidence 위에서 다시 훑고, 자동화 상태·K-IFRS citation·외부 근거
role·synthetic fact evidence·NeedsHumanReview 항목을 같은 표로 계량했다.

## 무엇이 가능해졌나

### 1. 업무 산출물 단위 source coverage 측정

새 analyzer는 review pack별로 아래를 공통 측정한다.

- 자동화 상태: automated / needs_human_review
- primary K-IFRS citation count
- external evidence role count
- fact evidence count
- human-review item count

### 2. 1109/1115/1116 비교표

재생성 report 기준 현재 결과:

| Standard | Packs | Automated | Needs human review | Citations | Fact evidence refs | Human-review items |
|---|---:|---:|---:|---:|---:|---:|
| KIFRS1109 | 10 | 7 | 3 | 16 | 10 | 17 |
| KIFRS1115 | 4 | 4 | 0 | 28 | 4 | 4 |
| KIFRS1116 | 10 | 9 | 1 | 81 | 10 | 16 |

### 3. Public-safe 재생성 command

```powershell
python scripts\workflow_rebuild_report.py --out docs\reports\2026-07-05-wr3-source-aware-rebuild-report.md
```

이 command는 보호 본문 없이 public synthetic fixture와 metadata-only evidence manifest만 사용한다.

## 구현 산출물

- `kifrs/workflows/source_aware_rebuild.py`
- `scripts/workflow_rebuild_report.py`
- `tests/test_source_aware_rebuild.py`
- `docs/reports/2026-07-05-wr3-source-aware-rebuild-report.md`

## Close Gate

```powershell
python -m pytest tests\test_source_aware_rebuild.py tests\test_1109_review_pack.py tests\test_1115_review_pack.py tests\test_1116_review_pack.py tests\test_demo_poc.py -q
# 19 passed

python scripts\quality_preflight.py --format text
# ok: True
# public_safe: True

git diff --check
# no whitespace errors; LF -> CRLF warnings only
```

Pytest cache warning은 `.pytest_cache` 쓰기 권한 문제이고 테스트 실패는 아니다.

## Deliberately Out of Scope

- 새 회계 판단 로직 추가
- 외부 API 호출
- KASB/FSS 본문 fetch
- raw DART filing 저장
- external evidence를 primary K-IFRS evidence로 승격
- 사람 검토 항목 제거

## Next Horizon Recommendation

Recommended next horizon:

- `real-case-feedback-loop`

Why:

이제 demo package와 source-aware workflow rebuild report가 모두 있으므로, 다음은 익명화된 실제 업무 사례를
받아 review pack 입력으로 변환하고, 회계사 correction을 eval seed/backlog로 남기는 루프를 만드는 것이
자연스럽다.

Candidate milestones:

1. Anonymized case intake schema
2. Case-to-review-pack routing stub
3. Reviewer correction capture format
4. Eval seed/backlog conversion report
