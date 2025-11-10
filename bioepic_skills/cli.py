# -*- coding: utf-8 -*-
"""
Command-line interface for bioepic_skills ontology grounding.

Provides convenient access to ontology search and term grounding via the command line.
"""
import json
import logging
import sys
from pathlib import Path
from typing import Optional

import typer
from rich import print as rprint
from rich.console import Console
from rich.table import Table
from rich.json import JSON
from rich.logging import RichHandler
from rich.panel import Panel
from rich.markdown import Markdown

from bioepic_skills.ontology_grounding import (
    search_ontology,
    get_term_details,
    ground_terms,
    list_ontologies,
)
from bioepic_skills.trowel_wrapper import (
    get_essdive_metadata,
    get_essdive_variables,
    match_term_lists,
)

app = typer.Typer(
    name="bioepic",
    help="BioEPIC Skills - Ontology grounding utilities using OAK",
    add_completion=False,
)

console = Console()
error_console = Console(stderr=True)


def setup_logging(verbose: int = 0):
    """Configure logging based on verbosity level."""
    if verbose == 0:
        level = logging.WARNING
    elif verbose == 1:
        level = logging.INFO
    else:
        level = logging.DEBUG
    
    logging.basicConfig(
        level=level,
        format="%(message)s",
        handlers=[RichHandler(console=console, rich_tracebacks=True)]
    )


@app.command()
def version():
    """Show version information."""
    console.print("BioEPIC Skills version 0.2.0", style="bold green")


@app.command()
def ontologies():
    """List available ontologies."""
    ontology_list = list_ontologies()
    
    table = Table(title="Available Ontologies", show_header=True)
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Description")
    table.add_column("Selector", style="dim")
    
    for ont in ontology_list:
        table.add_row(
            ont["id"],
            ont["name"],
            ont["description"],
            ont["selector"]
        )
    
    console.print(table)


@app.command()
def search(
    query: str = typer.Argument(..., help="Search term to look up"),
    ontology: Optional[str] = typer.Option(
        None,
        "--ontology", "-o",
        help="Ontology to search (e.g., 'bervo', 'envo', 'chebi'). Leave empty to search all."
    ),
    limit: int = typer.Option(
        10,
        "--limit", "-n",
        help="Maximum number of results to return"
    ),
    verbose: int = typer.Option(
        0,
        "--verbose", "-v",
        count=True,
        help="Increase verbosity (-v, -vv)"
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        help="Save results to JSON file"
    ),
):
    """
    Search for ontology terms.
    
    Examples:
    
        bioepic search "soil moisture" --ontology bervo
        
        bioepic search "temperature" --limit 5
        
        bioepic search "precipitation" -o bervo --output results.json
    """
    setup_logging(verbose)
    
    console.print(f"\n[bold]Searching for:[/bold] {query}")
    if ontology:
        console.print(f"[bold]Ontology:[/bold] {ontology}")
    else:
        console.print("[bold]Ontology:[/bold] All ontologies")
    console.print()
    
    with console.status("[bold green]Searching...", spinner="dots"):
        results = search_ontology(query, ontology, limit)
    
    if not results:
        error_console.print(f"[yellow]No results found for '{query}'[/yellow]")
        sys.exit(1)
    
    # Display results in a table
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Term ID", style="cyan", no_wrap=True)
    table.add_column("Ontology", style="magenta", no_wrap=True)
    table.add_column("Label", style="green")
    
    for term_id, ont_id, label in results:
        table.add_row(term_id, ont_id, label)
    
    console.print(table)
    console.print(f"\n[dim]Found {len(results)} results[/dim]\n")
    
    # Save to file if requested
    if output:
        output_data = [
            {"term_id": tid, "ontology_id": oid, "label": label}
            for tid, oid, label in results
        ]
        with open(output, "w") as f:
            json.dump(output_data, f, indent=2)
        console.print(f"[green]✓[/green] Results saved to {output}")


