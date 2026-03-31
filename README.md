# gitlog

A CLI tool for summarizing git repository activity over a configurable time window.

## Features

- View commit summaries for any local git repository
- Filter commits by a rolling time window (default: last 7 days)
- Output rendered as a formatted table in the terminal via [Rich](https://github.com/Textualize/rich)

## Requirements

- Python >= 3.13
- [Poetry](https://python-poetry.org/)

## Installation

```bash
git clone https://github.com/princej02/gitlog.git
cd gitlog
poetry install
```

## Usage

```bash
gitlog [PATH] [--days N]
```

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `PATH` | argument | `.` | Path to the git repository to analyze |
| `--days` | option | `7` | How many days back to look for commits |

### Examples

Summarize the current repository over the last 7 days:

```bash
gitlog
```

Summarize a specific repository:

```bash
gitlog /path/to/repo
```

Look back 30 days:

```bash
gitlog --days 30
```

Combine both:

```bash
gitlog /path/to/repo --days 14
```

## Development

Install all dependency groups:

```bash
poetry install --with dev,test
```

### Linting and formatting

```bash
# Format code
poetry run black src/

# Sort imports
poetry run isort src/

# Lint
poetry run flake8 src/
poetry run pylint src/

# Type check
poetry run mypy src/
```

### Running tests

```bash
poetry run pytest
```

### Pre-commit hook

A pre-commit hook is included to run formatting and linting automatically before each commit. Install it with:

```bash
cp hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

## Project structure

```
gitlog/
├── src/
│   └── gitlog/
│       ├── main.py       # Entry point
│       ├── app.py        # CLI commands and core logic
│       └── version.py    # Version command
├── tests/
├── hooks/
│   └── pre-commit        # Git pre-commit hook
└── pyproject.toml
```
