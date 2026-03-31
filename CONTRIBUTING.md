# Contributing

Contributions to the **DocDo** systematic review pipeline are welcome.

## What to contribute

- Bug fixes and test coverage for the `docdo` library
- Documentation improvements
- Pipeline tooling improvements
- Cross-platform improvements (Windows + macOS + Linux)

## What not to contribute

- Proprietary datasets or restricted third-party content
- Credentials, API keys, or tokens
- Personal or identifying information

## Development setup

```bash
python -m pip install -U pip
python -m pip install -e ".[dev]"
```

## Checks

```bash
python -m ruff check .
python -m pytest
```

## Pull request guidelines

- Keep changes focused and well-scoped.
- Include tests for new functionality.
- Update documentation if you change folder structure or CLI commands.
