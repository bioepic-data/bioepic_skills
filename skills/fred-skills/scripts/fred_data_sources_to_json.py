#!/usr/bin/env python3
"""Download/convert FRED data sources to JSON/TSV (stdlib-only)."""
from __future__ import annotations

import argparse
import json
import ssl
import sys
from pathlib import Path
from urllib import parse, request

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from bioepic_skills.fred_parser import parse_display_range, parse_fred_data_sources_html

BASE_URL = "https://roots.ornl.gov/data-sources"


def _fetch(url: str, timeout: int, insecure: bool) -> str:
    req = request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0",
            "Accept": "text/html, text/plain",
        },
    )
    context = None
    if insecure:
        context = ssl._create_unverified_context()
    with request.urlopen(req, timeout=timeout, context=context) as resp:
        return resp.read().decode("utf-8", errors="replace")


def _try_variants(timeout: int, insecure: bool) -> str:
    variants = [
        BASE_URL,
        f"{BASE_URL}?page=all",
        f"{BASE_URL}?show=all",
        f"{BASE_URL}?display=all",
        f"{BASE_URL}?limit=2000",
        f"{BASE_URL}?per_page=2000",
        f"{BASE_URL}?items=2000",
        f"{BASE_URL}?pageSize=2000",
        f"{BASE_URL}?size=2000",
        f"{BASE_URL}?offset=0&limit=2000",
        f"{BASE_URL}?start=0&length=2000",
    ]
    best = None
    for url in variants:
        try:
            content = _fetch(url, timeout, insecure)
        except Exception:
            continue
        display = parse_display_range(content)
        if display:
            _start, end, total = display
            best = content
            if end >= total:
                return content
        elif best is None:
            best = content
    return best or ""


def _write_json(records, output_path: Path | None) -> None:
    payload = [record.__dict__ for record in records]
    if output_path:
        output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    else:
        print(json.dumps(payload, indent=2))


def _write_tsv(records, output_path: Path | None) -> None:
    lines = ["year\tcitation\tdoi"]
    for record in records:
        values = [
            "" if record.year is None else str(record.year),
            record.citation.replace("\t", " ").replace("\n", " "),
            record.doi or "",
        ]
        lines.append("\t".join(values))
    output = "\n".join(lines)
    if output_path:
        output_path.write_text(output + "\n", encoding="utf-8")
    else:
        print(output)


def main() -> int:
    parser = argparse.ArgumentParser(description="Download/convert FRED data sources")
    parser.add_argument(
        "--format",
        choices=["json", "tsv"],
        default="json",
        help="Output format (default: json)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Write output to file (defaults to stdout)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Request timeout in seconds (default: 30)",
    )
    parser.add_argument(
        "--insecure",
        action="store_true",
        help="Disable SSL certificate verification",
    )
    parser.add_argument(
        "--save",
        default=None,
        help="Save fetched HTML to a file",
    )

    args = parser.parse_args()
    html_text = _try_variants(args.timeout, args.insecure)
    if args.save:
        Path(args.save).write_text(html_text, encoding="utf-8")

    records = parse_fred_data_sources_html(html_text)

    output_path = Path(args.output) if args.output else None
    if args.format == "tsv":
        _write_tsv(records, output_path)
    else:
        _write_json(records, output_path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
