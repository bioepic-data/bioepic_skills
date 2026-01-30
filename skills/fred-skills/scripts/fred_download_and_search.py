#!/usr/bin/env python3
"""Download FRED pages and search for keywords (stdlib-only)."""
from __future__ import annotations

import argparse
import re
import ssl
from urllib import request


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


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Download FRED pages and search for keywords (no external tools)."
    )
    parser.add_argument(
        "--page",
        choices=["traits", "species", "sources"],
        default="traits",
        help="Which FRED page to fetch (default: traits)",
    )
    parser.add_argument(
        "--pattern",
        default="snow|snowpack",
        help="Regex pattern to search for (case-insensitive)",
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
        help="Save fetched content to a file",
    )

    args = parser.parse_args()

    url_map = {
        "traits": "https://roots.ornl.gov/data-inventory",
        "species": "https://roots.ornl.gov/plant-species",
        "sources": "https://roots.ornl.gov/data-sources",
    }

    content = _fetch(url_map[args.page], args.timeout, args.insecure)
    if args.save:
        with open(args.save, "w", encoding="utf-8") as handle:
            handle.write(content)

    regex = re.compile(args.pattern, re.IGNORECASE)
    for line in content.splitlines():
        if regex.search(line):
            print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
