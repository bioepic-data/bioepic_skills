#!/usr/bin/env python3
"""Convert TRY species list text to JSON or TSV (stdlib-only)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from bioepic_skills.try_parser import parse_try_species_list_text, parse_try_species_text


def _write_json(species, output_path: Path | None) -> None:
    if not species:
        payload = []
    elif hasattr(species[0], "__dict__"):
        payload = [record.__dict__ for record in species]
    else:
        payload = [{"species": name} for name in species]
    if output_path:
        output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    else:
        print(json.dumps(payload, indent=2))


def _write_tsv(species, output_path: Path | None) -> None:
    if not species:
        lines = ["Species"]
    elif hasattr(species[0], "__dict__"):
        header = [
            "AccSpeciesID",
            "AccSpeciesName",
            "ObsNum",
            "ObsGRNum",
            "MeasNum",
            "MeasGRNum",
            "TraitNum",
            "PubNum",
            "AccSpecNum",
        ]
        lines = ["\t".join(header)]
        for record in species:
            lines.append(
                "\t".join(
                    [
                        "" if record.acc_species_id is None else str(record.acc_species_id),
                        record.acc_species_name,
                        "" if record.obs_num is None else str(record.obs_num),
                        "" if record.obs_gr_num is None else str(record.obs_gr_num),
                        "" if record.meas_num is None else str(record.meas_num),
                        "" if record.meas_gr_num is None else str(record.meas_gr_num),
                        "" if record.trait_num is None else str(record.trait_num),
                        "" if record.pub_num is None else str(record.pub_num),
                        "" if record.acc_spec_num is None else str(record.acc_spec_num),
                    ]
                )
            )
    else:
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
    first_line = text.splitlines()[0] if text else ""
    if "AccSpeciesID" in first_line and "\t" in first_line:
        species = parse_try_species_text(text)
    else:
        species = parse_try_species_list_text(text)

    output_path = Path(args.output) if args.output else None
    if args.format == "tsv":
        _write_tsv(species, output_path)
    else:
        _write_json(species, output_path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