@app.command()
def term(
    term_id: str = typer.Argument(..., help="Term ID to retrieve (e.g., 'ENVO:00000001')"),
    ontology: Optional[str] = typer.Option(
        None,
        "--ontology", "-o",
        help="Ontology containing the term"
    ),
    verbose: int = typer.Option(
        0,
        "--verbose", "-v",
        count=True,
        help="Increase verbosity"
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        help="Save details to JSON file"
    ),
):
    """
    Get detailed information about a specific ontology term.
    
    Examples:
    
        bioepic term ENVO:00000001
        
        bioepic term CHEBI:17234 --ontology chebi
        
        bioepic term ENVO:00000001 --output term_details.json
    """
    setup_logging(verbose)
    
    console.print(f"\n[bold]Retrieving details for:[/bold] {term_id}\n")
    
    with console.status("[bold green]Fetching...", spinner="dots"):
        details = get_term_details(term_id, ontology)
    
    if "error" in details:
        error_console.print(f"[red]Error:[/red] {details['error']}")
        sys.exit(1)
    
    # Display term details
    console.print(Panel(
        f"[bold cyan]{details['term_id']}[/bold cyan]\n"
        f"[bold]{details['label']}[/bold]\n\n"
        f"{details.get('definition', 'No definition available')}",
        title="Term Details",
        border_style="cyan"
    ))
    
    # Display synonyms
    if details.get('synonyms'):
        console.print("\n[bold]Synonyms:[/bold]")
        for syn in details['synonyms']:
            console.print(f"  • {syn}")
    
    # Display relationships
    if details.get('relationships'):
        console.print("\n[bold]Relationships:[/bold]")
        for rel, fillers in details['relationships'].items():
            console.print(f"\n  [cyan]{rel}:[/cyan]")
            for filler in fillers:
                console.print(f"    → {filler['id']}: {filler['label']}")
    
    console.print()
    
    # Save to file if requested
    if output:
        with open(output, "w") as f:
            json.dump(details, f, indent=2)
        console.print(f"[green]✓[/green] Details saved to {output}")


@app.command()
def ground(
    terms: list[str] = typer.Argument(..., help="Terms to ground (space-separated)"),
    ontology: Optional[str] = typer.Option(
        None,
        "--ontology", "-o",
        help="Target ontology (e.g., 'bervo', 'envo')"
    ),
    threshold: float = typer.Option(
        0.8,
        "--threshold", "-t",
        help="Minimum confidence threshold (0.0-1.0)"
    ),
    limit: int = typer.Option(
        3,
        "--limit", "-n",
        help="Maximum matches per term"
    ),
    verbose: int = typer.Option(
        0,
        "--verbose", "-v",
        count=True,
        help="Increase verbosity"
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        help="Save grounding results to JSON file"
    ),
):
    """
    Ground text terms to ontology concepts.
    
    This command searches for ontology terms that best match your input text
    and returns confidence-scored matches.
    
    Examples:
    
        bioepic ground "soil moisture" "air temperature" "precipitation" --ontology bervo
        
        bioepic ground "pH" "salinity" --threshold 0.9
        
        bioepic ground "soil" "water" --ontology envo --output grounding.json
    """
    setup_logging(verbose)
    
    console.print(f"\n[bold]Grounding {len(terms)} terms[/bold]")
    if ontology:
        console.print(f"[bold]Target ontology:[/bold] {ontology}")
    else:
        console.print("[bold]Target ontology:[/bold] All ontologies")
    console.print(f"[bold]Threshold:[/bold] {threshold}\n")
    
    with console.status("[bold green]Grounding terms...", spinner="dots"):
        results = ground_terms(terms, ontology, threshold, limit)
    
    # Display results
    for text_term, matches in results.items():
        console.print(f"\n[bold cyan]'{text_term}'[/bold cyan]")
        
        if not matches:
            console.print("  [yellow]No matches found[/yellow]")
            continue
        
        table = Table(show_header=True, box=None, pad_edge=False)
        table.add_column("Term ID", style="cyan", no_wrap=True)
        table.add_column("Label", style="green")
        table.add_column("Ontology", style="magenta", no_wrap=True)
        table.add_column("Confidence", style="yellow", justify="right")
        
        for match in matches:
            table.add_row(
                match["term_id"],
                match["label"],
                match["ontology_id"],
                f"{match['confidence']:.2f}"
            )
        
        console.print(table)
    
    console.print()
    
    # Save to file if requested
    if output:
        with open(output, "w") as f:
            json.dump(results, f, indent=2)
        console.print(f"[green]✓[/green] Results saved to {output}")


