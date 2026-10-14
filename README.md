# Streamlit Workshop App

Companion Streamlit app for the **"Ready, Set, Publish: Write Your First Python Package"** workshop.

This project demonstrates how to run a Streamlit app that depends on a packaged Python library (for example, `data_analytics`).

## Prerequisites

- [`uv`](https://docs.astral.sh/uv/)

## Quick Start

From the project root:

```bash
uv python install 3.13
uv sync
uv run streamlit run src/app.py
```

`uv sync` creates or updates `.venv` and installs dependencies from `pyproject.toml`. `data-analytics` comes from the local package index, so that server has to be running before `uv sync`.

## Run Commands

Primary command:

```bash
uv run streamlit run src/app.py
```


Always run commands from the repository root so imports and paths resolve correctly.

## Optional: Activate the Virtual Environment

You usually do not need this because `uv run` handles it automatically. 

```bash
source .venv/bin/activate
streamlit run src/app.py
```


If you are using Visual Studio Code or Cursor, select the Python interpreter at `.venv/bin/python`.

## Install the workshop package from a local index

`data-analytics` is pinned to `0.2.0` and comes from one local package index, used in addition to PyPI. `pyproject.toml` records it as:

```toml
[[tool.uv.index]]
url = "http://localhost:8080/simple/"
```

`uv.lock` resolves `data-analytics` from `http://localhost:8080/simple/`. Start that server before `uv lock` or `uv sync`.

To add the package from that index again:

```bash
uv add data-analytics --index http://localhost:8080/simple/
```
