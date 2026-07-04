from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DEFAULT_LEDGER = Path("docs/reports/real-accountant-session/outreach-log.sample.jsonl")
DEFAULT_ALIAS = "reviewer-001"
DEFAULT_CONTACTED_AT = "2026-07-05"
DEFAULT_FOLLOW_UP_BY = "2026-07-08"
DEFAULT_CHANNEL = "manual"
ALLOWED_RESPONSE = {"follow_up", "schedule", "decline"}


def build_response_packet(
    *,
    response: str,
    ledger_path: Path = DEFAULT_LEDGER,
    reviewer_alias: str = DEFAULT_ALIAS,
    contacted_at: str = DEFAULT_CONTACTED_AT,
    follow_up_by: str = DEFAULT_FOLLOW_UP_BY,
    channel: str = DEFAULT_CHANNEL,
) -> dict[str, Any]:
    if response not in ALLOWED_RESPONSE:
        raise ValueError(f"unsupported response: {response}")
    if not reviewer_alias.startswith("reviewer-"):
        raise ValueError("reviewer_alias must be a public-safe alias like reviewer-001")

    status = {"follow_up": "sent", "schedule": "scheduled", "decline": "declined"}[response]
    notes = {
        "follow_up": "follow-up sent",
        "schedule": "session scheduled",
        "decline": "reviewer declined",
    }[response]
    return {
        "reviewer_alias": reviewer_alias,
        "response": response,
        "message": _message_for(response),
        "boundary": [
            "Do not include reviewer real name, customer name, company name, contract text, or private filing body in the ledger.",
            "Keep scheduling details outside the public repo if they identify a person.",
        ],
        "ledger_update_command": _update_command(
            ledger_path=ledger_path,
            reviewer_alias=reviewer_alias,
            status=status,
            channel=channel,
            contacted_at=contacted_at,
            follow_up_by=follow_up_by,
            notes=notes,
        ),
    }


def render_text(packet: dict[str, Any]) -> str:
    lines = [
        "Real Accountant Outreach Response Packet",
        "",
        f"Reviewer alias: {packet['reviewer_alias']}",
        f"Response mode: {packet['response']}",
        "",
        "Message:",
        "",
        str(packet["message"]),
        "",
        "Boundary:",
    ]
    lines.extend(f"- {item}" for item in packet["boundary"])
    lines.extend(["", "After handling response, run:", "", str(packet["ledger_update_command"]), ""])
    return "\n".join(lines)


def _message_for(response: str) -> str:
    if response == "follow_up":
        return (
            "안녕하세요. 앞서 드린 회계 AI PoC 30분 피드백 요청 관련해 짧게 확인드립니다.\n\n"
            "고객자료나 계약 원문은 필요 없고, 화면 공유로 public-safe demo만 보여드릴 예정입니다. "
            "가능하신 시간대가 있으면 알려주시면 맞추겠습니다."
        )
    if response == "schedule":
        return (
            "가능한 시간 알려주셔서 감사합니다. 30분 세션에서는 public-safe demo만 보고, "
            "고객자료나 계약 원문은 받지 않겠습니다.\n\n"
            "세션 후에는 식별정보 없이 제품 개선용 요약 피드백만 기록하겠습니다."
        )
    return (
        "확인 감사합니다. 이번에는 어렵다는 점 이해했습니다.\n\n"
        "혹시 나중에 10분 정도 짧게 봐주실 수 있는 시점이 생기면 다시 여쭙겠습니다. "
        "고객자료나 식별정보는 요청하지 않겠습니다."
    )


def _update_command(
    *,
    ledger_path: Path,
    reviewer_alias: str,
    status: str,
    channel: str,
    contacted_at: str,
    follow_up_by: str,
    notes: str,
) -> str:
    return (
        "python scripts\\real_accountant_outreach_update.py "
        f"--ledger {ledger_path.as_posix()} "
        f"--reviewer-alias {reviewer_alias} "
        f"--status {status} "
        f"--channel {channel} "
        f"--contacted-at {contacted_at} "
        f"--follow-up-by {follow_up_by} "
        f'--notes "{notes}"'
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a public-safe response packet for accountant outreach.")
    parser.add_argument("--response", choices=sorted(ALLOWED_RESPONSE), required=True)
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--reviewer-alias", default=DEFAULT_ALIAS)
    parser.add_argument("--contacted-at", default=DEFAULT_CONTACTED_AT)
    parser.add_argument("--follow-up-by", default=DEFAULT_FOLLOW_UP_BY)
    parser.add_argument("--channel", default=DEFAULT_CHANNEL)
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    packet = build_response_packet(
        response=args.response,
        ledger_path=args.ledger,
        reviewer_alias=args.reviewer_alias,
        contacted_at=args.contacted_at,
        follow_up_by=args.follow_up_by,
        channel=args.channel,
    )
    if args.format == "json":
        print(json.dumps(packet, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_text(packet), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
