---
name: try-skills
description: Skills for discovering datasets, traits, and species information from the TRY plant trait database
---

# Commands

There is no public TRY API. Use direct site pages and published lists:

- Datasets list: https://www.try-db.org/TryWeb/Data.php
- Trait list (TRY properties): https://www.try-db.org/TryWeb/Prop023.php
- Species list with annotations: https://www.try-db.org/dnld/TryAccSpecies.txt

## Full details

### Dataset discovery

Use the TRY datasets list page to locate datasets by keyword (e.g., "snow", "leaf",
"trait", "root"). Because there is no API, prefer:

- Browser search (Ctrl/Cmd+F on the Data.php page)
- Downloading the page and searching locally with `rg`

Example local search workflow (curl + rg):

```bash
curl -sL "https://www.try-db.org/TryWeb/Data.php" -o try_datasets.html
rg -ni "snow|pack|alpine|tundra" try_datasets.html
```

If `rg` is unavailable, use `grep`:

```bash
curl -sL "https://www.try-db.org/TryWeb/Data.php" -o try_datasets.html
grep -iE "snow|pack|alpine|tundra" try_datasets.html
```

If `curl` fails, try `wget`:

```bash
wget -O try_datasets.html "https://www.try-db.org/TryWeb/Data.php"
grep -iE "snow|pack|alpine|tundra" try_datasets.html
```

If certificate validation fails, use:

```bash
wget -O try_datasets.html "https://www.try-db.org/TryWeb/Data.php" --no-check-certificate
grep -iE "snow|pack|alpine|tundra" try_datasets.html
```

If certificate validation fails with curl, use:

```bash
curl -sL -k "https://www.try-db.org/TryWeb/Data.php" -o try_datasets.html
grep -iE "snow|pack|alpine|tundra" try_datasets.html
```

Pure Python fallback (no curl/wget/rg/grep required):

```bash
python skills/try-skills/scripts/try_download_and_search.py --page datasets --pattern "snow|snowpack"
```

If certificate validation fails, use:

```bash
python skills/try-skills/scripts/try_download_and_search.py --page datasets --pattern "snow|snowpack" --insecure
```

Save the downloaded HTML for later parsing:

```bash
python skills/try-skills/scripts/try_download_and_search.py --page datasets --pattern "snow|snowpack" --insecure --save try_datasets.html
```

Download + convert to JSON or TSV in one step:

```bash
python skills/try-skills/scripts/try_download_and_search.py --page datasets --insecure --convert-datasets --convert-format json --convert-output try_datasets.json
```

```bash
python skills/try-skills/scripts/try_download_and_search.py --page datasets --insecure --convert-datasets --convert-format tsv --convert-output try_datasets.tsv
```

### Trait list access

Use the TRY properties page for the authoritative trait list. You can download and
search it locally if needed.

```bash
curl -sL "https://www.try-db.org/TryWeb/Prop023.php" -o try_traits.html
rg -ni "snow|cold|temperature|alpine" try_traits.html
```

If `rg` is unavailable, use `grep`:

```bash
curl -sL "https://www.try-db.org/TryWeb/Prop023.php" -o try_traits.html
grep -iE "snow|cold|temperature|alpine" try_traits.html
```

If `curl` fails, try `wget`:

```bash
wget -O try_traits.html "https://www.try-db.org/TryWeb/Prop023.php"
grep -iE "snow|cold|temperature|alpine" try_traits.html
```

If certificate validation fails, use:

```bash
wget -O try_traits.html "https://www.try-db.org/TryWeb/Prop023.php" --no-check-certificate
grep -iE "snow|cold|temperature|alpine" try_traits.html
```

If certificate validation fails with curl, use:

```bash
curl -sL -k "https://www.try-db.org/TryWeb/Prop023.php" -o try_traits.html
grep -iE "snow|cold|temperature|alpine" try_traits.html
```

Pure Python fallback (no curl/wget/rg/grep required):

```bash
python skills/try-skills/scripts/try_download_and_search.py --page traits --pattern "snow|cold|temperature|alpine"
```

