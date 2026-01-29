#!/usr/bin/env python3
"""Download TRY pages and search for keywords (stdlib-only)."""
from __future__ import annotations

import argparse
import json
import re
import ssl
import sys
from pathlib import Path
from urllib import request

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from bioepic_skills.try_parser import parse_try_dataset_entries_html

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
        description="Download TRY pages and search for keywords (no external tools)."
    )
    parser.add_argument(
        "--page",
        choices=["datasets", "traits", "species"],
        default="datasets",
        help="Which TRY page to fetch (default: datasets)",
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
    parser.add_argument(
        "--convert-datasets",
        action="store_true",
        help="Convert downloaded dataset page to JSON/TSV (datasets only)",
    )
    parser.add_argument(
        "--convert-format",
        choices=["json", "tsv"],
        default="json",
        help="Output format for conversion (default: json)",
    )
    parser.add_argument(
        "--convert-output",
        default=None,
        help="Write converted output to file (defaults to stdout)",
    )

    args = parser.parse_args()

    url_map = {
        "datasets": "https://www.try-db.org/TryWeb/Data.php",
        "traits": "https://www.try-db.org/TryWeb/Prop023.php",
        "species": "https://www.try-db.org/dnld/TryAccSpecies.txt",
    }

    content = _fetch(url_map[args.page], args.timeout, args.insecure)
    regex = re.compile(args.pattern, re.IGNORECASE)
    if args.save:
        with open(args.save, "w", encoding="utf-8") as handle:
            handle.write(content)

    if args.convert_datasets:
        if args.page != "datasets":
            raise SystemExit("--convert-datasets can only be used with --page datasets")
        entries = parse_try_dataset_entries_html(content)
        records = [
            {
                **{k: v for k, v in entry.__dict__.items() if k != "extra_fields"},
                "extra_fields": entry.extra_fields,
            }
            for entry in entries
        ]
        if args.convert_format == "tsv":
            header = [
                "title",
                "try_file_archive_id",
                "rights_of_use",
                "publication_date",
                "version",
                "author",
                "contributors",
                "reference_publication",
                "reference_data_package",
                "doi",
                "format",
                "file_name",
                "description",
                "geolocation",
                "temporal_coverage",
                "taxonomic_coverage",
                "field_list",
                "extra_fields",
            ]
            lines = ["\t".join(header)]
            for record in records:
                row = []
                for col in header:
                    value = record.get(col, "")
                    if isinstance(value, list):
                        value = ", ".join(value)
                    elif isinstance(value, dict):
                        value = json.dumps(value, ensure_ascii=False)
                    if isinstance(value, str):
                        value = value.replace("\t", " ").replace("\r", " ").replace("\n", " ")
                    row.append(value)
                lines.append("\t".join(row))
            output = "\n".join(lines) + "\n"
            if args.convert_output:
                with open(args.convert_output, "w", encoding="utf-8") as handle:
                    handle.write(output)
            else:
                print(output)
        else:
            if args.convert_output:
                with open(args.convert_output, "w", encoding="utf-8") as handle:
                    json.dump(records, handle, indent=2)
            else:
                print(json.dumps(records, indent=2))

    for line in content.splitlines():
        if regex.search(line):
            print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
