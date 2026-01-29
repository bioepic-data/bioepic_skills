---
name: essdive-search
description: Skills for searching ESS-DIVE datasets via the Dataset API
---

# Commands

`bioepic essdive-search --help`
`bioepic essdive-dataset --help`

## Full details

## Fallback (No CLI Required)

If the `bioepic` CLI is not installed, use the ESS-DIVE API directly with curl or
Python's standard library (no third-party packages required).

Alternatively, use the bundled script:

```bash
python skills/essdive-search/scripts/essdive_search.py search --keyword "snow depth" --page-size 5
```

```bash
python skills/essdive-search/scripts/essdive_search.py dataset 7a9f0b1f-1234-5678-9abc-def012345678
```

Save output to a file:

```bash
python skills/essdive-search/scripts/essdive_search.py search --keyword "snow depth" --page-size 5 --output results.json
```

```bash
python skills/essdive-search/scripts/essdive_search.py dataset 7a9f0b1f-1234-5678-9abc-def012345678 --output dataset.json
```

Print the resolved URL for debugging:

```bash
python skills/essdive-search/scripts/essdive_search.py search --keyword "snow depth" --page-size 5 --debug-url
```

Use a token file (to avoid putting the token in shell history):

```bash
python skills/essdive-search/scripts/essdive_search.py --token-file /path/to/token.txt search --keyword "snow"
```

Notes:
- `--page-size` and `--row-start` must be >= 0.

### curl examples

Search by keyword:

```bash
curl -sG \"https://api.ess-dive.lbl.gov/packages\" \\
  -H \"User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0\" \\
  -H \"Content-Type: application/json\" \\
  -H \"Range: bytes=0-1000\" \\
  --data-urlencode \"text=snow depth\" \\
  --data-urlencode \"page_size=5\" \\
  --data-urlencode \"row_start=0\" \\
  --data-urlencode \"isPublic=true\"
```

Fetch a dataset by package ID:

```bash
curl -sG \"https://api.ess-dive.lbl.gov/packages/REPLACE_WITH_PACKAGE_ID\" \\
  -H \"User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0\" \\
  -H \"Content-Type: application/json\" \\
  -H \"Range: bytes=0-1000\" \\
  --data-urlencode \"isPublic=true\"
```

Authenticated (private) access:

```bash
curl -sG \"https://api.ess-dive.lbl.gov/packages\" \\
  -H \"Authorization: Bearer $ESSDIVE_TOKEN\" \\
  -H \"User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0\" \\
  -H \"Content-Type: application/json\" \\
  -H \"Range: bytes=0-1000\" \\
  --data-urlencode \"text=snow depth\" \\
  --data-urlencode \"isPublic=false\"
```

### Python stdlib example

```python
from urllib import parse, request

params = {
    \"text\": \"snow depth\",
    \"page_size\": 5,
    \"row_start\": 0,
    \"isPublic\": \"true\",
}

url = \"https://api.ess-dive.lbl.gov/packages?\" + parse.urlencode(params)
req = request.Request(
    url,
    headers={
        \"Accept\": \"application/json\",
        \"User-Agent\": \"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0\",
        \"Content-Type\": \"application/json\",
        \"Range\": \"bytes=0-1000\",
    },
)

with request.urlopen(req, timeout=30) as resp:
    print(resp.read().decode(\"utf-8\"))
```

### ESS-DIVE Dataset Search

Usage: `bioepic essdive-search [OPTIONS]`

Search ESS-DIVE datasets using the Dataset API. Useful for discovery by keyword,
provider/project name, or custom query parameters.

**Authentication:**
- Public searches do not require a token
- To include private datasets, set `ESSDIVE_TOKEN` or pass `--token`

Examples:

    # Search by keyword
    bioepic essdive-search --keyword "soil" --page-size 10

    # Search by provider/project name
    bioepic essdive-search --provider-name "Project Name"

    # Pass extra query parameters directly
    bioepic essdive-search --param "doi=10.15485/1234567"

╭─ Options ──────────────────────────────────────────────────────────────────────╮
│ --keyword           -k  TEXT     Keyword to search for                         │
│ --provider-name     -p  TEXT     Provider/project name                          │
│ --page-size             INTEGER Number of records per page [default: 25]       │
│ --row-start             INTEGER Row offset for pagination [default: 0]         │
│ --public/--include-private        Limit to public datasets by default          │
│ --param                 TEXT     Extra query parameter in key=value form       │
│ --token                 TEXT     ESS-DIVE API token (or use ESSDIVE_TOKEN)     │
│ --base-url              TEXT     ESS-DIVE API base URL                          │
│ --output            -o  PATH     Save JSON response to file                     │
│ --verbose           -v           Increase verbosity                            │
│ --help                           Show this message and exit.                   │
╰───────────────────────────────────────────────────────────────────────────────╯

---

### ESS-DIVE Dataset Fetch

Usage: `bioepic essdive-dataset [OPTIONS] PACKAGE_ID`

Fetch a single dataset record by package ID.

Examples:

    # Fetch a public dataset
    bioepic essdive-dataset 7a9f0b1f-1234-5678-9abc-def012345678

    # Include private datasets (requires token)
    bioepic essdive-dataset 7a9f0b1f-1234-5678-9abc-def012345678 --include-private

╭─ Options ──────────────────────────────────────────────────────────────────────╮
│ --public/--include-private        Treat the dataset as public by default       │
│ --token                 TEXT     ESS-DIVE API token (or use ESSDIVE_TOKEN)     │
│ --base-url              TEXT     ESS-DIVE API base URL                          │
│ --output            -o  PATH     Save JSON response to file                     │
│ --verbose           -v           Increase verbosity                            │
│ --help                           Show this message and exit.                   │
╰───────────────────────────────────────────────────────────────────────────────╯
