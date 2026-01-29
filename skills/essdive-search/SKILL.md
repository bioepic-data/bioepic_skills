---
name: essdive-search
description: Skills for searching ESS-DIVE datasets via the Dataset API
---

# Commands

`bioepic essdive-search --help`
`bioepic essdive-dataset --help`

## Full details

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
