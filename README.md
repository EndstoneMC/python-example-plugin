# Endstone Python Example Plugin

[![Build](https://github.com/EndstoneMC/python-example-plugin/actions/workflows/build.yml/badge.svg)](https://github.com/EndstoneMC/python-example-plugin/actions/workflows/build.yml)

An example Python plugin for [Endstone](https://github.com/EndstoneMC/endstone) servers, demonstrating commands,
events, configuration, and permissions.

## Prerequisites

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Getting Started

1. **Clone this repository**

   ```bash
   git clone https://github.com/EndstoneMC/python-example-plugin.git
   cd python-example-plugin
   ```

2. **Install in development mode**

   ```bash
   uv sync --extra dev
   ```

3. **Run linting**

   ```bash
   uv run ruff check src/
   ```

4. **Build a wheel for distribution**

   ```bash
   uv build
   ```

   Copy the `.whl` from `dist/` into your Endstone server's `plugins/` folder.

## Structure

```
python-example-plugin/
├── src/
│   └── endstone_example/
│       ├── __init__.py       # Package entry point, re-exports ExamplePlugin
│       ├── plugin.py         # Plugin class: lifecycle, config, commands
│       ├── listener.py       # Event listener: player join/quit
│       └── config.toml       # Default plugin configuration
├── .github/
│   ├── dependabot.yml       # Automated dependency updates
│   └── workflows/
│       ├── build.yml        # CI: lint
│       └── release.yml      # Release automation
├── CHANGELOG.md             # Release notes (keepachangelog format)
├── pyproject.toml           # Build config, dependencies, tool settings
├── LICENSE                  # MIT License
└── README.md                # This file
```

## Documentation

For more on the Endstone API, see the [documentation](https://endstone.readthedocs.io).

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
