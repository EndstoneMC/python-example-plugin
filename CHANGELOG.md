# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Changed
- Modernized build system with hatch-vcs for automatic git-tag versioning
- Switched from pip to uv for dependency management and builds
- Updated minimum Python version to 3.10
- Bumped api_version from 0.6 to 0.11
- Simplified source file names (plugin.py, listener.py, command.py)
- CI now runs linting (ruff)
- Replaced publish workflow with full release automation (changelog, tagging, PyPI, GitHub release)

### Added
- Ruff linting configuration
- Dependabot for automated dependency updates
- CHANGELOG.md following Keep a Changelog format
