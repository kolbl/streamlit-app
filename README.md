# Streamlit Workshop App

Companion Streamlit app for the **"Ready, Set, Publish: Write Your First Python Package"** workshop.

This project demonstrates how to run a Streamlit app that depends on a packaged Python library (for example, `data_analytics`).

## Prerequisites

- Python 3.13
- [`uv`](https://docs.astral.sh/uv/)

## Quick Start

From the project root:

```bash
uv sync
uv run streamlit run src/app.py
```

`uv sync` creates/updates `.venv` and installs dependencies from `pyproject.toml`.

## Run Commands

Primary command:

```bash
uv run streamlit run src/app.py
```

Equivalent command:

```bash
uv run python -m streamlit run src/app.py
```

Always run commands from the repository root so imports and paths resolve correctly.

## Optional: Activate the Virtual Environment

You usually do not need this because `uv run` handles it automatically.

```bash
source .venv/bin/activate
streamlit run src/app.py
```

## Install Workshop Package from TestPyPI

If your app depends on the workshop package, install it like this:

```bash
uv add "data-analytics_<...>==0.1.0.dev1" \
  --extra-index-url https://test.pypi.org/simple/ \
  --index-strategy unsafe-best-match
```

Then re-sync:

```bash
uv sync
```

## Troubleshooting

If you see an import error for `data_analytics`:

- confirm the package is listed in `pyproject.toml`
- run `uv sync` again
- make sure you are launching from the project root

## Project Structure

```text
streamlit-app/
├── src/
│   └── app.py
├── pyproject.toml
└── README.md
```