# Endstone Python Example Plugin

[![Build](https://github.com/EndstoneMC/python-example-plugin/actions/workflows/build.yml/badge.svg)](https://github.com/EndstoneMC/python-example-plugin/actions/workflows/build.yml)

A starter template for building [Endstone](https://github.com/EndstoneMC/endstone) plugins in Python.
Endstone is a plugin framework for Minecraft Bedrock Dedicated Server, similar to
Bukkit/Spigot/Paper for Java Edition. This template demonstrates commands, events,
configuration, and permissions.

## Use This Template

1. Click **Use this template** on GitHub (or fork/clone it)
2. Rename the following to match your plugin:

| What | Where | Example |
|------|-------|---------|
| Package name | `pyproject.toml` `[project] name` | `endstone-my-plugin` |
| Package directory | `src/endstone_example/` | `src/endstone_my_plugin/` |
| Entry point | `pyproject.toml` `[project.entry-points."endstone"]` | `my-plugin = "endstone_my_plugin:MyPlugin"` |
| Plugin class | `plugin.py` class name + `prefix` | `MyPlugin`, `prefix = "MyPlugin"` |
| Permission prefix | `plugin.py` `permissions` dict keys | `my_plugin.command.*` |

3. Set `api_version = "0.11"` (or the Endstone version you target)
4. Delete the example command/listener code and start building

## Development

This template uses [uv](https://docs.astral.sh/uv/) for fast dependency management. If you
prefer pip, replace `uv sync` with `pip install -e ".[dev]"` and `uv run` with just running
the command directly.

```bash
git clone https://github.com/EndstoneMC/python-example-plugin.git
cd python-example-plugin
uv sync --extra dev       # Install dependencies
uv run ruff check src/    # Lint
```

For live development on a running server, activate the server's virtualenv and install in
editable mode:

```bash
pip install -e .
```

Then use `/reload` in-game to pick up code changes without restarting.

## Project Structure

```
src/endstone_example/
  __init__.py       Re-exports the plugin class
  plugin.py         Plugin lifecycle, commands, config
  listener.py       Event listener (player join/quit)
  config.toml       Default config (copied on first run)
```

## Install on a Server

```bash
uv build
```

Copy the `.whl` from `dist/` into your server's `plugins/` folder and restart.

## Releasing

This template includes a GitHub Actions release workflow. To make a release:

1. Add your changes under `## [Unreleased]` in `CHANGELOG.md`
2. Go to **Actions > Release > Run workflow**
3. Enter the version (e.g. `0.5.0`) and run

The workflow validates the version, updates the changelog, creates a git tag and GitHub release,
builds the wheel, publishes to PyPI (if configured), and attaches the `.whl` to the release.

Use **dry run** to preview without making changes.

Versioning is handled automatically by [hatch-vcs](https://github.com/ofek/hatch-vcs): tagged
commits get clean versions (e.g. `0.5.0`), untagged commits get dev versions
(e.g. `0.5.1.dev3`).

## Documentation

For more on the Endstone API, see the [documentation](https://endstone.dev/latest/).

## License

[MIT License](LICENSE)
