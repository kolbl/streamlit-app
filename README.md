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

`uv sync` creates/updates `.venv` and installs dependencies from `pyproject.toml`.

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


If you are using Visual Studio Code - just select the Python interpreter from the freshly created venv folder .venv/bin/python. 

## Install Workshop Package from TestPyPI

If your app depends on the workshop package, install it like this:

```bash
uv add "data-analytics_<...>==0.1.0.dev1" \
  --extra-index-url https://test.pypi.org/simple/ \
  --index-strategy unsafe-best-match
```