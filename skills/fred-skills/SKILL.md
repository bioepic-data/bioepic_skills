---
name: fred-skills
description: Skills for discovering traits, species, and data sources in the Fine-Root Ecology Database (FRED)
---

# Commands

There is no public FRED API. Use direct site pages and HTML tables:

- Trait inventory: https://roots.ornl.gov/data-inventory
- Species list: https://roots.ornl.gov/plant-species
- Data sources: https://roots.ornl.gov/data-sources

## Full details

### Trait inventory

Download the traits table (HTML) and convert to JSON/TSV.

```bash
python skills/fred-skills/scripts/fred_download_and_search.py --page traits --save fred_traits.html
python skills/fred-skills/scripts/fred_traits_to_json.py fred_traits.html --format json --output fred_traits.json
python skills/fred-skills/scripts/fred_traits_to_json.py fred_traits.html --format tsv --output fred_traits.tsv
```

If certificate validation fails, add `--insecure` to the download command.

### Species list

Download the species list (HTML) and convert to JSON/TSV.

```bash
python skills/fred-skills/scripts/fred_download_and_search.py --page species --save fred_species.html
python skills/fred-skills/scripts/fred_species_to_json.py fred_species.html --format json --output fred_species.json
python skills/fred-skills/scripts/fred_species_to_json.py fred_species.html --format tsv --output fred_species.tsv
```

If certificate validation fails, add `--insecure` to the download command.

### Data sources (pagination)

The data sources page shows only 50 rows at a time. The helper script attempts
common query parameters to request all rows at once. If the site does not
support a larger page size, the script falls back to the default page.

```bash
python skills/fred-skills/scripts/fred_data_sources_to_json.py --format json --output fred_sources.json
python skills/fred-skills/scripts/fred_data_sources_to_json.py --format tsv --output fred_sources.tsv
```

You can also save the downloaded HTML for inspection:

```bash
python skills/fred-skills/scripts/fred_data_sources_to_json.py --save fred_sources.html
```

If certificate validation fails, add `--insecure`.

### Search helpers

```bash
python skills/fred-skills/scripts/fred_download_and_search.py --page traits --pattern "snow|cold" --insecure
python skills/fred-skills/scripts/fred_download_and_search.py --page species --pattern "picea|abies" --insecure
python skills/fred-skills/scripts/fred_download_and_search.py --page sources --pattern "snow|alpine" --insecure
```

## Notes

- FRED pages may use server-side pagination; the data sources helper is best-effort.
- If HTML structure changes, update parsers in `bioepic_skills/fred_parser.py`.
