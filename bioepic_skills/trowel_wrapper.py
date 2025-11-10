"""
Wrapper functions for trowel package functionality.

This module provides Python function interfaces to the trowel CLI commands,
making them available as agent-compatible functions.
"""

import os
import subprocess
from typing import Optional


def get_essdive_metadata(doi_file: str, output_dir: str = ".") -> dict[str, str]:
    """
    Get metadata from ESS-DIVE for a list of DOIs.

    Args:
        doi_file: Path to a file containing one DOI per line
        output_dir: Directory where output files should be written (default: current directory)

    Returns:
        Dictionary with paths to the generated files:
        - 'results': Path to results.tsv
        - 'frequencies': Path to frequencies.tsv
        - 'filetable': Path to filetable.tsv

    Raises:
        RuntimeError: If the command fails or ESSDIVE_TOKEN is not set
        FileNotFoundError: If the doi_file doesn't exist
    """
    if not os.path.exists(doi_file):
        raise FileNotFoundError(f"DOI file not found: {doi_file}")

    if not os.getenv("ESSDIVE_TOKEN"):
        raise RuntimeError(
            "ESSDIVE_TOKEN environment variable must be set. "
            "See https://docs.ess-dive.lbl.gov/programmatic-tools/ess-dive-dataset-api#get-access"
        )

    if not os.path.exists(output_dir):
        raise FileNotFoundError(f"Output directory not found: {output_dir}")

    cmd = ["trowel", "get-essdive-metadata", "--path", doi_file, "--outpath", output_dir]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"trowel command failed: {result.stderr}")

    return {
        "results": os.path.join(output_dir, "results.tsv"),
        "frequencies": os.path.join(output_dir, "frequencies.tsv"),
        "filetable": os.path.join(output_dir, "filetable.tsv"),
    }


def get_essdive_variables(
    filetable_path: Optional[str] = None,
    output_dir: str = ".",
    workers: int = 10,
) -> str:
    """
    Extract variable names from ESS-DIVE data files.

    This extracts variable names from data files, keywords from XML files,
    and compiles data dictionary information. Must be run after get_essdive_metadata.

    Args:
        filetable_path: Path to filetable.tsv (if None, looks for filetable.tsv in output_dir)
        output_dir: Directory where output files should be written (default: current directory)
        workers: Number of parallel workers for file processing (default: 10)

    Returns:
        Path to the variable_names.tsv output file

    Raises:
        RuntimeError: If the command fails
        FileNotFoundError: If the filetable doesn't exist
    """
    if not os.path.exists(output_dir):
        raise FileNotFoundError(f"Output directory not found: {output_dir}")

    cmd = ["trowel", "get-essdive-variables", "--outpath", output_dir, "--workers", str(workers)]

    if filetable_path:
        if not os.path.exists(filetable_path):
            raise FileNotFoundError(f"Filetable not found: {filetable_path}")
        cmd.extend(["--path", filetable_path])

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"trowel command failed: {result.stderr}")

    return os.path.join(output_dir, "variable_names.tsv")


def match_term_lists(
    terms_file: str,
    list_file: str,
    output: Optional[str] = None,
    fuzzy: bool = False,
    similarity_threshold: float = 80.0,
) -> str:
    """
    Match terms from a TSV file against a list of terms in another file.

    Args:
        terms_file: Path to a TSV file with terms in the first column
        list_file: Path to a file with terms, one per line
        output: Path where the output file should be written (optional)
        fuzzy: Enable fuzzy matching for terms without exact matches (default: False)
        similarity_threshold: Minimum similarity score (0-100) for fuzzy matches (default: 80.0)

    Returns:
        Path to the output file containing matched terms

    Raises:
        RuntimeError: If the command fails
        FileNotFoundError: If either input file doesn't exist
    """
    if not os.path.exists(terms_file):
        raise FileNotFoundError(f"Terms file not found: {terms_file}")

    if not os.path.exists(list_file):
        raise FileNotFoundError(f"List file not found: {list_file}")

    cmd = [
        "trowel",
        "match-term-lists",
        "--terms-file",
        terms_file,
        "--list-file",
        list_file,
    ]

    if output:
        cmd.extend(["--output", output])

    if fuzzy:
        cmd.append("--fuzzy")
        cmd.extend(["--similarity-threshold", str(similarity_threshold)])

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"trowel command failed: {result.stderr}")

    # Parse output to get the result file path
    if output:
        return output
    else:
        # Extract the output path from the command output
        for line in result.stdout.split("\n"):
            if "Matched terms written to" in line:
                return line.split("Matched terms written to")[-1].strip()

        raise RuntimeError("Could not determine output file path")
