#!/usr/bin/env python3
"""Convert TRY trait list HTML to JSON or TSV (stdlib-only)."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from bioepic_skills.try_parser import parse_try_traits_html


def _write_json(records, output_path: Path | None) -> None:
    payload = [record.__dict__ for record in records]
    if output_path:
        output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    else:
        print(json.dumps(payload, indent=2))


def _write_tsv(records, output_path: Path | None) -> None:
    lines = [
        "TraitID\tTrait\tObsNum\tObsGRNum\tPubNum\tAccSpecNum",
    ]
    for record in records:
        lines.append(
            "\t".join(
                [
                    "" if record.trait_id is None else str(record.trait_id),
                    record.trait,
                    "" if record.obs_num is None else str(record.obs_num),
                    "" if record.obs_gr_num is None else str(record.obs_gr_num),
                    "" if record.pub_num is None else str(record.pub_num),
                    "" if record.acc_spec_num is None else str(record.acc_spec_num),
                ]
            )
        )

    output = "\n".join(lines)
    if output_path:
        output_path.write_text(output + "\n", encoding="utf-8")
    else:
        print(output)


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert TRY trait HTML to JSON/TSV")
    parser.add_argument(
        "html_path",
        help="Path to TRY trait list HTML (downloaded from Prop023.php)",
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
    records = parse_try_traits_html(html_text)

    output_path = Path(args.output) if args.output else None
    if args.format == "tsv":
        _write_tsv(records, output_path)
    else:
        _write_json(records, output_path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
