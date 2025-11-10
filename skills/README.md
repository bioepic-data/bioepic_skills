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

## Use in Claude Code

To use these skills in Claude Code:

```
/plugin marketplace add ./.claude-plugin/marketplace.json
```

This will register the bioepic-skills plugin and make all skill definitions available to Claude Code.
