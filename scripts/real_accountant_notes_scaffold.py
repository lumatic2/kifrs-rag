from __future__ import annotations

import argparse
from pathlib import Path


DEFAULT_OUT = Path("docs/reports/real-accountant-session/actual-feedback-notes.md")


def render_notes_scaffold(
    *,
    date: str = "YYYY-MM-DD",
    reviewer_role: str = "",
    reviewer_service_line: str = "",
    reviewer_experience_context: str = "",
    session_mode: str = "screen share / in-person / async review",
) -> str:
    return "\n".join(
        [
            "# Real Accountant Session Evidence",
            "",
            "> Public-safe actual feedback notes scaffold. Fill this after the real reviewer session. It must fail the notes checker until actual feedback fields and boundary confirmations are completed.",
            "",
            "## Session Metadata",
            "",
            f"- Date: {date}",
            f"- Reviewer role: {reviewer_role}",
            f"- Reviewer service-line: {reviewer_service_line}",
            f"- Reviewer experience context: {reviewer_experience_context}",
            f"- Session mode: {session_mode}",
            "- Actual feedback evidence: false until completed",
            "",
            "## Viewed Files",
            "",
            "- [ ] one-page brief",
            "- [ ] field-feedback runbook",
            "- [ ] demo bundle manifest",
            "- [ ] real-transaction PoC package",
            "- [ ] field-feedback capture package",
            "- [ ] feedback questionnaire",
            "- [ ] incorporated review question supplement",
            "",
            "## Scores",
            "",
            "- Workflow fit (1-5):",
            "- Evidence boundary clarity (1-5):",
            "- Review pack usefulness (1-5):",
            "- Human-review boundary clarity (1-5):",
            "- Real-case PoC willingness (1-5):",
            "",
            "## Top Positive",
            "",
            "TODO: summarize the strongest useful part in your own words.",
            "",
            "## Top Risk",
            "",
            "TODO: summarize the strongest risk in your own words.",
            "",
            "## Missing Inputs",
            "",
            "- TODO: structured fact or evidence request that is missing.",
            "",
            "## Review Question Additions",
            "",
            "- TODO: human-review question to add or revise.",
            "",
            "## Safe Correction Candidates",
            "",
            "### Candidate 1",
            "",
            "- Case id:",
            "- Issue:",
            "- Severity: low / medium / high / blocker",
            "- Suggested fix:",
            "- Missing evidence:",
            "- Disposition: eval_seed_candidate / backlog_candidate / no_action",
            "- Affected outputs:",
            "",
            "## Next Action",
            "",
            "- [ ] actual anonymized transaction can be provided",
            "- [ ] second review session needed",
            "- [ ] only wording/checklist changes needed",
            "- [ ] stop/pause",
            "",
            "## Boundary Confirmation",
            "",
            "- [ ] No raw contract copied",
            "- [ ] No customer/client/company identifier copied",
            "- [ ] No private filing body copied",
            "- [ ] No K-IFRS source text copied",
            "- [ ] Notes are safe to convert into queue candidates",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a public-safe actual-feedback notes scaffold.")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--date", default="YYYY-MM-DD")
    parser.add_argument("--reviewer-role", default="")
    parser.add_argument("--reviewer-service-line", default="")
    parser.add_argument("--reviewer-experience-context", default="")
    parser.add_argument("--session-mode", default="screen share / in-person / async review")
    args = parser.parse_args()

    text = render_notes_scaffold(
        date=args.date,
        reviewer_role=args.reviewer_role,
        reviewer_service_line=args.reviewer_service_line,
        reviewer_experience_context=args.reviewer_experience_context,
        session_mode=args.session_mode,
    )
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
