#!/usr/bin/env python3
"""Convert TRY species list text to JSON or TSV (stdlib-only)."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from bioepic_skills.try_parser import parse_try_species_list_text


def _write_json(species, output_path: Path | None) -> None:
    payload = [{"species": name} for name in species]
    if output_path:
        output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    else:
        print(json.dumps(payload, indent=2))


def _write_tsv(species, output_path: Path | None) -> None:
    lines = ["Species"]
    lines.extend(species)
    output = "\n".join(lines)
    if output_path:
        output_path.write_text(output + "\n", encoding="utf-8")
    else:
        print(output)


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert TRY species list to JSON/TSV")
    parser.add_argument(
        "species_path",
        help="Path to TRY species list text (TryAccSpecies.txt)",
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
    text = Path(args.species_path).read_text(encoding="utf-8")
    species = parse_try_species_list_text(text)

    output_path = Path(args.output) if args.output else None
    if args.format == "tsv":
        _write_tsv(species, output_path)
    else:
        _write_json(species, output_path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