@app.command()
def essdive_metadata(
    doi_file: Path = typer.Argument(..., help="Path to file containing DOIs (one per line)"),
    output_dir: Path = typer.Option(
        ".",
        "--output", "-o",
        help="Directory where output files should be written"
    ),
    verbose: int = typer.Option(
        0,
        "--verbose", "-v",
        count=True,
        help="Increase verbosity"
    ),
):
    """
    Retrieve metadata from ESS-DIVE for a list of DOIs.
    
    Requires ESSDIVE_TOKEN environment variable to be set.
    Get your token at: https://docs.ess-dive.lbl.gov/programmatic-tools/ess-dive-dataset-api#get-access
    
    Produces three output files:
    - results.tsv: Dataset metadata
    - frequencies.tsv: Variable frequency counts
    - filetable.tsv: List of data files
    
    Examples:
    
        bioepic essdive-metadata dois.txt
        
        bioepic essdive-metadata dois.txt --output ./data
    """
    setup_logging(verbose)
    
    console.print(f"\n[bold]Retrieving ESS-DIVE metadata[/bold]")
    console.print(f"DOI file: {doi_file}")
    console.print(f"Output directory: {output_dir}\n")
    
    try:
        with console.status("[bold green]Fetching metadata from ESS-DIVE...", spinner="dots"):
            output_files = get_essdive_metadata(str(doi_file), str(output_dir))
        
        console.print("[green]✓[/green] Metadata retrieval complete!\n")
        console.print("[bold]Output files:[/bold]")
        for name, path in output_files.items():
            console.print(f"  • {name}: [cyan]{path}[/cyan]")
        console.print()
        
    except Exception as e:
        error_console.print(f"[red]Error:[/red] {str(e)}")
        sys.exit(1)


@app.command()
def essdive_variables(
    filetable: Optional[Path] = typer.Option(
        None,
        "--filetable", "-f",
        help="Path to filetable.tsv (defaults to filetable.tsv in output directory)"
    ),
    output_dir: Path = typer.Option(
        ".",
        "--output", "-o",
        help="Directory where output files should be written"
    ),
    workers: int = typer.Option(
        10,
        "--workers", "-w",
        help="Number of parallel workers for file processing"
    ),
    verbose: int = typer.Option(
        0,
        "--verbose", "-v",
        count=True,
        help="Increase verbosity"
    ),
):
    """
    Extract variable names from ESS-DIVE data files.
    
    Must be run after essdive-metadata command. Extracts:
    - Variable names from data files (CSV, TSV, Excel)
    - Keywords from XML metadata files
    - Data dictionary contents
    
    Produces:
    - variable_names.tsv: All extracted variable names with metadata
    - data_dictionaries.tsv: Compiled data dictionary information
    
    Examples:
    
        bioepic essdive-variables
        
        bioepic essdive-variables --output ./data --workers 20
        
        bioepic essdive-variables --filetable ./data/filetable.tsv
    """
    setup_logging(verbose)
    
    console.print(f"\n[bold]Extracting ESS-DIVE variables[/bold]")
    console.print(f"Output directory: {output_dir}")
    console.print(f"Workers: {workers}\n")
    
    try:
        with console.status("[bold green]Extracting variables...", spinner="dots"):
            output_file = get_essdive_variables(
                str(filetable) if filetable else None,
                str(output_dir),
                workers
            )
        
        console.print(f"[green]✓[/green] Variable extraction complete!")
        console.print(f"Output file: [cyan]{output_file}[/cyan]\n")
        
    except Exception as e:
        error_console.print(f"[red]Error:[/red] {str(e)}")
        sys.exit(1)


