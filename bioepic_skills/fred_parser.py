"""Helpers for parsing Fine-Root Ecology Database (FRED) tables."""
from __future__ import annotations

import html as html_lib
import re
from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Optional


@dataclass(frozen=True)
class FredTraitRecord:
    trait_category: str
    trait_type: str
    trait: str
    column_id: str
    description: str
    single_species_observations: Optional[int]
    multi_species_observations: Optional[int]
    total_observations: Optional[int]


@dataclass(frozen=True)
class FredSpeciesRecord:
    name: str
    observations: Optional[int]


@dataclass(frozen=True)
class FredDataSourceRecord:
    year: Optional[int]
    citation: str
    doi: Optional[str]


def _strip_trailing_period(value: str) -> str:
    trimmed = value.rstrip()
    # Remove trailing punctuation (periods/commas/semicolons) and whitespace.
    trimmed = re.sub(r"[\s\.,;]+$", "", trimmed)
    return trimmed.strip()


def _remove_doi_from_citation(citation: str, doi: Optional[str]) -> str:
    if not doi:
        return citation
    return citation.replace(doi, "").strip()


class _HtmlTablesParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._in_table = False
        self._in_cell = False
        self._current_row: list[str] = []
        self._current_table: list[list[str]] = []
        self.tables: list[list[list[str]]] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        lowered = tag.lower()
        if lowered == "table":
            self._in_table = True
            self._current_table = []
        elif self._in_table and lowered in {"td", "th"}:
            self._in_cell = True
            self._current_row.append("")

    def handle_endtag(self, tag: str) -> None:
        lowered = tag.lower()
        if lowered == "tr" and self._current_row:
            self._current_table.append([cell.strip() for cell in self._current_row])
            self._current_row = []
        elif lowered in {"td", "th"}:
            self._in_cell = False
        elif lowered == "table" and self._in_table:
            if self._current_table:
                self.tables.append(self._current_table)
            self._current_table = []
            self._in_table = False

    def handle_data(self, data: str) -> None:
        if self._in_cell and self._current_row:
            self._current_row[-1] += data


def _normalize_header(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def _select_table(html_text: str, required_headers: set[str]) -> Optional[list[list[str]]]:
    parser = _HtmlTablesParser()
    parser.feed(html_text)
    for table in parser.tables:
        if not table:
            continue
        header = [_normalize_header(cell) for cell in table[0]]
        if required_headers.issubset(set(header)):
            return table
    return None


def _html_to_text(html_text: str) -> list[str]:
    cleaned = re.sub(r"<script[\s\S]*?</script>", "", html_text, flags=re.IGNORECASE)
    cleaned = re.sub(r"<style[\s\S]*?</style>", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"<[^>]+>", "", cleaned)
    cleaned = html_lib.unescape(cleaned)
    return [line.strip() for line in cleaned.splitlines()]


def _to_int(value: str | None) -> Optional[int]:
    if value is None:
        return None
    stripped = value.strip()
    if stripped == "":
        return None
    try:
        return int(stripped)
    except ValueError:
        return None


def parse_fred_traits_html(html_text: str) -> list[FredTraitRecord]:
    table = _select_table(
        html_text,
        {
            "trait category",
            "trait type",
            "traits",
            "column id",
            "total observations",
        },
    )
    if not table or len(table) < 2:
        return []

    header = [_normalize_header(cell) for cell in table[0]]
    records: list[FredTraitRecord] = []
    for row in table[1:]:
        if not row:
            continue
        row_map = {header[i]: row[i].strip() if i < len(row) else "" for i in range(len(header))}
        records.append(
            FredTraitRecord(
                trait_category=row_map.get("trait category", ""),
                trait_type=row_map.get("trait type", ""),
                trait=row_map.get("traits", ""),
                column_id=row_map.get("column id", ""),
                description=row_map.get("description", ""),
                single_species_observations=_to_int(row_map.get("single-species observations")),
                multi_species_observations=_to_int(row_map.get("multi-species observations")),
                total_observations=_to_int(row_map.get("total observations")),
            )
        )
    return records


def parse_fred_species_html(html_text: str) -> list[FredSpeciesRecord]:
    table = _select_table(html_text, {"scientific name", "observations"})
    if not table:
        table = _select_table(html_text, {"name", "observations"})
    if table and len(table) >= 2:
        header = [_normalize_header(cell) for cell in table[0]]
        records: list[FredSpeciesRecord] = []
        for row in table[1:]:
            if not row:
                continue
            row_map = {header[i]: row[i].strip() if i < len(row) else "" for i in range(len(header))}
            name = row_map.get("scientific name") or row_map.get("name") or row[0].strip()
            observations = row_map.get("observations", "")
            records.append(
                FredSpeciesRecord(
                    name=name,
                    observations=_to_int(observations),
                )
            )
        return records

    lines = _html_to_text(html_text)
    records: list[FredSpeciesRecord] = []
    for line in lines:
        if not line:
            continue
        if line.lower().startswith("name") and "observ" in line.lower():
            continue
        match = re.match(r"^(?P<name>.+?)\s+(?P<count>\d+)$", line)
        if match:
            records.append(
                FredSpeciesRecord(
                    name=match.group("name").strip(),
                    observations=_to_int(match.group("count")),
                )
            )
    return records


def parse_fred_data_sources_html(html_text: str) -> list[FredDataSourceRecord]:
    table = _select_table(html_text, {"year", "citation"})
    if table and len(table) >= 2:
        header = [_normalize_header(cell) for cell in table[0]]
        records: list[FredDataSourceRecord] = []
        for row in table[1:]:
            if not row:
                continue
            row_map = {header[i]: row[i].strip() if i < len(row) else "" for i in range(len(header))}
            citation = row_map.get("citation", "")
            doi_match = re.search(r"https?://doi\.org/\S+", citation)
            doi = doi_match.group(0) if doi_match else row_map.get("doi") or None
            if doi:
                doi = _strip_trailing_period(doi)
            citation = _remove_doi_from_citation(citation, doi)
            citation = _strip_trailing_period(citation)
            records.append(
                FredDataSourceRecord(
                    year=_to_int(row_map.get("year")),
                    citation=citation,
                    doi=doi,
                )
            )
        return records

    lines = _html_to_text(html_text)
    records: list[FredDataSourceRecord] = []
    current_year: Optional[int] = None
    for line in lines:
        if not line:
            continue
        if re.match(r"^\d{4}$", line):
            current_year = _to_int(line)
            continue
        if line.lower().startswith("displaying"):
            continue
        if "http" not in line:
            continue
        doi_match = re.search(r"https?://doi\.org/\S+", line)
        doi = doi_match.group(0) if doi_match else None
        if doi:
            doi = _strip_trailing_period(doi)
        citation = _remove_doi_from_citation(line.strip(), doi)
        citation = _strip_trailing_period(citation)
        records.append(
            FredDataSourceRecord(
                year=current_year,
                citation=citation,
                doi=doi,
            )
        )
    return records


def parse_display_range(html_text: str) -> Optional[tuple[int, int, int]]:
    match = re.search(r"Displaying\s+(\d+)\s*-\s*(\d+)\s+of\s+(\d+)", html_text)
    if not match:
        return None
    return int(match.group(1)), int(match.group(2)), int(match.group(3))
