# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [0.5.0] - 2026-03-23

### Changed
- Overhauled plugin examples to focus on essential patterns: lifecycle, config, commands, events
- Two commands (`/hello`, `/broadcast`) demonstrating `isinstance` sender checks, config usage, and arguments
- Simplified listener to player join/quit with event priority example
- Modernized build system with hatch-vcs for automatic git-tag versioning
- Switched from pip to uv for dependency management and builds
- Updated minimum Python version to 3.10
- Bumped api_version from 0.6 to 0.11
- Simplified source file names (plugin.py, listener.py)
- CI now runs linting (ruff)
- Replaced publish workflow with full release automation (changelog, tagging, PyPI, GitHub release)
- README rewritten as a practical template quickstart with renaming guide, dependency instructions, and release docs
- Fixed deprecated ServerListPingEvent API (remote_host/remote_port to address)

### Added
- AGENTS.md to guide AI coding agents building Endstone plugins
- Default config.toml with multiple value types (string, bool)
- Comments and docstrings throughout example code explaining what and why
- CONTRIBUTING.md, bug report and feature request issue templates
- Ruff linting and Dependabot configuration

### Removed
- Separate CommandExecutor class (command.py); on_command approach is simpler for examples
- Scheduler, permission attachment examples (too advanced for a starter template)
