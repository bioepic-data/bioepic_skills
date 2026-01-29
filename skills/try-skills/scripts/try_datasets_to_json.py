#!/usr/bin/env python3
"""Convert TRY dataset list HTML to JSON or TSV (stdlib-only)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from bioepic_skills.try_parser import parse_try_dataset_entries_html


def _write_json(records, output_path: Path | None) -> None:
    if output_path:
        output_path.write_text(json.dumps(records, indent=2), encoding="utf-8")
    else:
        print(json.dumps(records, indent=2))


def _write_tsv(header, records, output_path: Path | None) -> None:
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
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Emit summary fields only (title, archive id, doi, description)",
    )

    args = parser.parse_args()
    html_text = Path(args.html_path).read_text(encoding="utf-8")
    entries = parse_try_dataset_entries_html(html_text)
    if args.summary:
        records = [
            {
                "title": entry.title,
                "try_file_archive_id": entry.try_file_archive_id,
                "doi": entry.doi,
                "description": entry.description,
            }
            for entry in entries
        ]
        header = ["title", "try_file_archive_id", "doi", "description"]
    else:
        records = [
            {
                **{k: v for k, v in entry.__dict__.items() if k != "extra_fields"},
                "extra_fields": entry.extra_fields,
            }
            for entry in entries
        ]
        if args.format == "tsv":
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
        else:
            header = []

    output_path = Path(args.output) if args.output else None
    if args.format == "tsv":
        _write_tsv(header, records, output_path)
    else:
        _write_json(records, output_path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
