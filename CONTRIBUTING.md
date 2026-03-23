# Contributing

Thanks for your interest in improving this template!

## Development Setup

```bash
git clone https://github.com/EndstoneMC/python-example-plugin.git
cd python-example-plugin
uv sync --extra dev
```

## Making Changes

1. Create a branch for your changes
2. Run `uv run ruff check src/` before committing
3. Update `CHANGELOG.md` under `## [Unreleased]` if your change is user-facing
4. Open a pull request with a clear description of what changed and why

## Code Style

- Follow existing patterns in the codebase
- Keep examples simple and well-commented (this is a teaching template)
- Run `uv run ruff check src/` to lint

## Reporting Issues

Use [GitHub Issues](https://github.com/EndstoneMC/python-example-plugin/issues) for bugs
and feature requests.
