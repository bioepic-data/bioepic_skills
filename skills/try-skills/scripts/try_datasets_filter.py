#!/usr/bin/env python3
"""Filter TRY datasets JSON/TSV by keywords in field list or text fields."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def _load_json(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and "result" in data:
        return data["result"]
    if isinstance(data, list):
        return data
    return []


def _load_tsv(path: Path) -> list[dict]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines:
        return []
    header = lines[0].split("\t")
    records = []
    for line in lines[1:]:
        if not line.strip():
            continue
        parts = line.split("\t")
        records.append({header[i]: parts[i] if i < len(parts) else "" for i in range(len(header))})
    return records


def _as_text(record: dict, fields: list[str]) -> str:
    values = []
    for field in fields:
        value = record.get(field, "")
        if isinstance(value, list):
            value = ", ".join(value)
        elif isinstance(value, dict):
            value = json.dumps(value, ensure_ascii=False)
        values.append(str(value))
    return "\n".join(values)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Filter TRY datasets by keyword in field list or text fields"
    )
    parser.add_argument("input_path", help="Path to TRY datasets JSON/TSV")
    parser.add_argument(
        "--format",
        choices=["json", "tsv"],
        default="json",
        help="Input format (default: json)",
    )
    parser.add_argument(
        "--pattern",
        required=True,
        help="Regex pattern to match",
    )
    parser.add_argument(
        "--fields",
        default="title,description,field_list",
        help="Comma-separated fields to search",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Write filtered JSON to file (defaults to stdout)",
    )

    args = parser.parse_args()
    path = Path(args.input_path)
    records = _load_json(path) if args.format == "json" else _load_tsv(path)

    fields = [field.strip() for field in args.fields.split(",") if field.strip()]
    regex = re.compile(args.pattern, re.IGNORECASE)

    filtered = []
    for record in records:
        text = _as_text(record, fields)
        if regex.search(text):
            filtered.append(record)

    payload = json.dumps(filtered, indent=2)
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    else:
        print(payload)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
