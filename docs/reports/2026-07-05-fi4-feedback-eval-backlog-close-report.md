# FI4 Feedback Eval Backlog Close Report

> Horizon: `feedback-eval-backlog-integration`
> Date: 2026-07-05

## 한 줄 결론

`feedback-eval-backlog-integration` horizon은 닫을 수 있다. 회계사 correction candidate를 public-safe
JSONL queue로 저장하고, eval seed 후보와 product backlog 후보를 분리해 markdown report로 볼 수 있게 했다.

## 무엇이 가능해졌나

### 1. Feedback queue 저장

`FeedbackQueueRecord`는 validated case/correction에서만 생성된다.

저장 필드:

- case id
- domain
- review-pack route
- disposition
- severity
- issue
- expected improvement
- missing evidence
- affected outputs

### 2. Eval/backlog split

현재 sample queue:

| Bucket | Count |
|---|---:|
| Eval seed candidates | 1 |
| Backlog candidates | 1 |
| No-action records | 0 |
| High/blocker severity | 1 |

### 3. 재생성 command

```powershell
python scripts\feedback_queue_report.py --queue docs\feedback\feedback_queue.sample.jsonl --out docs\reports\2026-07-05-fi3-feedback-queue-report.md
```

## 구현 산출물

- `kifrs/feedback/queue.py`
- `tests/test_feedback_queue.py`
- `scripts/feedback_queue_report.py`
- `docs/feedback/feedback_queue.sample.jsonl`
- `docs/reports/2026-07-05-fi3-feedback-queue-report.md`

## Close Gate

```powershell
python -m pytest tests\test_feedback_queue.py tests\test_real_case_feedback.py -q
# 16 passed

python scripts\quality_preflight.py --format text
# ok: True
# public_safe: True

git diff --check
# no whitespace errors; LF -> CRLF warnings only
```

Pytest cache warning은 `.pytest_cache` 쓰기 권한 문제이고 테스트 실패는 아니다.

## Deliberately Out of Scope

- 실제 회계사 correction 수집
- private client workpaper 저장
- raw contract, customer identifier, source body 저장
- eval runner에 seed를 자동 편입
- backlog issue tracker 연동

## Next Horizon Recommendation

Recommended next horizon:

- `toolkit-packaging-readiness`

Why:

Accounting Intelligence Expansion의 핵심 루프는 이제 이어졌다: source-aware demo -> anonymized intake ->
reviewer correction -> eval/backlog queue. 다음은 회계법인 소개/PoC로 가기 위해 로컬 도구킷 설치·실행·
demo 재현 절차를 하나의 readiness package로 정리하는 단계가 자연스럽다.