If certificate validation fails, use:

```bash
python skills/try-skills/scripts/try_download_and_search.py --page traits --pattern "snow|cold|temperature|alpine" --insecure
```

### Species list access

The species list is a plain text file with one species per line.

```bash
curl -sL "https://www.try-db.org/dnld/TryAccSpecies.txt" -o try_species.txt
rg -ni "abies|picea|pinus" try_species.txt
```

If `rg` is unavailable, use `grep`:

```bash
curl -sL "https://www.try-db.org/dnld/TryAccSpecies.txt" -o try_species.txt
grep -iE "abies|picea|pinus" try_species.txt
```

If `curl` fails, try `wget`:

```bash
wget -O try_species.txt "https://www.try-db.org/dnld/TryAccSpecies.txt"
grep -iE "abies|picea|pinus" try_species.txt
```

If certificate validation fails, use:

```bash
wget -O try_species.txt "https://www.try-db.org/dnld/TryAccSpecies.txt" --no-check-certificate
grep -iE "abies|picea|pinus" try_species.txt
```

If certificate validation fails with curl, use:

```bash
curl -sL -k "https://www.try-db.org/dnld/TryAccSpecies.txt" -o try_species.txt
grep -iE "abies|picea|pinus" try_species.txt
```
Pure Python fallback (no curl/wget/rg/grep required):

```bash
python skills/try-skills/scripts/try_download_and_search.py --page species --pattern "abies|picea|pinus"
```

If certificate validation fails, use:

```bash
python skills/try-skills/scripts/try_download_and_search.py --page species --pattern "abies|picea|pinus" --insecure
```

## Notes

- TRY access policies may require registration or data-use agreements for some datasets.
- Use the dataset list page to identify dataset IDs/names, then follow TRY guidance
  for access or citation.

## Parsing helpers (local)

Use the Python helpers in `bioepic_skills/try_parser.py` to parse TRY tables locally:

```python
from bioepic_skills.try_parser import parse_try_species_text

records = parse_try_species_text(\"\"\"AccSpeciesID\\tAccSpeciesName\\tObsNum\\n271060\\tAa achalensis\\t5\"\"\")
```

Parse the TRY trait list HTML:

```python
from bioepic_skills.try_parser import parse_try_traits_html

with open(\"try_traits.html\", \"r\", encoding=\"utf-8\") as handle:
    records = parse_try_traits_html(handle.read())
```

Convert TRY trait HTML to JSON/TSV (CLI helper):

```bash
python skills/try-skills/scripts/try_traits_to_json.py try_traits.html --format json --output try_traits.json
```

```bash
python skills/try-skills/scripts/try_traits_to_json.py try_traits.html --format tsv --output try_traits.tsv
```

Convert TRY species list to JSON/TSV (CLI helper):

```bash
python skills/try-skills/scripts/try_species_to_json.py TryAccSpecies.txt --format json --output try_species.json
```

```bash
python skills/try-skills/scripts/try_species_to_json.py TryAccSpecies.txt --format tsv --output try_species.tsv
```

Note: The species file includes a header row. The helper auto-detects it and outputs
structured records with counts when present.

Convert TRY dataset list HTML to JSON/TSV (CLI helper, detailed by default):

```bash
python skills/try-skills/scripts/try_datasets_to_json.py try_datasets.html --format json --output try_datasets.json
```

```bash
python skills/try-skills/scripts/try_datasets_to_json.py try_datasets.html --format tsv --output try_datasets.tsv
```

Use the summary parser (title/id/doi/description only):

```bash
python skills/try-skills/scripts/try_datasets_to_json.py try_datasets.html --summary --format json --output try_datasets_summary.json
```

```bash
python skills/try-skills/scripts/try_datasets_to_json.py try_datasets.html --summary --format tsv --output try_datasets_summary.tsv
```

Filter datasets by keywords in `field_list` (or other fields):

```bash
python skills/try-skills/scripts/try_datasets_filter.py try_datasets_detailed.json --pattern "snow|snowpack" --fields "title,description,field_list" --output try_datasets_snow.json
```