@app.command()
def match_terms(
    terms_file: Path = typer.Argument(..., help="TSV file with terms in first column"),
    list_file: Path = typer.Argument(..., help="Text file with terms, one per line"),
    output: Optional[Path] = typer.Option(
        None,
        "--output", "-o",
        help="Output file path"
    ),
    fuzzy: bool = typer.Option(
        False,
        "--fuzzy", "-f",
        help="Enable fuzzy matching for terms without exact matches"
    ),
    threshold: float = typer.Option(
        80.0,
        "--threshold", "-t",
        help="Minimum similarity score (0-100) for fuzzy matches"
    ),
    verbose: int = typer.Option(
        0,
        "--verbose", "-v",
        count=True,
        help="Increase verbosity"
    ),
):
    """
    Match terms from a TSV file against a list of terms.
    
    Useful for checking which extracted terms match a reference list
    (e.g., which ESS-DIVE variables match BERVO terms).
    
    Examples:
    
        bioepic match-terms variable_names.tsv bervo_terms.txt
        
        bioepic match-terms variables.tsv reference.txt --fuzzy
        
        bioepic match-terms vars.tsv refs.txt --fuzzy --threshold 90
    """
    setup_logging(verbose)
    
    console.print(f"\n[bold]Matching terms[/bold]")
    console.print(f"Terms file: {terms_file}")
    console.print(f"Reference list: {list_file}")
    if fuzzy:
        console.print(f"Fuzzy matching enabled (threshold: {threshold})")
    console.print()
    
    try:
        with console.status("[bold green]Matching terms...", spinner="dots"):
            output_file = match_term_lists(
                str(terms_file),
                str(list_file),
                str(output) if output else None,
                fuzzy,
                threshold
            )
        
        console.print(f"[green]✓[/green] Term matching complete!")
        console.print(f"Output file: [cyan]{output_file}[/cyan]\n")
        
    except Exception as e:
        error_console.print(f"[red]Error:[/red] {str(e)}")
        sys.exit(1)


@app.command()
def info():
    """Show information about BioEPIC Skills and OAK."""
    info_text = """
# BioEPIC Skills - Ontology Grounding Toolkit

This tool provides functions for grounding terms to ontologies using the 
**Ontology Access Kit (OAK)** and extracting variables from ESS-DIVE datasets
using **trowel**.

## Key Features

### Ontology Grounding
- 🔍 **Search** ontologies for terms
- 📖 **Retrieve** detailed term information
- 🎯 **Ground** text terms to ontology concepts
- 🌐 **Access** multiple ontologies (BERVO, ENVO, ChEBI, NCBI Taxonomy, COMO, PO, MIXS)

### ESS-DIVE Data Extraction
- 📦 **Retrieve** dataset metadata from ESS-DIVE
- 🔬 **Extract** variable names from data files
- 🔗 **Match** extracted terms against reference lists

## Special Support for BERVO

**BERVO** (Biological and Environmental Research Variable Ontology) 
is accessed through BioPortal and provides comprehensive vocabulary for:

- Environmental research variables and conditions
- Earth science experimental variables
- Plant science measurements
- Geochemistry conditions
- Biological and physicochemical processes

## Quick Examples

Search BERVO for a term:
```bash
bioepic search "soil moisture" --ontology bervo
```

Ground multiple terms:
```bash
bioepic ground "air temperature" "precipitation" "soil pH" --ontology bervo
```

Get ESS-DIVE metadata:
```bash
bioepic essdive-metadata dois.txt --output ./data
```

Extract variables from ESS-DIVE datasets:
```bash
bioepic essdive-variables --output ./data
```

## Documentation

- OAK Documentation: https://incatools.github.io/ontology-access-kit/
- BERVO on BioPortal: https://bioportal.bioontology.org/ontologies/BERVO
- ESS-DIVE API: https://docs.ess-dive.lbl.gov/programmatic-tools/ess-dive-dataset-api
- trowel: https://github.com/bioepic-data/trowel
"""
    console.print(Markdown(info_text))


if __name__ == "__main__":
    app()
