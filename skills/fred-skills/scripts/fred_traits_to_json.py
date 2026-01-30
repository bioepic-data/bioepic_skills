#!/usr/bin/env python3
"""Convert FRED trait list HTML to JSON or TSV (stdlib-only)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from bioepic_skills.fred_parser import parse_fred_traits_html


def _write_json(records, output_path: Path | None) -> None:
    payload = [record.__dict__ for record in records]
    if output_path:
        output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    else:
        print(json.dumps(payload, indent=2))


def _write_tsv(records, output_path: Path | None) -> None:
    header = [
        "trait_category",
        "trait_type",
        "trait",
        "column_id",
        "description",
        "single_species_observations",
        "multi_species_observations",
        "total_observations",
    ]
    lines = ["\t".join(header)]
    for record in records:
        values = [
            record.trait_category,
            record.trait_type,
            record.trait,
            record.column_id,
            record.description.replace("\t", " ").replace("\n", " "),
            "" if record.single_species_observations is None else str(record.single_species_observations),
            "" if record.multi_species_observations is None else str(record.multi_species_observations),
            "" if record.total_observations is None else str(record.total_observations),
        ]
        lines.append("\t".join(values))
    output = "\n".join(lines)
    if output_path:
        output_path.write_text(output + "\n", encoding="utf-8")
    else:
        print(output)


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert FRED trait HTML to JSON/TSV")
    parser.add_argument(
        "html_path",
        help="Path to FRED trait list HTML (downloaded from data-inventory)",
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
    records = parse_fred_traits_html(html_text)

    output_path = Path(args.output) if args.output else None
    if args.format == "tsv":
        _write_tsv(records, output_path)
    else:
        _write_json(records, output_path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
