# bioepic-skills

This directory contains skill definitions for use with Claude Code and other AI assistants.

## Available Skills

### ontology-grounding

Skills for grounding environmental and biological research variable names to appropriate ontologies using the Ontology Access Kit.

**Key capabilities:**
- Ground free-text terms to standardized ontology concepts
- Support for multiple ontologies (BERVO, ENVO, ChEBI, NCBI Taxonomy, COMO, PO, MIXS)
- Confidence scoring for match quality
- Batch processing of term lists
- Python API and CLI access

**Use cases:**
- Standardizing research metadata
- Data integration across studies
- Quality control for terminology
- Linking data to formal ontologies

See [ontology-grounding/SKILL.md](./ontology-grounding/SKILL.md) for full documentation.

### essdive-extraction

Skills for extracting and processing variable names from ESS-DIVE (Environmental System Science Data Infrastructure for a Virtual Ecosystem) datasets.

**Key capabilities:**
- Retrieve dataset metadata from ESS-DIVE API
- Extract variable names from data files (CSV, TSV, Excel, XML)
- Process data dictionaries with definitions and units
- Match extracted terms against reference lists
- Fuzzy matching for approximate term matching
- Parallel processing for large datasets

**Use cases:**
- Dataset discovery and analysis
- Ontology mapping of real-world data
- Data standardization assessment
- Cross-dataset integration

See [essdive-extraction/SKILL.md](./essdive-extraction/SKILL.md) for full documentation.

### essdive-search

Skills for searching ESS-DIVE datasets via the Dataset API.

**Key capabilities:**
- Search datasets by keyword, provider/project name, or custom parameters
- Fetch a single dataset record by package ID
- Optional token support for private datasets

**Use cases:**
- Dataset discovery
- Quick dataset metadata lookup
- Integrating ESS-DIVE search into workflows

See [essdive-search/SKILL.md](./essdive-search/SKILL.md) for full documentation.

### try-skills

Skills for discovering datasets, traits, and species information from the TRY plant trait database.

**Key capabilities:**
- Search TRY dataset listings by keyword
- Access the full TRY trait list
- Access the list of species with TRY annotations

**Use cases:**
- Dataset discovery in TRY
- Trait lookup and terminology alignment
- Species coverage checks

See [try-skills/SKILL.md](./try-skills/SKILL.md) for full documentation.

### fred-skills

Skills for discovering traits, species, and data sources in the Fine-Root Ecology Database (FRED).

**Key capabilities:**
- Parse the FRED trait inventory (HTML → JSON/TSV)
- Parse the FRED species list (HTML → JSON/TSV)
- Download and parse FRED data sources (best-effort pagination)

**Use cases:**
- Trait and species coverage checks
- Data source discovery
- Local search over FRED metadata

See [fred-skills/SKILL.md](./fred-skills/SKILL.md) for full documentation.

## Use in Claude Code

To use these skills in Claude Code:

```
/plugin marketplace add ./.claude-plugin/marketplace.json
```

This will register the bioepic-skills plugin and make all skill definitions available to Claude Code.
