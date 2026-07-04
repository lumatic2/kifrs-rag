from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs.authority import load_source_pack, validate_source_pack  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-lev1-live-external-source-validation.md"

KNOWN_LIVE_LOCATORS = {
    "opendart-structured-financials-seed": "https://opendart.fss.or.kr/",
}


@dataclass(frozen=True)
class LiveProbeTarget:
    item_id: str
    source_id: str
    publisher: str
    allowed_use: str
    url: str


def collect_live_probe_targets() -> list[LiveProbeTarget]:
    targets: list[LiveProbeTarget] = []
    for item in load_source_pack().get("items", []):
        locator = item.get("locator", {})
        url = locator.get("url") if locator.get("kind") == "web_index" else None
        url = url or KNOWN_LIVE_LOCATORS.get(item.get("id", ""))
        if not url:
            continue
        targets.append(
            LiveProbeTarget(
                item_id=item["id"],
                source_id=item["source_id"],
                publisher=item["publisher"],
                allowed_use=item["allowed_use"],
                url=url,
            )
        )
    return targets


def default_fetcher(url: str, timeout: float) -> dict[str, object]:
    request = Request(url, headers={"User-Agent": "kifrs-rag-live-source-validation/1.0"})
    try:
        with urlopen(request, timeout=timeout) as response:
            return {
                "ok": 200 <= int(response.status) < 400,
                "status_code": int(response.status),
                "final_url": response.geturl(),
                "content_type": response.headers.get("content-type", ""),
                "error": "",
            }
    except HTTPError as exc:
        return {
            "ok": 400 <= int(exc.code) < 500,
            "status_code": int(exc.code),
            "final_url": url,
            "content_type": exc.headers.get("content-type", "") if exc.headers else "",
            "error": f"http_error:{exc.code}",
        }
    except (TimeoutError, URLError) as exc:
        return {
            "ok": False,
            "status_code": None,
            "final_url": url,
            "content_type": "",
            "error": type(exc).__name__,
        }


def validate_live_external_sources(
    *,
    allow_network: bool = False,
    timeout: float = 10.0,
    fetcher: Callable[[str, float], dict[str, object]] | None = None,
) -> dict[str, object]:
    source_pack = validate_source_pack()
    targets = collect_live_probe_targets()
    checks: list[dict[str, object]] = []
    errors: list[str] = []

    if not source_pack["ok"]:
        errors.extend(f"source_pack: {error}" for error in source_pack["errors"])
    if len(targets) < 2:
        errors.append("expected at least two external live probe targets")

    fetch = fetcher or default_fetcher
    for target in targets:
        row: dict[str, object] = {
            "item_id": target.item_id,
            "source_id": target.source_id,
            "publisher": target.publisher,
            "allowed_use": target.allowed_use,
            "url": target.url,
            "network_checked": allow_network,
            "body_text_stored": False,
        }
        if allow_network:
            probe = fetch(target.url, timeout)
            row.update(probe)
            if probe.get("ok") is not True:
                errors.append(f"{target.item_id}: live probe failed: {probe.get('error') or probe.get('status_code')}")
        else:
            row.update({"ok": None, "status_code": None, "final_url": "", "content_type": "", "error": "network_not_enabled"})
        checks.append(row)

    return {
        "ok": not errors,
        "errors": errors,
        "source_pack_ok": source_pack["ok"],
        "target_count": len(targets),
        "network_checked": allow_network,
        "body_text_stored": False,
        "checks": checks,
        "report_path": str(REPORT_PATH.relative_to(ROOT)),
        "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or opt-in retriever demo validation",
    }


def render_report(result: dict[str, object]) -> str:
    lines = [
        "# LEV1 Live External Source Validation",
        "",
        "> Scope: metadata-only live check for external authority source surfaces.",
        "",
        "## 한 줄 결론",
        "",
        "External source metadata now has a live validation gate. The gate checks link/API landing surfaces only and stores no source body text.",
        "",
        "## Check Results",
        "",
        f"- ok: {result['ok']}",
        f"- source_pack_ok: {result['source_pack_ok']}",
        f"- network_checked: {result['network_checked']}",
        f"- target_count: {result['target_count']}",
        f"- body_text_stored: {result['body_text_stored']}",
        "",
        "## Live Targets",
        "",
        "| Item | Publisher | Status | Final URL |",
        "|---|---|---:|---|",
    ]
    for check in result["checks"]:
        status = check.get("status_code") if check.get("network_checked") else "not checked"
        lines.append(f"| `{check['item_id']}` | {check['publisher']} | {status} | {check.get('final_url') or check['url']} |")

    lines.extend([
        "",
        "## Boundary",
        "",
        "- This report does not store KASB/FSS/OpenDART body text.",
        "- This report does not promote external sources above K-IFRS primary evidence.",
        "- This report does not implement body ingestion, OCR, crawling, or embeddings.",
        "",
        "## Next Leaf",
        "",
        str(result["next_leaf"]),
        "",
        "## Machine Result",
        "",
        "```json",
        json.dumps(result, ensure_ascii=False, indent=2, default=str),
        "```",
    ])
    return "\n".join(lines) + "\n"


def write_report(*, allow_network: bool = False, timeout: float = 10.0) -> dict[str, object]:
    result = validate_live_external_sources(allow_network=allow_network, timeout=timeout)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_report(result), encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate metadata-only external source live surfaces.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--allow-network", action="store_true")
    parser.add_argument("--timeout", type=float, default=10.0)
    args = parser.parse_args()

    result = write_report(allow_network=args.allow_network, timeout=args.timeout) if args.write else validate_live_external_sources(allow_network=args.allow_network, timeout=args.timeout)
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"source_pack_ok: {result['source_pack_ok']}")
        print(f"network_checked: {result['network_checked']}")
        print(f"target_count: {result['target_count']}")
        print(f"body_text_stored: {result['body_text_stored']}")
        print(f"next_leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
