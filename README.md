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


If you are using Visual Studio Code or Cursor, select the Python interpreter at `.venv/bin/python`. The **Debug Streamlit** launch configuration starts `src/app.py` under the debugger.

## Install the workshop package from a local index

`data-analytics` (`>=0.3.0`) comes from a local package index. `pyproject.toml` lists that server twice, as `localhost` and as `127.0.0.1`. `uv.lock` resolves packages from `http://localhost:8080/simple/`.

Add the package with that index. `uv` appends the URL to `pyproject.toml`, so later `uv lock` and `uv sync` keep using it:

```bash
uv add data-analytics --index http://localhost:8080/simple/
```

The project currently records both URLs:

```toml
[[tool.uv.index]]
url = "http://localhost:8080/simple/"



These indexes are used in addition to PyPI. Start the local server before `uv lock` or `uv sync`.
