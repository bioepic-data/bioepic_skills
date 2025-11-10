# -*- coding: utf-8 -*-
"""
Command-line interface for bioepic_skills.

Provides convenient access to BioEPIC API operations via the command line.
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

from bioepic_skills.api_search import APISearch
from bioepic_skills.data_processing import DataProcessing
from bioepic_skills.utils import parse_filter
from bioepic_skills.export_utils import export_records

app = typer.Typer(
    name="bioepic",
    help="BioEPIC Skills API utilities command-line interface",
    add_completion=False,
)

console = Console()
error_console = Console(stderr=True)

# Common options for all commands
env_option = typer.Option(
    "prod",
    "--env", "-e",
    help="API environment (prod or dev)",
    envvar="BIOEPIC_ENV"
)
verbose_option = typer.Option(
    0,
    "--verbose", "-v",
    count=True,
    help="Increase verbosity: -v (INFO: show API URLs and timing), -vv (DEBUG: show full requests/responses)"
)
format_option = typer.Option(
    "auto",
    "--format", "-f",
    help="Output format: json, csv, tsv, or auto (detect from file extension)"
)


def setup_logging(verbose: int = 0):
    """
    Configure logging based on verbosity level.

    Args:
        verbose: Verbosity level (0=WARNING, 1=INFO, 2+=DEBUG)
    """
    if verbose == 0:
        level = logging.WARNING
    elif verbose == 1:
        level = logging.INFO
    else:  # 2 or more
        level = logging.DEBUG

    logging.basicConfig(
        level=level,
        format="%(message)s",
        handlers=[RichHandler(console=console, rich_tracebacks=True, show_time=True, show_path=False)],
        force=True  # Override any existing logging configuration
    )


def _display_results(results, output: Optional[Path] = None, format: str = "auto"):
    """Display or export results to console or file."""
    if not results:
        console.print("[yellow]No results found.[/yellow]")
        return

    if output:
        export_records(results, output, format)
        console.print(f"[green]✓[/green] Exported {len(results)} record(s) to {output}")
    else:
        # Display to console
        json_output = JSON(json.dumps(results, indent=2))
        console.print(json_output)


@app.command()
def sample(
    id: Optional[str] = typer.Option(None, "--id", help="Get sample by ID"),
    filter: Optional[str] = typer.Option(None, "--filter", help="Filter query (YAML or JSON format)"),
    limit: int = typer.Option(10, "--limit", "-l", help="Maximum number of records to return"),
    all_pages: bool = typer.Option(False, "--all", "-a", help="Fetch all pages of results"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file (JSON/CSV/TSV)"),
    format: str = format_option,
    collection: str = typer.Option("samples", "--collection", "-c", help="Collection name to query"),
    env: str = env_option,
    verbose: int = verbose_option,
):
    """
    Search and retrieve sample records.

    Filter syntax supports both YAML and JSON formats:
    - Simple: 'name: test'
    - Nested: 'metadata.type: biological'
    - JSON with operators: '{"status": {"$eq": "active"}}'

    Examples:

    \b
        # Get a specific sample by ID
        bioepic sample --id sample-123

    \b
        # Simple YAML filter
        bioepic sample --filter 'type: biological' --limit 5

    \b
        # JSON filter with MongoDB operators
        bioepic sample --filter '{"status": "active"}' --all

    \b
        # Export to CSV
        bioepic sample --filter 'category: research' --limit 100 -o results.csv

    \b
        # Use different collection
        bioepic sample --collection experiments --filter 'status: completed'
    """
    setup_logging(verbose)
    client = APISearch(collection_name=collection, env=env)

    try:
        if id:
            results = client.get_record_by_id(record_id=id)
            _display_results([results] if isinstance(results, dict) else results, output, format)
        else:
            # Parse filter to handle both YAML and JSON
            parsed_filter = ""
            if filter:
                try:
                    parsed_filter = parse_filter(filter)
                except ValueError as e:
                    error_console.print(f"[red]Invalid filter syntax:[/red] {e}")
                    raise typer.Exit(1)

            results = client.get_records(filter=parsed_filter, max_page_size=limit, all_pages=all_pages)
            _display_results(results, output, format)
            
            # Show summary
            if results:
                console.print(f"\n[green]Retrieved {len(results)} record(s)[/green]")
    except Exception as e:
        error_console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def search(
    attribute: str = typer.Argument(..., help="Attribute name to search"),
    value: str = typer.Argument(..., help="Attribute value to match"),
    limit: int = typer.Option(10, "--limit", "-l", help="Maximum number of records to return"),
    all_pages: bool = typer.Option(False, "--all", "-a", help="Fetch all pages of results"),
    exact: bool = typer.Option(False, "--exact", help="Use exact matching instead of partial"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file (JSON/CSV/TSV)"),
    format: str = format_option,
    collection: str = typer.Option("samples", "--collection", "-c", help="Collection name to query"),
    env: str = env_option,
    verbose: int = verbose_option,
):
    """
    Search records by specific attribute values.

    Examples:

    \b
        # Search for samples by type
        bioepic search type biological --limit 20

    \b
        # Exact match search
        bioepic search id sample-123 --exact

    \b
        # Search and export all results
        bioepic search category research --all -o research_samples.json

    \b
        # Search in different collection
        bioepic search status active --collection experiments --all
    """
    setup_logging(verbose)
    client = APISearch(collection_name=collection, env=env)

    try:
        results = client.get_record_by_attribute(
            attribute_name=attribute,
            attribute_value=value,
            max_page_size=limit,
            all_pages=all_pages,
            exact_match=exact
        )
        
        _display_results(results, output, format)
        
        if results:
            console.print(f"\n[green]Found {len(results)} matching record(s)[/green]")
    except Exception as e:
        error_console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def collections(
    env: str = env_option,
    verbose: int = verbose_option,
):
    """
    List available collections in the API.

    Example:

    \b
        bioepic collections
    """
    setup_logging(verbose)
    
    # This would require implementation in api_base.py
    console.print("[yellow]Collection listing not yet implemented.[/yellow]")
    console.print("[dim]Commonly used collections: samples, experiments, data_objects[/dim]")


@app.command()
def version():
    """Show version information."""
    from bioepic_skills import __version__
    console.print(f"[bold]BioEPIC Skills[/bold] version [cyan]{__version__}[/cyan]")


@app.command()
def info(
    env: str = env_option,
):
    """Show API configuration and connection info."""
    from bioepic_skills.api_base import APIBase
    
    api = APIBase(env=env)
    
    table = Table(title="BioEPIC API Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Environment", env)
    table.add_row("Base URL", api.base_url)
    
    console.print(table)


def main():
    """Main entry point for CLI."""
    app()


if __name__ == "__main__":
    main()
