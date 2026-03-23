# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Changed
- Overhauled plugin examples to focus on essential patterns: lifecycle, config, commands, events
- Simplified to one command (`/hello`) demonstrating `isinstance` sender checks and config usage
- Simplified listener to player join/quit with custom messages
- Removed scheduler, permission attachment, and priority examples (too advanced for a starter template)
- Modernized build system with hatch-vcs for automatic git-tag versioning
- Switched from pip to uv for dependency management and builds
- Updated minimum Python version to 3.10
- Bumped api_version from 0.6 to 0.11
- Simplified source file names (plugin.py, listener.py)
- CI now runs linting (ruff)
- Replaced publish workflow with full release automation (changelog, tagging, PyPI, GitHub release)

### Added
- Default config.toml demonstrating plugin configuration
- Ruff linting configuration
- Dependabot for automated dependency updates
- CHANGELOG.md following Keep a Changelog format

### Removed
- Separate CommandExecutor class (command.py); on_command approach is simpler for examples
