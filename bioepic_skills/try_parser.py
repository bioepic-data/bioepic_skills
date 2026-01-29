"""Helpers for parsing TRY dataset, trait, and species tables."""
from __future__ import annotations

import csv
from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Iterable, Optional, Tuple


@dataclass(frozen=True)
class TrySpeciesRecord:
    """Normalized representation of a TRY species row."""

    acc_species_id: Optional[int]
    acc_species_name: str
    obs_num: Optional[int]
    obs_gr_num: Optional[int]
    meas_num: Optional[int]
    meas_gr_num: Optional[int]
    trait_num: Optional[int]
    pub_num: Optional[int]
    acc_spec_num: Optional[int]


@dataclass(frozen=True)
class TryTraitRecord:
    """Normalized representation of a TRY trait row."""

    trait_id: Optional[int]
    trait: str
    obs_num: Optional[int]
    obs_gr_num: Optional[int]
    pub_num: Optional[int]
    acc_spec_num: Optional[int]


@dataclass(frozen=True)
class TryDatasetEntry:
    """Normalized representation of a TRY dataset entry."""

    title: str
    try_file_archive_id: Optional[str]
    rights_of_use: Optional[str]
    publication_date: Optional[str]
    version: Optional[str]
    author: Optional[str]
    contributors: Optional[str]
    reference_publication: Optional[str]
    reference_data_package: Optional[str]
    doi: Optional[str]
    format: Optional[str]
    file_name: Optional[str]
    description: Optional[str]
    geolocation: Optional[str]
    temporal_coverage: Optional[str]
    taxonomic_coverage: Optional[str]
    field_list: list[str]
    extra_fields: dict[str, str]


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


def _iter_rows(lines: Iterable[str]) -> Iterable[dict[str, str]]:
    reader = csv.DictReader(lines, delimiter="\t")
    for row in reader:
        yield {key: (value or "") for key, value in row.items()}


def parse_try_species_rows(lines: Iterable[str]) -> list[TrySpeciesRecord]:
    """Parse TRY species table rows from an iterable of lines."""
    records: list[TrySpeciesRecord] = []
    for row in _iter_rows(lines):
        records.append(
            TrySpeciesRecord(
                acc_species_id=_to_int(row.get("AccSpeciesID")),
                acc_species_name=row.get("AccSpeciesName", "").strip(),
                obs_num=_to_int(row.get("ObsNum")),
                obs_gr_num=_to_int(row.get("ObsGRNum")),
                meas_num=_to_int(row.get("MeasNum")),
                meas_gr_num=_to_int(row.get("MeasGRNum")),
                trait_num=_to_int(row.get("TraitNum")),
                pub_num=_to_int(row.get("PubNum")),
                acc_spec_num=_to_int(row.get("AccSpecNum")),
            )
        )
    return records


def parse_try_species_text(text: str) -> list[TrySpeciesRecord]:
    """Parse TRY species table rows from a text string."""
    return parse_try_species_rows(text.splitlines())


def parse_try_species_file(path: str) -> list[TrySpeciesRecord]:
    """Parse TRY species table rows from a TSV file on disk."""
    with open(path, "r", encoding="utf-8") as handle:
        return parse_try_species_rows(handle)


def parse_try_traits_html(html_text: str) -> list[TryTraitRecord]:
    """Parse TRY trait list table from HTML content."""
    header, rows = _select_html_table(html_text)
    if not rows:
        return []
    records: list[TryTraitRecord] = []
    for row in rows[1:]:
        if not row or len(row) < 2:
            continue
        row_map = {header[i]: row[i] if i < len(row) else "" for i in range(len(header))}
        records.append(
            TryTraitRecord(
                trait_id=_to_int(row_map.get("TraitID")),
                trait=row_map.get("Trait", "").strip(),
                obs_num=_to_int(row_map.get("ObsNum")),
                obs_gr_num=_to_int(row_map.get("ObsGRNum")),
                pub_num=_to_int(row_map.get("PubNum")),
                acc_spec_num=_to_int(row_map.get("AccSpecNum")),
            )
        )
    return records


