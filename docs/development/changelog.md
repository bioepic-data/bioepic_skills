# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Migrated documentation from Sphinx to MkDocs with Material theme
- Updated documentation structure for better organization
- Switched from pip to uv for package management
- Changed build backend from setuptools to hatchling
- Removed requirements.txt files (now managed by pyproject.toml)
- Updated CI/CD workflows to use uv
- Added ruff as a linting tool

## [0.1.0] - 2025-11-10

### Added
- Initial project structure
- Base API functionality (`APIBase`, `APISearch`)
- Authentication system (`BioEPICAuth`)
- Data processing utilities (`DataProcessing`)
- Custom decorators (`@requires_auth`)
- Basic test suite
- Documentation setup
- Example usage code
- GitHub Actions CI/CD workflow
- Contributing guidelines
- Project metadata and configuration

### Documentation
- Installation guide
- Quick start tutorial
- User guide with authentication and data processing examples
- API reference for all modules
- Development documentation

[Unreleased]: https://github.com/bioepic-data/bioepic_skills/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/bioepic-data/bioepic_skills/releases/tag/v0.1.0
