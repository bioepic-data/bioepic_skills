#!/usr/bin/env python3
"""CLI-free ESS-DIVE Dataset API helper (stdlib-only)."""
from __future__ import annotations

import argparse
import json
import os
import sys
from urllib import parse, request, error

DEFAULT_BASE_URL = "https://api.ess-dive.lbl.gov/"
DEFAULT_TIMEOUT = 30
USER_HEADERS = {
    "user_agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0",
    "content-type": "application/json",
    "Range": "bytes=0-1000",
}


def _build_url(base_url: str, path: str, params: dict[str, str] | None) -> str:
    base = base_url if base_url.endswith("/") else f"{base_url}/"
    url = parse.urljoin(base, path.lstrip("/"))
    if params:
        url = f"{url}?{parse.urlencode(params)}"
    return url


def _request_json(url: str, token: str | None, timeout: int) -> dict:
    headers = {
        "Accept": "application/json",
        "User-Agent": USER_HEADERS["user_agent"],
        "Content-Type": USER_HEADERS["content-type"],
        "Range": USER_HEADERS["Range"],
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = request.Request(url, headers=headers, method="GET")
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            payload = resp.read().decode("utf-8")
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore") if exc.fp else ""
        raise SystemExit(f"HTTP {exc.code}: {detail}") from exc
    except error.URLError as exc:
        raise SystemExit(f"Request failed: {exc.reason}") from exc

    try:
        return json.loads(payload)
    except json.JSONDecodeError as exc:
        raise SystemExit("Response was not valid JSON") from exc


def _load_token(path: str | None) -> str | None:
    if not path:
        return None
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read().strip() or None
    except OSError as exc:
        raise SystemExit(f"Failed to read token file: {exc}") from exc


def cmd_search(args: argparse.Namespace) -> int:
    if args.page_size < 0:
        raise SystemExit("--page-size must be >= 0")
    if args.row_start < 0:
        raise SystemExit("--row-start must be >= 0")
    params: dict[str, str] = {
        "isPublic": "false" if args.include_private else "true",
        "page_size": str(args.page_size),
        "row_start": str(args.row_start),
    }
    if args.keyword:
        params["text"] = args.keyword
    if args.provider_name:
        params["providerName"] = args.provider_name
    if args.param:
        for item in args.param:
            if "=" not in item:
                raise SystemExit("--param must be in key=value form")
            key, value = item.split("=", 1)
            if not key:
                raise SystemExit("--param key cannot be empty")
            params[key] = value

    url = _build_url(args.base_url, "packages", params)
    if args.debug_url:
        print(f"DEBUG URL: {url}", file=sys.stderr)
    token = args.token or _load_token(args.token_file) or os.getenv("ESSDIVE_TOKEN")
    data = _request_json(url, token, args.timeout)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2)
    else:
        print(json.dumps(data, indent=2))
    return 0


def cmd_dataset(args: argparse.Namespace) -> int:
    params = {
        "isPublic": "false" if args.include_private else "true",
    }
    url = _build_url(args.base_url, f"packages/{args.package_id}", params)
    if args.debug_url:
        print(f"DEBUG URL: {url}", file=sys.stderr)
    token = args.token or _load_token(args.token_file) or os.getenv("ESSDIVE_TOKEN")
    data = _request_json(url, token, args.timeout)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2)
    else:
        print(json.dumps(data, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="ESS-DIVE Dataset API helper (no external dependencies)."
    )
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help="ESS-DIVE API base URL",
    )
    parser.add_argument(
        "--token",
        default=None,
        help="ESS-DIVE API token (or set ESSDIVE_TOKEN)",
    )
    parser.add_argument(
        "--token-file",
        default=None,
        help="Path to a file containing the ESS-DIVE token",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help="Request timeout in seconds (default: 30)",
    )
    parser.add_argument(
        "--debug-url",
        action="store_true",
        help="Print the resolved request URL to stderr",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    search = subparsers.add_parser("search", help="Search datasets")
    search.add_argument("--keyword", "-k", help="Search text (maps to API text parameter)")
    search.add_argument(
        "--provider-name", "-p", help="Provider/project name (providerName)"
    )
    search.add_argument(
        "--page-size",
        type=int,
        default=25,
        help="Number of records per page (must be >= 0)",
    )
    search.add_argument(
        "--row-start",
        type=int,
        default=0,
        help="Row offset for pagination (must be >= 0)",
    )
    search.add_argument(
        "--include-private",
        action="store_true",
        help="Include private datasets (requires token)",
    )
    search.add_argument(
        "--param",
        action="append",
        help="Extra query parameter in key=value form",
    )
    search.add_argument(
        "--output",
        "-o",
        help="Write JSON response to a file instead of stdout",
    )
    search.set_defaults(func=cmd_search)

    dataset = subparsers.add_parser("dataset", help="Fetch a dataset by ID")
    dataset.add_argument("package_id", help="ESS-DIVE package ID")
    dataset.add_argument(
        "--include-private",
        action="store_true",
        help="Include private datasets (requires token)",
    )
    dataset.add_argument(
        "--output",
        "-o",
        help="Write JSON response to a file instead of stdout",
    )
    dataset.set_defaults(func=cmd_dataset)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