def parse_try_species_list_text(text: str) -> list[str]:
    """Parse TRY species list text into a list of species names."""
    return [line.strip() for line in text.splitlines() if line.strip()]


def parse_try_datasets_html(html_text: str) -> list[dict[str, str]]:
    """Parse TRY dataset list table from HTML content."""
    _, records = parse_try_datasets_html_with_header(html_text)
    return records


def parse_try_datasets_html_with_header(
    html_text: str,
) -> Tuple[list[str], list[dict[str, str]]]:
    """Parse TRY dataset list table from HTML content, returning header + records."""
    header, rows = _select_html_table(html_text, prefer_dataset_headers=True)
    if not rows:
        return [], []
    return header, _rows_to_dicts(header, rows[1:])


def parse_try_dataset_entries_html(html_text: str) -> list[TryDatasetEntry]:
    """Parse TRY dataset entries from the datasets page HTML."""
    parser = _HtmlTablesParser()
    parser.feed(html_text)

    entries: list[TryDatasetEntry] = []
    for table in parser.tables:
        if not table or len(table) < 2:
            continue
        first_cell = table[0][0].strip() if table[0] else ""
        if "Title" not in first_cell:
            continue

        field_map: dict[str, str] = {}
        for row in table:
            if len(row) < 2:
                continue
            key = row[0].strip()
            value = row[1].strip()
            if key.endswith(":"):
                key = key[:-1].strip()
            if key:
                field_map[key] = value

        title = field_map.get("Title", "")
        field_list_raw = field_map.get("Field list", "")
        field_list = [item.strip() for item in field_list_raw.split(",") if item.strip()]

        entries.append(
            TryDatasetEntry(
                title=title,
                try_file_archive_id=field_map.get("TRY File Archive ID"),
                rights_of_use=field_map.get("Rights of use"),
                publication_date=field_map.get("Publication Date"),
                version=field_map.get("Version"),
                author=field_map.get("Author"),
                contributors=field_map.get("Contributors"),
                reference_publication=field_map.get("Reference to publication"),
                reference_data_package=field_map.get("Reference to data package"),
                doi=field_map.get("DOI"),
                format=field_map.get("Format"),
                file_name=field_map.get("File name"),
                description=field_map.get("Description"),
                geolocation=field_map.get("Geolocation"),
                temporal_coverage=field_map.get("Temporal coverage"),
                taxonomic_coverage=field_map.get("Taxonomic coverage"),
                field_list=field_list,
                extra_fields={
                    key: value
                    for key, value in field_map.items()
                    if key
                    not in {
                        "Title",
                        "TRY File Archive ID",
                        "Rights of use",
                        "Publication Date",
                        "Version",
                        "Author",
                        "Contributors",
                        "Reference to publication",
                        "Reference to data package",
                        "DOI",
                        "Format",
                        "File name",
                        "Description",
                        "Geolocation",
                        "Temporal coverage",
                        "Taxonomic coverage",
                        "Field list",
                    }
                },
            )
        )

    return entries


def _rows_to_dicts(header: list[str], rows: list[list[str]]) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for row in rows:
        if not row:
            continue
        record = {header[i]: row[i] if i < len(row) else "" for i in range(len(header))}
        if any(value.strip() for value in record.values()):
            records.append(record)
    return records


def _select_html_table(
    html_text: str,
    prefer_dataset_headers: bool = False,
) -> Tuple[list[str], list[list[str]]]:
    parser = _HtmlTablesParser()
    parser.feed(html_text)
    tables = parser.tables
    if not tables:
        return [], []

    best_table: list[list[str]] | None = None
    for table in tables:
        if len(table) < 2:
            continue
        header = [cell.strip() for cell in table[0]]
        if prefer_dataset_headers:
            if any("dataset" in cell.lower() for cell in header):
                return header, table
        if best_table is None:
            best_table = table

    if best_table is None:
        return [], []
    header = [cell.strip() for cell in best_table[0]]
    return header, best_table
