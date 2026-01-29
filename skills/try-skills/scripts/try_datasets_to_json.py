#!/usr/bin/env python3
"""Convert TRY dataset list HTML to JSON or TSV (stdlib-only)."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from bioepic_skills.try_parser import parse_try_datasets_html_with_header


def _write_json(records, output_path: Path | None) -> None:
    if output_path:
        output_path.write_text(json.dumps(records, indent=2), encoding="utf-8")
    else:
        print(json.dumps(records, indent=2))


def _write_tsv(header, records, output_path: Path | None) -> None:
    lines = ["\t".join(header)]
    for record in records:
        lines.append("\t".join(record.get(col, "") for col in header))
    output = "\n".join(lines)
    if output_path:
        output_path.write_text(output + "\n", encoding="utf-8")
    else:
        print(output)


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert TRY dataset HTML to JSON/TSV")
    parser.add_argument(
        "html_path",
        help="Path to TRY dataset list HTML (downloaded from Data.php)",
    )
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

    args = parser.parse_args()
    html_text = Path(args.html_path).read_text(encoding="utf-8")
    header, records = parse_try_datasets_html_with_header(html_text)

    output_path = Path(args.output) if args.output else None
    if args.format == "tsv":
        _write_tsv(header, records, output_path)
    else:
        _write_json(records, output_path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
